import csv
import os
from tkinter import *
from tkinter import filedialog

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.PrepareDataset.PrepareDatasetSidebar import PrepareDatasetSidebar
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.RoundedCard import RoundedCard

BG = COLORS['background_alt']


class _ModeCard(RoundedCard):
    def __init__(self, parent, radio_var, value, title, subtitle, **kwargs):
        super().__init__(parent, **kwargs)
        self.radio_var = radio_var
        self.value = value

        self.configure(cursor='hand2')
        self._body.configure(cursor='hand2')

        top = Frame(self._body, bg=COLORS['card_bg'], cursor='hand2')
        top.pack(fill=X, padx=12, pady=(10, 0))

        self.dot = Canvas(top, width=16, height=16,
                          bg=COLORS['card_bg'], highlightthickness=0)
        self.dot.pack(side=LEFT, padx=(0, 10))

        text_f = Frame(top, bg=COLORS['card_bg'], cursor='hand2')
        text_f.pack(side=LEFT, fill=X, expand=True)
        Label(text_f, text=title, bg=COLORS['card_bg'],
              fg=COLORS['text'], font=('Arial', 12, 'bold')).pack(anchor=W)

        Label(self._body, text=subtitle, bg=COLORS['card_bg'],
              fg=COLORS['subtitle'], font=('Arial', 10)).pack(anchor=W, padx=14, pady=(4, 0))

        self.input_area = Frame(self._body, bg=COLORS['card_bg'])

        for w in (self, self._body, top, text_f, self.dot):
            w.bind('<Button-1>', self._select)

        radio_var.trace_add('write', self._update_display)
        self._update_display()

    def _select(self, _=None):
        self.radio_var.set(self.value)

    def _update_display(self, *_):
        selected = self.radio_var.get() == self.value
        bg = COLORS['card_selected_bg'] if selected else COLORS['card_bg']
        border = COLORS['card_selected_border'] if selected else COLORS['card_border']
        self.set_card_style(bg, border)

        self.dot.delete('all')
        color = COLORS['primary'] if selected else '#CBD5E1'
        self.dot.create_oval(1, 1, 15, 15, outline=color, width=2)
        if selected:
            self.dot.create_oval(5, 5, 11, 11, fill=COLORS['primary'], outline='')

        if selected:
            self.input_area.pack(fill=X, padx=12, pady=(8, 10))
        else:
            self.input_area.pack_forget()


