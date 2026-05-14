import json
from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.database.queries.get_data_project import get_data_project
from gene_essence_interface.database.queries.get_models import get_models
from gene_essence_interface.database.queries.get_projects import get_projects
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.InformationProjectFrame import InformationProjectFrame
from gene_essence_interface.pages.components.LoadProjectFrame import LoadProjectFrame
from gene_essence_interface.pages.components.NavigationSidebar import NavigationSidebar, STEPS_BY_TYPE, STEP_INDEX_BY_TYPE
from gene_essence_interface.pages.components.SegmentedToggle import SegmentedToggle
from gene_essence_interface.pages.components.CustomErrorDialog import show_error_dialog
from gene_essence_interface.utils.check_system_resources import check_system_resources_for_model

BG = COLORS['background_alt']


class InformationProject(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.analyse_type = None

        self.radio_var = StringVar(value='create')
        self.project_name = StringVar()
        self.file_path_var = StringVar()
        self.model_file_path_var = StringVar()
        self.test_size = DoubleVar()
        self.directory_var = StringVar()
        self.selected_project = StringVar()

        self._sidebar = NavigationSidebar(self)
        self._sidebar.pack(side=LEFT, fill=Y)
        self._sidebar.set_active_step(1)

        self._content = Frame(self, bg=BG)
        self._content.pack(side=RIGHT, fill=BOTH, expand=True)

        self._right_body = None
        self.next_page = None
        self._trace_ids = []

        self.bind('<Visibility>', self._on_visible)

    def on_show(self):
        t = self.controller.get_analyse_type() or 'Training'
        self._sidebar.reset_steps(STEPS_BY_TYPE[t])
        self._sidebar.set_active_step(STEP_INDEX_BY_TYPE[t]['InformationProject'])

    def _on_visible(self, event):
        new_type = self.controller.get_analyse_type()
        if new_type == self.analyse_type and self._right_body is not None:
            return
        self.analyse_type = new_type
        self._rebuild()

    def _rebuild(self):
        for var, mode, cbname in self._trace_ids:
            try:
                var.trace_remove(mode, cbname)
            except Exception:
                pass
        self._trace_ids.clear()

        if self._right_body:
            self._right_body.destroy()

        self._right_body = Frame(self._content, bg=BG)
        self._right_body.pack(fill=BOTH, expand=True)

        # Bottom buttons (packed first to stick to bottom)
        btn_frame = Frame(self._right_body, bg=BG)
        btn_frame.pack(side=BOTTOM, fill=X, padx=20, pady=12)
        Frame(self._right_body, bg=COLORS['border'], height=1).pack(side=BOTTOM, fill=X)

        self.next_page = CustomButton(btn_frame, text='NEXT →', variant='primary',
                                      state=DISABLED, command=self._save_and_proceed)
        self.next_page.pack(side=RIGHT)
        CustomButton(btn_frame, text='← BACK', variant='secondary',
                     command=self.controller.go_back).pack(side=RIGHT, padx=(0, 8))

        # Title
        title_area = Frame(self._right_body, bg=BG)
        title_area.pack(fill=X, padx=20, pady=(20, 0))
        Label(title_area, text=f'Project information — {self.analyse_type}',
              bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold')).pack(anchor=W)


        # Forms area
        forms = Frame(self._right_body, bg=BG)
        forms.pack(fill=BOTH, expand=True, padx=20, pady=12)

        has_projects = bool(get_projects(self.analyse_type))

        if has_projects:
            toggle_frame = Frame(forms, bg=BG)
            toggle_frame.pack(fill=X, pady=(0, 10))
            SegmentedToggle(toggle_frame, variable=self.radio_var,
                            options=[('Create new', 'create'), ('Load existing', 'load')]
                            ).pack(fill=X)
        else:
            self.radio_var.set('create')

        # Create form
        self._create_frame = InformationProjectFrame(
            forms, self.controller,
            analyse_type=self.analyse_type,
            project_name_var=self.project_name,
            file_path_var=self.file_path_var,
            model_file_path_var=self.model_file_path_var,
            test_size=self.test_size,
            directory_var=self.directory_var,
            update_callback=self._check_next,
        )

        # Load form (only if projects exist)
        self._load_frame = None
        if has_projects:
            self._load_frame = LoadProjectFrame(
                forms, self.controller,
                selected_project=self.selected_project,
                analyse_type=self.analyse_type,
            )

        self._trace_ids += [
            (self.radio_var,         'write', self.radio_var.trace_add('write', self._switch_form)),
            (self.project_name,      'write', self.project_name.trace_add('write', self._check_next)),
            (self.selected_project,  'write', self.selected_project.trace_add('write', self._check_next)),
        ]
        self._switch_form()
        self.update_idletasks()

    def _switch_form(self, *args):
        mode = self.radio_var.get()
        if mode == 'create':
            if self._load_frame:
                self._load_frame.pack_forget()
            self._create_frame.pack(fill=X)
        elif mode == 'load' and self._load_frame:
            self._create_frame.pack_forget()
            self._load_frame.pack(fill=X)
        self._check_next()
        self.update_idletasks()

    def _check_next(self, *args):
        if not self.next_page or not self.next_page.winfo_exists():
            return
        name = self.project_name.get()
        file = self.file_path_var.get()
        directory = self.directory_var.get()
        test_size = self.test_size.get()
        model_file = self.model_file_path_var.get()
        sel = self.selected_project.get()

        if self.radio_var.get() == 'create':
            valid = self._valid_create(name, file, directory, test_size, model_file)
        else:
            valid = sel not in ('', 'Choose the project')

        self.next_page.config(state=NORMAL if valid else DISABLED)

    def _valid_create(self, name, file, directory, test_size, model_file):
        if self.analyse_type == 'Ensemble':
            return directory and (5 <= len(name) <= 10) and file and (0.1 <= test_size <= 0.9)
        elif self.analyse_type == 'Prediction':
            return (5 <= len(name) <= 10) and file and model_file
        elif self.analyse_type == 'Training':
            return (5 <= len(name) <= 10) and file and (0.1 <= test_size <= 0.9)
        return False

    def _save_and_proceed(self):
        self._reset_project_settings()
        if self.radio_var.get() == 'create':
            self._handle_create()
        else:
            self._handle_load()

    def _handle_create(self):
        model_file = self.model_file_path_var.get()
        if self.analyse_type == 'Prediction' and model_file:
            ok, msg = check_system_resources_for_model(model_file)
            if not ok:
                show_error_dialog(self, 'Insufficient Resources', msg)
                return

        models = get_models()
        self.controller.set_model_parameters({m['name']: m['parameters'] for m in models})
        self.controller.set_project_name(self.project_name.get())
        self.controller.set_csv_file_path(self.file_path_var.get())
        self.controller.set_project_type('create')

        if self.analyse_type == 'Ensemble':
            self.controller.set_directory_path(self.directory_var.get())
        elif self.analyse_type == 'Prediction':
            self.controller.set_model_file_path(model_file)
        if self.analyse_type in ('Ensemble', 'Training'):
            self.controller.set_test_size(self.test_size.get())

        self.controller.show_page(
            {'Training': 'ChooseModels', 'Prediction': 'ChooseHowToReceiveTheResults'
             }.get(self.analyse_type, 'ChooseMetrics')
        )

    def _handle_load(self):
        project_name = self.selected_project.get()
        project = get_data_project(self.analyse_type, project_name)
        if not project:
            return

        if self.analyse_type == 'Prediction':
            model_file = project.get('model_file', '')
            if model_file:
                ok, msg = check_system_resources_for_model(model_file)
                if not ok:
                    show_error_dialog(self, 'Insufficient Resources', msg)
                    return

        self.controller.set_project_type('load')
        self.controller.set_project_name(project.get('project_name', ''))
        self.controller.set_csv_file_path(project.get('file_path_csv', ''))
        self.controller.set_metrics(project.get('selected_metrics', []))
        self.controller.set_receipt_type(project.get('result_delivery_method', ''))
        self.controller.set_receipt_in(project.get('delivery_contact', ''))

        if self.analyse_type == 'Prediction':
            self.controller.set_model_file_path(project.get('model_file', ''))
        else:
            self.controller.set_models(project.get('selected_models', []))
            self.controller.set_model_parameters(
                json.loads(project.get('model_parameters', '{}')))
            if self.analyse_type == 'Ensemble':
                self.controller.set_directory_path(project.get('model_directory_path', ''))
            elif self.analyse_type == 'Training':
                self.controller.set_test_size(project.get('test_size', ''))

        self.controller.show_page(
            {'Training': 'ChooseModels', 'Prediction': 'ChooseHowToReceiveTheResults'
             }.get(self.analyse_type, 'ChooseMetrics')
        )

    def _reset_project_settings(self):
        for setter, val in [
            (self.controller.set_project_name, ''),
            (self.controller.set_csv_file_path, ''),
            (self.controller.set_test_size, 0.0),
            (self.controller.set_model_file_path, ''),
            (self.controller.set_directory_path, ''),
            (self.controller.set_models, []),
            (self.controller.set_model_parameters, {}),
            (self.controller.set_metrics, []),
            (self.controller.set_receipt_type, ''),
            (self.controller.set_receipt_in, ''),
        ]:
            setter(val)