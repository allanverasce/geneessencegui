from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.RoundedCard import RoundedCard


class CardOption(RoundedCard):
    """Radio-style card with title and description. Binds to a StringVar."""

    def __init__(self, parent, title, description, value, variable, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.value = value
        self.variable = variable
        self.command = command

        self.configure(cursor='hand2')
        self._body.configure(cursor='hand2')

        self._accent = Canvas(self._body, width=3, height=1, highlightthickness=0,
                              bg=COLORS['card_bg'], cursor='hand2')
        self._accent.pack(side=LEFT, fill=Y)

        self.dot_canvas = Canvas(self._body, width=16, height=16,
                                 bg=COLORS['card_bg'], highlightthickness=0)
        self.dot_canvas.pack(side=LEFT, padx=(12, 10), pady=12)

        text_frame = Frame(self._body, bg=COLORS['card_bg'])
        text_frame.pack(side=LEFT, fill=BOTH, expand=True, pady=10, padx=(0, 12))

        self.title_lbl = Label(text_frame, text=title, bg=COLORS['card_bg'],
                               fg=COLORS['text'], font=('Arial', 13, 'bold'), anchor=W)
        self.title_lbl.pack(fill=X)

        self.desc_lbl = Label(text_frame, text=description, bg=COLORS['card_bg'],
                              fg=COLORS['subtitle'], font=('Arial', 11),
                              wraplength=480, justify=LEFT, anchor=W)
        self.desc_lbl.pack(fill=X)

        for w in (self, self._body, self._accent, self.dot_canvas,
                  text_frame, self.title_lbl, self.desc_lbl):
            w.bind('<Button-1>', self._on_click)
            w.bind('<Enter>', self._on_hover)
            w.bind('<Leave>', self._on_leave)

        variable.trace_add('write', self._update_display)
        self._update_display()

    def _on_click(self, event=None):
        self.variable.set(self.value)
        if self.command:
            self.command()

    def _on_hover(self, event=None):
        if self.variable.get() != self.value:
            self.set_card_style(COLORS['card_hover_bg'], COLORS['card_hover_border'])

    def _on_leave(self, event=None):
        x, y = self.winfo_pointerxy()
        wx, wy = self.winfo_rootx(), self.winfo_rooty()
        ww, wh = self.winfo_width(), self.winfo_height()
        if not (wx <= x <= wx + ww and wy <= y <= wy + wh):
            self._update_display()

    def _update_display(self, *args):
        selected = self.variable.get() == self.value
        bg = COLORS['card_selected_bg'] if selected else COLORS['card_bg']
        border = COLORS['card_selected_border'] if selected else COLORS['card_border']

        self.set_card_style(bg, border)

        # set_card_style → update_bg resets all child bgs; restore accent colour after
        self._accent.configure(bg=COLORS['primary'] if selected else bg)

        self.dot_canvas.delete('all')
        dot_border = COLORS['primary'] if selected else '#CBD5E1'
        self.dot_canvas.create_oval(1, 1, 15, 15, outline=dot_border, width=2)
        if selected:
            self.dot_canvas.create_oval(5, 5, 11, 11, fill=COLORS['primary'], outline='')