class PrepareDataset(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.radio_var = StringVar(value='training')

        self._annotation_var = StringVar()
        self._fasta_var = StringVar()
        self._genbank_train_var = StringVar()
        self._genbank_pred_var = StringVar()

        sidebar = PrepareDatasetSidebar(self)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.set_active_step(0)

        self._right = Frame(self, bg=BG)
        self._right.pack(side=RIGHT, fill=BOTH, expand=True)

        self._build()

    def _build(self):
        btn_frame = Frame(self._right, bg=BG)
        btn_frame.pack(side=BOTTOM, fill=X, padx=20, pady=12)
        Frame(self._right, bg=COLORS['border'], height=1).pack(side=BOTTOM, fill=X)

        self._run_btn = CustomButton(btn_frame, text='NEXT →', variant='primary',
                                     state=DISABLED, command=self._proceed)
        self._run_btn.pack(side=RIGHT)
        CustomButton(btn_frame, text='← BACK', variant='secondary',
                     command=self.controller.go_back).pack(side=RIGHT, padx=(0, 8))

        title_area = Frame(self._right, bg=BG)
        title_area.pack(fill=X, padx=20, pady=(20, 0))
        Label(title_area, text='Prepare Dataset',
              bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold')).pack(anchor=W)
        Label(title_area, text='Generate the input files required for analysis using the RNA preparation module.',
              bg=BG, fg=COLORS['subtitle'], font=('Arial', 11)).pack(anchor=W, pady=(4, 0))

        cards = Frame(self._right, bg=BG)
        cards.pack(fill=X, padx=20, pady=14)

        for var in (self.radio_var, self._annotation_var, self._fasta_var,
                    self._genbank_train_var, self._genbank_pred_var):
            var.trace_add('write', self._update_run_btn)

        self._training_card = _ModeCard(
            cards, self.radio_var, 'training',
            'Training Dataset',
            'Generates CSV files for model training using annotation, FASTA and GenBank data.'
        )
        self._training_card.pack(fill=X, pady=(0, 10))
        self._build_training_inputs(self._training_card.input_area)

        self._pred_card = _ModeCard(
            cards, self.radio_var, 'prediction',
            'Prediction Dataset',
            'Generates the input file for prediction using GenBank files only.'
        )
        self._pred_card.pack(fill=X)
        self._build_prediction_inputs(self._pred_card.input_area)

    # ── Input builders ────────────────────────────────────────────────────────

    def _file_row(self, parent, label_text, placeholder, browse_cmd):
        row = Frame(parent, bg=COLORS['card_bg'])
        row.pack(fill=X, pady=(0, 6))
        Label(row, text=label_text, bg=COLORS['card_bg'], fg=COLORS['subtitle'],
              font=('Arial', 10), width=22, anchor=W).pack(side=LEFT)

        wrap = Frame(row, bg=COLORS['border'])
        wrap.pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
        inner = Frame(wrap, bg='#F7F8FA')
        inner.pack(fill=X, padx=1, pady=1)
        lbl = Label(inner, text=placeholder, bg='#F7F8FA', fg=COLORS['subtitle'],
                    font=('Arial', 10), anchor=W)
        lbl.pack(fill=X, ipady=4, padx=6)

        CustomButton(row, text='Browse…', font_size=10, variant='secondary',
                     command=browse_cmd).pack(side=RIGHT)
        return lbl

    def _build_training_inputs(self, parent):
        self._annotation_lbl = self._file_row(
            parent, 'DEG annotation (.csv)', 'No file selected',
            lambda: self._browse_annotation())
        self._fasta_lbl = self._file_row(
            parent, 'FASTA file (.fasta/.aa)', 'No file selected',
            lambda: self._browse_fasta())
        self._genbank_train_lbl = self._file_row(
            parent, 'GenBank directory', 'No folder selected',
            lambda: self._browse_genbank(self._genbank_train_var, self._genbank_train_lbl))

    def _build_prediction_inputs(self, parent):
        self._genbank_pred_lbl = self._file_row(
            parent, 'GenBank directory', 'No folder selected',
            lambda: self._browse_genbank(self._genbank_pred_var, self._genbank_pred_lbl))

    # ── Validation ────────────────────────────────────────────────────────────

    def _validate_csv(self, path):
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                row = next(reader, None)
                return row is not None and len(row) >= 13
        except Exception:
            return False

    def _validate_fasta(self, path):
        try:
            with open(path, encoding='utf-8', errors='ignore') as f:
                return f.readline().startswith('>')
        except Exception:
            return False

    def _validate_genbank_dir(self, path):
        try:
            for name in os.listdir(path):
                fpath = os.path.join(path, name)
                if not os.path.isfile(fpath):
                    continue
                try:
                    with open(fpath, encoding='utf-8', errors='ignore') as f:
                        if f.readline().startswith('LOCUS'):
                            return True
                except Exception:
                    continue
            return False
        except Exception:
            return False

    # ── Browse helpers ────────────────────────────────────────────────────────

    def _browse_annotation(self):
        path = filedialog.askopenfilename(
            filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
        if not path:
            return
        if self._validate_csv(path):
            self._annotation_lbl.config(
                text=f'✓ {os.path.basename(path)}', fg=COLORS['success'])
            self._annotation_var.set(path)
        else:
            self._annotation_lbl.config(
                text='Invalid CSV file.', fg=COLORS['error'])
            self._annotation_var.set('')

    def _browse_fasta(self):
        path = filedialog.askopenfilename(
            filetypes=[('FASTA files', '*.fasta *.fa *.aa'), ('All files', '*.*')])
        if not path:
            return
        if self._validate_fasta(path):
            self._fasta_lbl.config(
                text=f'✓ {os.path.basename(path)}', fg=COLORS['success'])
            self._fasta_var.set(path)
        else:
            self._fasta_lbl.config(
                text='Invalid FASTA file.', fg=COLORS['error'])
            self._fasta_var.set('')

    def _browse_genbank(self, var, lbl):
        path = filedialog.askdirectory()
        if not path:
            return
        if self._validate_genbank_dir(path):
            lbl.config(text=f'✓ {os.path.basename(path)}', fg=COLORS['success'])
            var.set(path)
        else:
            lbl.config(text='No .gb/.gbk files found.', fg=COLORS['error'])
            var.set('')

    # ── Button state ──────────────────────────────────────────────────────────

    def _update_run_btn(self, *_):
        mode = self.radio_var.get()
        if mode == 'training':
            valid = (self._annotation_var.get() and
                     self._fasta_var.get() and
                     self._genbank_train_var.get())
        else:
            valid = bool(self._genbank_pred_var.get())
        self._run_btn.config(state=NORMAL if valid else DISABLED)

    # ── Proceed ───────────────────────────────────────────────────────────────

    def _proceed(self):
        mode = self.radio_var.get()
        if mode == 'training':
            params = {
                'mode': 'training',
                'annotation': self._annotation_var.get(),
                'fasta': self._fasta_var.get(),
                'genbank': self._genbank_train_var.get(),
            }
        else:
            params = {
                'mode': 'prediction',
                'genbank': self._genbank_pred_var.get(),
            }
        self.controller.set_prepare_params(params)
        self.controller.show_page('RunPreparation')
