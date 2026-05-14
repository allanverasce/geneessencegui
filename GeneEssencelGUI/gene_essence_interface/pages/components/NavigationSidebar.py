from tkinter import *
from PIL import Image, ImageTk

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.canvas_utils import rounded_rect
from gene_essence_interface.utils import resource_path

STEPS_BY_TYPE = {
    'Training':   ["Analysis Type", "Project Info", "Select Models", "Select Metrics", "Delivery", "Confirm", "Running"],
    'Prediction': ["Analysis Type", "Project Info", "Delivery", "Confirm", "Running"],
    'Ensemble':   ["Analysis Type", "Project Info", "Select Metrics", "Delivery", "Confirm", "Running"],
}

STEP_INDEX_BY_TYPE = {
    'Training': {
        'ChooseAnalysisType': 0, 'InformationProject': 1, 'ChooseModels': 2,
        'ChooseMetrics': 3, 'ChooseHowToReceiveTheResults': 4,
        'ConfirmInformationFrame': 5, 'RunAnalysis': 6,
    },
    'Prediction': {
        'ChooseAnalysisType': 0, 'InformationProject': 1,
        'ChooseHowToReceiveTheResults': 2, 'ConfirmInformationFrame': 3, 'RunAnalysis': 4,
    },
    'Ensemble': {
        'ChooseAnalysisType': 0, 'InformationProject': 1, 'ChooseMetrics': 2,
        'ChooseHowToReceiveTheResults': 3, 'ConfirmInformationFrame': 4, 'RunAnalysis': 5,
    },
}

STEPS = STEPS_BY_TYPE['Training']

PARTNERS = ["UFPA", "ENGBIO"]
_PILL_BG = '#243447'
_PILL_FG = '#9AA5B4'


def build_partners_footer(parent, sidebar_bg):
    """Rodapé de parceiros reutilizável na sidebar e na StartPage."""
    bottom = Frame(parent, bg=sidebar_bg)
    bottom.pack(side=BOTTOM, fill=X, padx=14, pady=14)

    Frame(parent, bg=COLORS['sidebar_divider'], height=1).pack(side=BOTTOM, fill=X)

    Label(bottom, text='PARTNERS', bg=sidebar_bg, fg=COLORS['sidebar_steps_label'],
          font=('Arial', 10, 'bold')).pack(anchor=CENTER, pady=(0, 6))

    pills_row = Frame(bottom, bg=sidebar_bg)
    pills_row.pack(anchor=CENTER)
    for name in PARTNERS:
        Label(pills_row, text=name, bg=_PILL_BG, fg=_PILL_FG,
              font=('Arial', 9), padx=7, pady=2).pack(side=LEFT, padx=(0, 4))


