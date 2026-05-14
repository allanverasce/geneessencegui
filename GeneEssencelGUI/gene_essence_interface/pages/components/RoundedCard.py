from tkinter import Frame, Canvas, BOTH

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.canvas_utils import rounded_rect, update_bg


class RoundedCard(Frame):
    """
    Frame base com borda arredondada desenhada via Canvas.

    Filhos devem ser adicionados a self._body (não a self).
    Use set_card_style(bg, border) para mudar cores em hover/selected.
    """
    RADIUS = 8

    def __init__(self, parent,
                 card_bg=COLORS['card_bg'],
                 border=COLORS['card_border'],
                 border_width=1.5,
                 **kwargs):

        try:
            parent_bg = parent.cget('bg')
        except Exception:
            parent_bg = COLORS['background_alt']

        # Outer Frame é transparente (bg do parent) → cantos arredondados aparecem recortados
        super().__init__(parent, bg=parent_bg, **kwargs)

        self._card_bg    = card_bg
        self._cur_bg     = card_bg
        self._cur_border = border
        self._border_w   = border_width
        self._parent_bg  = parent_bg

        # Canvas que desenha o fundo arredondado (fica abaixo do body em z-order)
        self._bg_canvas = Canvas(self, bg=parent_bg, highlightthickness=0)
        self._bg_canvas.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        # Frame interno onde os filhos são adicionados
        # padx/pady deixa 2px visíveis para a borda arredondada aparecer
        self._body = Frame(self, bg=card_bg)
        self._body.pack(fill=BOTH, expand=True, padx=2, pady=2)

        # Garante que o body fique acima do canvas
        self._body.lift()

        self.bind('<Configure>', self._redraw)

    # ── Desenho ───────────────────────────────────────────────────────────────

    def _redraw(self, e=None):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 4 or h < 4:
            return
        self._bg_canvas.delete('all')
        bw = self._border_w
        rounded_rect(self._bg_canvas,
                     bw / 2, bw / 2, w - bw / 2, h - bw / 2,
                     self.RADIUS,
                     fill=self._cur_bg,
                     outline=self._cur_border if bw > 0 else '',
                     width=bw)

    # ── API pública ───────────────────────────────────────────────────────────

    def set_card_style(self, bg=None, border=None):
        """Atualiza cores do card e de todos os filhos internos."""
        if bg is not None:
            self._cur_bg = bg
            self._body.configure(bg=bg)
            update_bg(self._body, bg)
        if border is not None:
            self._cur_border = border
        self._redraw()

    def reset_card_style(self):
        self.set_card_style(self._card_bg, COLORS['card_border'])
