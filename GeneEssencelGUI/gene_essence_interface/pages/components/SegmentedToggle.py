from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.canvas_utils import rounded_rect


class SegmentedToggle(Canvas):
    """Toggle com dois segmentos, cantos arredondados via Canvas."""

    _H = 34
    _PAD = 3
    _R_OUTER = 8
    _R_INNER = 6

    def __init__(self, parent, variable, options, **kwargs):
        try:
            parent_bg = parent.cget('bg')
        except Exception:
            parent_bg = COLORS['background_alt']

        super().__init__(parent, bg=parent_bg, highlightthickness=0,
                         height=self._H, width=1, cursor='hand2', **kwargs)

        self.variable = variable
        self._segments = options  # [(label, value), ...]

        self.bind('<Configure>', self._redraw)
        self.bind('<Button-1>', self._on_click)
        variable.trace_add('write', lambda *_: self._safe_redraw())

    def _safe_redraw(self):
        try:
            if self.winfo_exists():
                self._redraw()
        except Exception:
            pass

    def _redraw(self, event=None):
        self.delete('all')
        w = self.winfo_width()
        h = self._H
        if w < 8:
            return

        p = self._PAD
        n = len(self._segments)
        btn_w = (w - p * (n + 1)) / n

        # Fundo do container arredondado
        rounded_rect(self, 0, 0, w, h, self._R_OUTER, fill='#F1F5F9', outline='')

        active = self.variable.get()

        for i, (label, value) in enumerate(self._segments):
            x1 = p + i * (btn_w + p)
            y1 = p
            x2 = x1 + btn_w
            y2 = h - p
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            if value == active:
                rounded_rect(self, x1, y1, x2, y2, self._R_INNER,
                             fill='white', outline='')
                self.create_text(cx, cy, text=label,
                                 fill='#1A2332', font=('Arial', 11, 'bold'))
            else:
                self.create_text(cx, cy, text=label,
                                 fill='#64748B', font=('Arial', 11, 'bold'))

    def _on_click(self, event):
        w = self.winfo_width()
        p = self._PAD
        n = len(self._segments)
        btn_w = (w - p * (n + 1)) / n

        for i, (_, value) in enumerate(self._segments):
            x1 = p + i * (btn_w + p)
            x2 = x1 + btn_w
            if x1 <= event.x <= x2:
                self.variable.set(value)
                break