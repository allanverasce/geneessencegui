import os
from tkinter import *
from tkinter import filedialog
import csv

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.database.queries.check_project_exists import check_project_exists
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.RoundedCard import RoundedCard

_LABEL_FG = COLORS['subtitle']
_SEP_COLOR = '#F1F5F9'


class InformationProjectFrame(RoundedCard):
    """Form for creating a new project (project name, CSV, test size, optional fields)."""

    def __init__(self, parent, controller, analyse_type, project_name_var, file_path_var,
                 model_file_path_var, test_size, directory_var, update_callback,
                 **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.analyse_type = analyse_type
        self.project_name_var = project_name_var
        self.file_path_var = file_path_var
        self.model_file_path_var = model_file_path_var
        self.test_size = test_size
        self.directory_var = directory_var
        self.update_callback = update_callback
        self._separators = []

        self._build_form()
        self.project_name_var.trace_add('write', self._on_name_changed)
        self.after(0, self._force_render)

    def _force_render(self):
        if self.winfo_exists():
            self.update_idletasks()

    def _build_form(self):
        self._create_name_field()
        self._sep()
        self._create_file_field()

        if self.analyse_type != 'Prediction':
            self._sep()
            self._create_test_size_field()
        if self.analyse_type == 'Ensemble':
            self._sep()
            self._create_directory_field()
        if self.analyse_type == 'Prediction':
            self._sep()
            self._create_model_file_field()

        if self._separators:
            self._separators[-1].destroy()
            self._separators.pop()

    def _sep(self):
        sep = Frame(self._body, bg=_SEP_COLOR, height=1)
        sep.pack(fill=X, padx=14)
        self._separators.append(sep)

    def _row(self, label_text):
        """Horizontal label | value row. Returns right-side Frame."""
        row = Frame(self._body, bg=COLORS['card_bg'])
        row.pack(fill=X, padx=14)

        Label(row, text=label_text, bg=COLORS['card_bg'], fg=_LABEL_FG,
              font=('Arial', 11), anchor=W).pack(side=LEFT, pady=8)

        right = Frame(row, bg=COLORS['card_bg'])
        right.pack(side=LEFT, fill=X, expand=True, pady=4)
        return right

    def _create_name_field(self):
        right = self._row('Project name')

        entry_wrap = Frame(right, bg=COLORS['border'])
        entry_wrap.pack(side=LEFT)
        entry_inner = Frame(entry_wrap, bg='#F8FAFC')
        entry_inner.pack(padx=1, pady=1)

        vcmd = (entry_inner.register(lambda P: len(P) <= 10), '%P')
        self._name_entry = Entry(entry_inner, textvariable=self.project_name_var,
                                 bg='#F8FAFC', fg=COLORS['text'],
                                 relief='flat', bd=0, highlightthickness=0,
                                 insertbackground=COLORS['text'], font=('Arial', 11),
                                 width=14, validate='key', validatecommand=vcmd)
        self._name_entry.pack(padx=6, ipady=4)

        self._char_count = Label(right, text='0/10', bg=COLORS['card_bg'],
                                 fg='#94A3B8', font=('Arial', 9))
        self._char_count.pack(side=LEFT, padx=(6, 0))

        self._name_error = Label(self._body, text='', fg=COLORS['error'],
                                 bg=COLORS['card_bg'], font=('Arial', 9))
        self._name_error.pack(anchor=W, padx=14)

    def _create_file_field(self):
        right = self._row('CSV file')

        self._file_label = Label(right, text='No file selected', fg=COLORS['subtitle'],
                                 bg=COLORS['card_bg'], font=('Arial', 10), anchor=E)
        self._file_label.pack(side=LEFT, fill=X, expand=True)

        CustomButton(right, text='Browse', font_size=10, variant='secondary',
                     command=self._select_file).pack(side=RIGHT, padx=(8, 0))

    def _create_model_file_field(self):
        right = self._row('Model file (.pkl)')

        self._model_label = Label(right, text='No model file selected', fg=COLORS['subtitle'],
                                  bg=COLORS['card_bg'], font=('Arial', 10), anchor=E)
        self._model_label.pack(side=LEFT, fill=X, expand=True)

        CustomButton(right, text='Browse', font_size=10, variant='secondary',
                     command=self._select_model_file).pack(side=RIGHT, padx=(8, 0))

    def _create_directory_field(self):
        right = self._row('Models directory')

        self._dir_label = Label(right, text='No folder selected', fg=COLORS['subtitle'],
                                bg=COLORS['card_bg'], font=('Arial', 10), anchor=E)
        self._dir_label.pack(side=LEFT, fill=X, expand=True)

        CustomButton(right, text='Browse', font_size=10, variant='secondary',
                     command=self._select_directory).pack(side=RIGHT, padx=(8, 0))

    def _create_test_size_field(self):
        right = self._row('Test size  (0.1–0.9)')

        sb = Spinbox(right, format='%.1f', increment=0.1, from_=0.1, to=0.9,
                     wrap=True, width=6, bg='#F8FAFC', fg=COLORS['text'],
                     textvariable=self.test_size,
                     highlightthickness=1, highlightbackground=COLORS['border'],
                     highlightcolor=COLORS['border'], font=('Arial', 11))
        sb.pack(side=RIGHT, ipady=4)
        sb.delete(0, 'end')
        sb.insert(0, '0.3')

    def _on_name_changed(self, *args):
        if not hasattr(self, '_name_error') or not self._name_error.winfo_exists():
            return
        val = self.project_name_var.get()
        count = len(val)

        if hasattr(self, '_char_count') and self._char_count.winfo_exists():
            self._char_count.config(text=f'{count}/10')

        if count > 10:
            self._name_error.config(text='Max 10 characters.')
        elif check_project_exists(val) and count >= 5:
            self._name_error.config(text='Project name already exists.')
        else:
            self._name_error.config(text='')

        self.update_callback()

    def _validate_csv(self, file_path):
        numeric_cols = ["M", "F", "L", "I", "V", "S", "P", "T", "A", "Y",
                        "H", "Q", "N", "K", "D", "E", "C", "W", "R", "G"]
        required = numeric_cols if self.analyse_type == 'Prediction' else numeric_cols + ["Product Name"]
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames != required:
                return False
            for row in reader:
                for col in numeric_cols:
                    try:
                        if int(row[col]) < 0:
                            return False
                    except ValueError:
                        return False
        return True

    def _select_file(self):
        path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')], title='Select a CSV file')
        if path:
            if self._validate_csv(path):
                self._file_label.config(text=f'✓ {os.path.basename(path)}', fg=COLORS['success'])
                self.file_path_var.set(path)
            else:
                self._file_label.config(text='Invalid CSV structure.', fg=COLORS['error'])
                self.file_path_var.set('')
        else:
            self._file_label.config(text='No file selected', fg=COLORS['subtitle'])
            self.file_path_var.set('')
        self.update_callback()

    def _select_model_file(self):
        path = filedialog.askopenfilename(filetypes=[('Model files', '*.pkl')], title='Select model file')
        if path:
            self._model_label.config(text=f'✓ {os.path.basename(path)}', fg=COLORS['success'])
            self.model_file_path_var.set(path)
        else:
            self._model_label.config(text='No model file selected', fg=COLORS['subtitle'])
            self.model_file_path_var.set('')
        self.update_callback()

    def _select_directory(self):
        path = filedialog.askdirectory(title='Select models directory')
        if path:
            if [f for f in os.listdir(path) if f.endswith('.pkl')]:
                self._dir_label.config(text=f'✓ {os.path.basename(path)}', fg=COLORS['success'])
                self.directory_var.set(path)
            else:
                self._dir_label.config(text='No .pkl files found.', fg=COLORS['error'])
                self.directory_var.set('')
        self.update_callback()