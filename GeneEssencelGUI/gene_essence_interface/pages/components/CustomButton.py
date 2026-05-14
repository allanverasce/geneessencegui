import tkinter.font as tkfont
from tkinter import Canvas, NORMAL, DISABLED

from gene_essence_interface.config.colors import COLORS

_BASE_PADX = 28
_BASE_PADY = 10
_RADIUS    = 8   # border-radius equivalente ao CSS

_VARIANTS = {
    'primary': {
        'bg':                '#63C2D1',
        'fg':                '#FFFFFF',
        'disabledforeground': '#DCF0F5',
        'border':            '',
        'border_width':      0,
        '_hover_bg':         '#4DB8C9',
        '_leave_bg':         '#63C2D1',
    },
    'secondary': {
        'bg':                '#F7F8FA',
        'fg':                '#64748B',
        'disabledforeground': '#CBD5E1',
        'border':            '#CBD5E1',
        'border_width':      1,
        '_hover_bg':         '#F0FBFC',
        '_leave_bg':         '#F7F8FA',
        '_hover_border':     '#63C2D1',
        '_leave_border':     '#CBD5E1',
    },
    'success': {
        'bg':                '#047857',
        'fg':                '#FFFFFF',
        'disabledforeground': '#DCF0F5',
        'border':            '',
        'border_width':      0,
        '_hover_bg':         '#065F46',
        '_leave_bg':         '#047857',
    },
    'danger': {
        'bg':                '#FEF2F2',
        'fg':                '#DC2626',
        'disabledforeground': '#CBD5E1',
        'border':            '#FCA5A5',
        'border_width':      1,
        '_hover_bg':         '#FEE2E2',
        '_leave_bg':         '#FEF2F2',
        '_hover_border':     '#DC2626',
        '_leave_border':     '#FCA5A5',
    },
}


def _rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    """Desenha retângulo com cantos arredondados no Canvas."""
    points = [
        x1 + r, y1,   x2 - r, y1,
        x2,     y1,   x2,     y1 + r,
        x2,     y2 - r, x2,   y2,
        x2 - r, y2,   x1 + r, y2,
        x1,     y2,   x1,     y2 - r,
        x1,     y1 + r, x1,   y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kw)


class CustomButton(Canvas):
    """Botão baseado em Canvas — cor garantida em todas as plataformas + border-radius."""

    def __init__(self, parent, text='', font_size=12, bg=None,
                 fg=None, cursor='hand2', variant=None,
                 command=None, state=NORMAL, **kwargs):

        v = _VARIANTS.get(variant, _VARIANTS['primary']) if variant else _VARIANTS['primary']

        self._bg           = bg if bg is not None else v['bg']
        self._fg           = fg if fg is not None else v['fg']
        self._dis_fg       = v.get('disabledforeground', '#CBD5E1')
        self._hover_bg     = v.get('_hover_bg',     self._bg)
        self._leave_bg     = v.get('_leave_bg',     self._bg)
        self._border       = v.get('border',        '')
        self._border_w     = v.get('border_width',  0)
        self._hover_border = v.get('_hover_border', self._border)
        self._leave_border = v.get('_leave_border', self._border)
        self._cur_border   = self._border
        self._cur_bg       = self._bg
        self._command      = command
        self._state        = str(state)
        self._text         = text

        # Mede o texto para calcular o tamanho do canvas
        padx = kwargs.pop('padx', _BASE_PADX)
        pady = kwargs.pop('pady', _BASE_PADY)
        self._font = tkfont.Font(family='Arial', size=font_size, weight='bold')
        tw = self._font.measure(text)
        th = self._font.metrics('linespace')
        w  = tw + 2 * padx
        h  = th + 2 * pady

        # Canvas bg = bg do parent para que os cantos arredondados pareçam recortados
        try:
            parent_bg = parent.cget('bg')
        except Exception:
            parent_bg = COLORS['background_alt']

        # Remove kwargs incompatíveis com Canvas
        for key in ('relief', 'bd', 'activebackground', 'activeforeground',
                    'disabledforeground', 'highlightcolor', 'borderless',
                    'highlightthickness', 'highlightbackground', 'overrelief',
                    'insertbackground'):
            kwargs.pop(key, None)

        super().__init__(parent, width=w, height=h,
                         bg=parent_bg,
                         highlightthickness=0,
                         cursor=cursor if self._state != 'disabled' else 'arrow',
                         **kwargs)

        self._redraw()

        if self._state != 'disabled':
            self._bind_events()

    # ── Desenho ───────────────────────────────────────────────────────────────

    def _redraw(self):
        self.delete('all')
        w = int(self['width'])
        h = int(self['height'])
        bg  = self._cur_bg
        fg  = self._fg if self._state != 'disabled' else self._dis_fg
        brd = self._cur_border
        bw  = self._border_w

        outline = brd if bw > 0 else ''
        _rounded_rect(self, 1, 1, w - 1, h - 1, _RADIUS,
                      fill=bg, outline=outline, width=bw)
        self.create_text(w // 2, h // 2, text=self._text, fill=fg, font=self._font)

    def _set_colors(self, bg, border=None):
        self._cur_bg = bg
        if border is not None:
            self._cur_border = border
        self._redraw()

    # ── Eventos ───────────────────────────────────────────────────────────────

    def _bind_events(self):
        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>',    self._on_enter)
        self.bind('<Leave>',    self._on_leave)

    def _unbind_events(self):
        self.unbind('<Button-1>')
        self.unbind('<Enter>')
        self.unbind('<Leave>')

    def _on_click(self, e=None):
        if self._state != 'disabled' and self._command:
            self._command()

    def _on_enter(self, e=None):
        if self._state == 'disabled':
            return
        self._set_colors(self._hover_bg, self._hover_border or None)

    def _on_leave(self, e=None):
        if self._state == 'disabled':
            return
        self._set_colors(self._leave_bg, self._leave_border or None)

    # ── API pública (espelha tkinter.Button) ──────────────────────────────────

    def config(self, **kw):
        if 'state' in kw:
            new_state = str(kw.pop('state'))
            if new_state != self._state:
                self._state = new_state
                if new_state == 'disabled':
                    Canvas.config(self, cursor='arrow')
                    self._cur_bg     = self._bg
                    self._cur_border = self._border
                    self._unbind_events()
                else:
                    Canvas.config(self, cursor='hand2')
                    self._bind_events()
                self._redraw()

        if 'bg' in kw:
            self._cur_bg = self._bg = kw.pop('bg')
            self._redraw()

        if 'text' in kw:
            self._text = kw.pop('text')
            self._redraw()

        if kw:
            try:
                Canvas.config(self, **kw)
            except Exception:
                pass

    configure = config

    def cget(self, key):
        if key == 'state':
            return self._state
        if key == 'text':
            return self._text
        return Canvas.cget(self, key)
