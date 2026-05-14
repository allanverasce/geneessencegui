from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.database.queries.save_project import save_project
from gene_essence_interface.database.queries.update_project import update_project
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.RoundedCard import RoundedCard

BG = COLORS['background_alt']
_SEP = '#F1F5F9'


def _row(parent, key, value, is_last=False):
    if not value or str(value).strip() in ('N/A', 'None', ''):
        return False
    row = Frame(parent, bg=COLORS['card_bg'])
    row.pack(fill=X, pady=0)
    Label(row, text=key, bg=COLORS['card_bg'], fg='#64748B',
          font=('Arial', 11), anchor=W).pack(side=LEFT, pady=7)
    Label(row, text=str(value), bg=COLORS['card_bg'], fg='#1A2332',
          font=('Arial', 11, 'bold'), anchor=E, wraplength=280,
          justify=RIGHT).pack(side=RIGHT, pady=7)
    if not is_last:
        Frame(parent, bg=_SEP, height=1).pack(fill=X)
    return True


class InformationProject(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        # Bottom buttons
        btn_frame = Frame(self, bg=BG)
        btn_frame.pack(side=BOTTOM, fill=X, padx=20, pady=12)
        Frame(self, bg=COLORS['border'], height=1).pack(side=BOTTOM, fill=X)

        CustomButton(btn_frame, text='CONFIRM AND RUN', variant='success',
                     command=self._next_page).pack(side=RIGHT)
        CustomButton(btn_frame, text='← BACK', variant='secondary',
                     command=self.controller.go_back).pack(side=RIGHT, padx=(0, 8))

        self._msg_label = Label(btn_frame, text='', fg=COLORS['success'],
                                bg=BG, font=('Arial', 11), wraplength=350)
        self._msg_label.pack(side=LEFT)

        # Title
        title_area = Frame(self, bg=BG)
        title_area.pack(fill=X, padx=20, pady=(20, 0))
        Label(title_area, text='Confirm information',
              bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold')).pack(anchor=W)

        self._cards_area = Frame(self, bg=BG)
        self._cards_area.pack(fill=BOTH, expand=True, padx=20, pady=12)

        self.bind('<Visibility>', self._on_visible)

    def _on_visible(self, event):
        for w in self._cards_area.winfo_children():
            w.destroy()
        self._render_cards()

    def _render_cards(self):
        ctrl = self.controller
        atype = ctrl.get_analyse_type() or ''

        card = RoundedCard(self._cards_area)
        card.pack(fill=X)
        body = Frame(card._body, bg=COLORS['card_bg'])
        body.pack(fill=X, padx=14, pady=2)

        rows = []
        rows.append(('Analysis type', atype))
        rows.append(('Project name', ctrl.get_project_name()))
        rows.append(('CSV file', ctrl.get_csv_file_path()))
        if atype in ('Training', 'Ensemble'):
            rows.append(('Test size', str(ctrl.get_test_size())))
        if atype == 'Prediction':
            rows.append(('Model file', ctrl.get_model_file_path()))
        if atype == 'Ensemble':
            rows.append(('Models directory', ctrl.get_directory_path()))
        if atype in ('Training', 'Ensemble'):
            models = ctrl.get_models() or []
            rows.append(('Models', ', '.join(models) if models else '—'))
        if atype != 'Prediction':
            metrics = ctrl.get_metrics() or []
            rows.append(('Metrics', ', '.join(metrics) if metrics else '—'))
        method = ctrl.get_receipt_type() or ''
        dest = ctrl.get_receipt_in() or ''
        delivery_val = f'{method.capitalize()} — {dest}' if method and dest else (method or dest or '—')
        rows.append(('Delivery', delivery_val))

        for i, (key, val) in enumerate(rows):
            _row(body, key, val, is_last=(i == len(rows) - 1))

    def _next_page(self):
        ctrl = self.controller
        project_data = {
            'project_name': ctrl.get_project_name(),
            'project_type': ctrl.get_analyse_type(),
            'model_file': ctrl.get_model_file_path(),
            'file_path_csv': ctrl.get_csv_file_path(),
            'selected_models': ctrl.get_models(),
            'selected_metrics': ctrl.get_metrics(),
            'status': 'Pending Analysis',
            'result_delivery_method': ctrl.get_receipt_type(),
            'delivery_contact': ctrl.get_receipt_in(),
            'model_directory_path': ctrl.get_directory_path(),
            'test_size': ctrl.get_test_size(),
            'model_parameters': ctrl.get_all_model_parameters(),
        }

        project_type = ctrl.get_project_type()
        if project_type == 'create':
            msg = save_project(**project_data)
        elif project_type == 'load':
            msg = update_project(**project_data)
        else:
            msg = 'Invalid project type.'

        success = 'successfully' in msg
        self._msg_label.config(text=msg, fg=COLORS['success'] if success else COLORS['error'])

        if success:
            data = {
                'project_name': ctrl.get_project_name(),
                'analysis_type': (ctrl.get_analyse_type() or '').lower(),
                'model_file': ctrl.get_model_file_path(),
                'selected_models': ctrl.get_models(),
                'file_path_csv': ctrl.get_csv_file_path(),
                'selected_metrics': [m.lower() for m in (ctrl.get_metrics() or [])],
                'status': 'Pending Analysis',
                'test_size': ctrl.get_test_size(),
                'result_delivery_method': (ctrl.get_receipt_type() or '').lower(),
                'delivery_contact': ctrl.get_receipt_in(),
                'model_directory_path': ctrl.get_directory_path(),
                'model_parameters': ctrl.get_all_model_parameters(),
            }
            ctrl.set_data_to_analyze(data)
            ctrl.show_page('RunAnalysis')