class NavigationSidebar(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['sidebar_bg'], width=200, **kwargs)
        self.pack_propagate(False)
        self._rows = []
        build_partners_footer(self, COLORS['sidebar_bg'])  # packed first → fica no bottom
        self._build_logo()
        self._build_divider()
        self._build_steps_label()
        self._build_steps()

    def _build_logo(self):
        f = Frame(self, bg=COLORS['sidebar_bg'])
        f.pack(fill=X, padx=14, pady=(20, 8))

        sidebar_hex = COLORS['sidebar_bg'].lstrip('#')
        sidebar_rgb = tuple(int(sidebar_hex[i:i+2], 16) for i in (0, 2, 4))
        raw = Image.open(resource_path("assets/gene_essence_logo.png")).resize((42, 42), Image.LANCZOS).convert('RGBA')
        bg = Image.new('RGBA', raw.size, sidebar_rgb + (255,))
        bg.paste(raw, mask=raw.split()[3])
        self._logo_img = ImageTk.PhotoImage(bg.convert('RGB'))
        Label(f, image=self._logo_img, bg=COLORS['sidebar_bg']).pack(anchor=CENTER, pady=(0, 6))

        Label(f, text='GeneEssenceGUI', bg=COLORS['sidebar_bg'],
              fg=COLORS['primary'], font=('Arial', 12, 'bold')).pack()
        Label(f, text='Integrating DEG and NCBI datasets through ensemble machine learning for essential gene prediction',
              bg=COLORS['sidebar_bg'], fg='#9AA5B4',
              font=('Arial', 10), wraplength=162, justify=CENTER).pack(pady=(4, 0))

    def _build_divider(self):
        Frame(self, bg=COLORS['sidebar_divider'], height=1).pack(fill=X, padx=12, pady=(8, 0))

    def _build_steps_label(self):
        Label(self, text='STEPS', bg=COLORS['sidebar_bg'],
              fg=COLORS['sidebar_steps_label'],
              font=('Arial', 10, 'bold')).pack(anchor=W, padx=14, pady=(6, 4))

    def _build_step_row(self, i, name):
        row_frame = Frame(self, bg=COLORS['sidebar_bg'])
        row_frame.pack(fill=X)
        accent = Frame(row_frame, width=3, bg=COLORS['sidebar_bg'])
        accent.pack(side=LEFT, fill=Y)
        badge_c = Canvas(row_frame, width=20, height=20,
                         bg=COLORS['sidebar_bg'], highlightthickness=0)
        badge_c.pack(side=LEFT, padx=(14, 7), pady=7)
        lbl = Label(row_frame, text=name, bg=COLORS['sidebar_bg'],
                    fg=COLORS['sidebar_text_muted'], font=('Arial', 10))
        lbl.pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
        return {'frame': row_frame, 'accent': accent, 'badge': badge_c, 'label': lbl, 'num': i + 1}

    def _build_steps(self):
        for i, name in enumerate(STEPS):
            self._rows.append(self._build_step_row(i, name))
        for row in self._rows:
            self._set_pending(row)

    def reset_steps(self, steps):
        for row in self._rows:
            row['frame'].destroy()
        self._rows.clear()
        for i, name in enumerate(steps):
            self._rows.append(self._build_step_row(i, name))
        for row in self._rows:
            self._set_pending(row)

    def _set_done(self, row):
        bg = COLORS['sidebar_bg']
        row['frame'].config(bg=bg)
        row['accent'].config(bg=bg)
        row['badge'].config(bg=bg)
        row['badge'].delete('all')
        rounded_rect(row['badge'], 0, 0, 20, 20, 4, fill=COLORS['sidebar_step_done_badge'], outline='')
        row['badge'].create_text(10, 10, text=str(row['num']), fill='white', font=('Arial', 9, 'bold'))
        row['label'].config(fg='#9AA5B4', bg=bg, font=('Arial', 10))

    def _set_active(self, row):
        bg = COLORS['sidebar_step_active_bg']
        row['frame'].config(bg=bg)
        row['accent'].config(bg=COLORS['primary'])
        row['badge'].config(bg=bg)
        row['badge'].delete('all')
        rounded_rect(row['badge'], 0, 0, 20, 20, 4, fill=COLORS['primary'], outline='')
        row['badge'].create_text(10, 10, text=str(row['num']), fill='white', font=('Arial', 9, 'bold'))
        row['label'].config(fg='white', bg=bg, font=('Arial', 10, 'bold'))

    def _set_pending(self, row):
        bg = COLORS['sidebar_bg']
        row['frame'].config(bg=bg)
        row['accent'].config(bg=bg)
        row['badge'].config(bg=bg)
        row['badge'].delete('all')
        rounded_rect(row['badge'], 0, 0, 20, 20, 4, fill=COLORS['sidebar_step_pending_badge'], outline='')
        row['badge'].create_text(10, 10, text=str(row['num']),
                                 fill=COLORS['sidebar_text_muted'], font=('Arial', 9, 'bold'))
        row['label'].config(fg=COLORS['sidebar_text_muted'], bg=bg, font=('Arial', 10))

    def set_active_step(self, index):
        for i, row in enumerate(self._rows):
            if i < index:
                self._set_done(row)
            elif i == index:
                self._set_active(row)
            else:
                self._set_pending(row)