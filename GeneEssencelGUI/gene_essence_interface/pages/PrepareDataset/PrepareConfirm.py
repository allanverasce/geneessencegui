from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.PrepareDataset.PrepareDatasetSidebar import PrepareDatasetSidebar
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.RoundedCard import RoundedCard

BG = COLORS['background_alt']
_SEP = '#F1F5F9'


def _row(parent, key, value, is_last=False):
    if not value or str(value).strip() in ('N/A', 'None', ''):
        return
    row = Frame(parent, bg=COLORS['card_bg'])
    row.pack(fill=X, pady=0)
    Label(row, text=key, bg=COLORS['card_bg'], fg='#64748B',
          font=('Arial', 11), anchor=W).pack(side=LEFT, pady=7)
    Label(row, text=str(value), bg=COLORS['card_bg'], fg='#1A2332',
          font=('Arial', 11, 'bold'), anchor=E, wraplength=280,
          justify=RIGHT).pack(side=RIGHT, pady=7)
    if not is_last:
        Frame(parent, bg=_SEP, height=1).pack(fill=X)


class PrepareConfirm(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        sidebar = PrepareDatasetSidebar(self)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.set_active_step(1)

        self._content = Frame(self, bg=BG)
        self._content.pack(side=RIGHT, fill=BOTH, expand=True)

        btn_frame = Frame(self._content, bg=BG)
        btn_frame.pack(side=BOTTOM, fill=X, padx=20, pady=12)
        Frame(self._content, bg=COLORS['border'], height=1).pack(side=BOTTOM, fill=X)

        CustomButton(btn_frame, text='CONFIRM AND RUN', variant='success',
                     command=self._run).pack(side=RIGHT)
        CustomButton(btn_frame, text='← BACK', variant='secondary',
                     command=self.controller.go_back).pack(side=RIGHT, padx=(0, 8))

        title_area = Frame(self._content, bg=BG)
        title_area.pack(fill=X, padx=20, pady=(20, 0))
        Label(title_area, text='Confirm information',
              bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold')).pack(anchor=W)

        self._cards_area = Frame(self._content, bg=BG)
        self._cards_area.pack(fill=BOTH, expand=True, padx=20, pady=12)

        self.bind('<Visibility>', self._on_visible)

    def _on_visible(self, _):
        for w in self._cards_area.winfo_children():
            w.destroy()
        self._render_cards()

    def _render_cards(self):
        ctrl = self.controller
        params = ctrl.get_prepare_params() or {}
        mode = params.get('mode', '').capitalize()

        card = RoundedCard(self._cards_area)
        card.pack(fill=X)
        body = Frame(card._body, bg=COLORS['card_bg'])
        body.pack(fill=X, padx=14, pady=2)

        rows = [('Mode', mode)]
        if params.get('annotation'):
            rows.append(('DEG annotation', params['annotation']))
        if params.get('fasta'):
            rows.append(('FASTA file', params['fasta']))
        if params.get('genbank'):
            rows.append(('GenBank directory', params['genbank']))

        for i, (key, val) in enumerate(rows):
            _row(body, key, val, is_last=(i == len(rows) - 1))

    def _run(self):
        self.controller.show_page('RunPreparation')
