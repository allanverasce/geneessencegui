from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.RoundedCard import RoundedCard
from gene_essence_interface.pages.components.canvas_utils import rounded_rect


class CheckCard(RoundedCard):
    """Checkbox-style card with title and optional subtitle. right_slot for extra widgets."""

    def __init__(self, parent, title, subtitle='', variable=None, on_toggle=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.variable = variable if variable is not None else BooleanVar()
        self.on_toggle = on_toggle

        self.configure(cursor='hand2')
        self._body.configure(cursor='hand2')

        self.cb_canvas = Canvas(self._body, width=16, height=16,
                                bg=COLORS['card_bg'], highlightthickness=0)
        self.cb_canvas.pack(side=LEFT, padx=(10, 8), pady=10)

        self._text_frame = Frame(self._body, bg=COLORS['card_bg'])
        self._text_frame.pack(side=LEFT, fill=BOTH, expand=True, pady=8)

        self.title_lbl = Label(self._text_frame, text=title, bg=COLORS['card_bg'],
                               fg=COLORS['text'], font=('Arial', 11), anchor=W)
        self.title_lbl.pack(fill=X)

        if subtitle:
            self.sub_lbl = Label(self._text_frame, text=subtitle, bg=COLORS['card_bg'],
                                 fg=COLORS['subtitle'], font=('Arial', 9), anchor=W,
                                 justify=LEFT, wraplength=200)
            self.sub_lbl.pack(fill=X)
            self._text_frame.bind('<Configure>', self._update_wraplength)
        else:
            self.sub_lbl = None

        self.right_slot = Frame(self._body, bg=COLORS['card_bg'])
        self.right_slot.pack(side=RIGHT, padx=6)

        for w in (self, self._body, self.cb_canvas, self._text_frame, self.title_lbl):
            w.bind('<Button-1>', self._on_click)
            w.bind('<Enter>', self._on_hover)
            w.bind('<Leave>', self._on_leave)

        self.variable.trace_add('write', self._update_display)
        self._update_display()

    def _update_wraplength(self, event):
        if self.sub_lbl:
            self.sub_lbl.config(wraplength=max(40, event.width - 4))

    def _on_click(self, event=None):
        self.variable.set(not self.variable.get())
        if self.on_toggle:
            self.on_toggle()

    def _on_hover(self, event=None):
        if not self.variable.get():
            self.set_card_style(COLORS['card_hover_bg'], COLORS['card_hover_border'])

    def _on_leave(self, event=None):
        x, y = self.winfo_pointerxy()
        wx, wy = self.winfo_rootx(), self.winfo_rooty()
        ww, wh = self.winfo_width(), self.winfo_height()
        if not (wx <= x <= wx + ww and wy <= y <= wy + wh):
            self._update_display()

    def _update_display(self, *args):
        checked = self.variable.get()
        bg = COLORS['card_selected_bg'] if checked else COLORS['card_bg']
        border = COLORS['card_selected_border'] if checked else COLORS['card_border']

        self.set_card_style(bg, border)

        self.cb_canvas.delete('all')
        if checked:
            rounded_rect(self.cb_canvas, 0, 0, 16, 16, 4,
                         fill=COLORS['primary'], outline=COLORS['primary'])
            self.cb_canvas.create_text(8, 8, text='✓', fill='white',
                                       font=('Arial', 10, 'bold'))
        else:
            rounded_rect(self.cb_canvas, 1, 1, 15, 15, 4,
                         fill='white', outline='#CBD5E1', width=2)