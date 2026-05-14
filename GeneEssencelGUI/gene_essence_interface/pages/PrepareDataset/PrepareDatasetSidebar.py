from tkinter import *
from PIL import Image, ImageTk

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.canvas_utils import rounded_rect
from gene_essence_interface.pages.components.NavigationSidebar import build_partners_footer
from gene_essence_interface.utils.resource_path import resource_path

_STEPS = ["Input Files", "Running"]


class PrepareDatasetSidebar(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['sidebar_bg'], width=200, **kwargs)
        self.pack_propagate(False)
        self._rows = []

        build_partners_footer(self, COLORS['sidebar_bg'])
        self._build_header()
        Frame(self, bg=COLORS['sidebar_divider'], height=1).pack(fill=X, padx=12, pady=(8, 0))
        Label(self, text='STEPS', bg=COLORS['sidebar_bg'],
              fg=COLORS['sidebar_steps_label'],
              font=('Arial', 10, 'bold')).pack(anchor=W, padx=14, pady=(6, 4))
        self._build_steps()

    def _build_header(self):
        f = Frame(self, bg=COLORS['sidebar_bg'])
        f.pack(fill=X, padx=14, pady=(20, 8))

        sidebar_hex = COLORS['sidebar_bg'].lstrip('#')
        sidebar_rgb = tuple(int(sidebar_hex[i:i+2], 16) for i in (0, 2, 4))
        raw = Image.open(resource_path('assets/gene_essence_logo.png')).resize((42, 42), Image.LANCZOS).convert('RGBA')
        bg = Image.new('RGBA', raw.size, sidebar_rgb + (255,))
        bg.paste(raw, mask=raw.split()[3])
        self._logo_img = ImageTk.PhotoImage(bg.convert('RGB'))
        Label(f, image=self._logo_img, bg=COLORS['sidebar_bg']).pack(anchor=CENTER, pady=(0, 6))

        Label(f, text='GeneEssenceGUI', bg=COLORS['sidebar_bg'],
              fg=COLORS['primary'], font=('Arial', 12, 'bold')).pack()
        Label(f, text='Integrating DEG and NCBI datasets through ensemble machine learning for essential gene prediction',
              bg=COLORS['sidebar_bg'], fg='#9AA5B4',
              font=('Arial', 10), wraplength=162, justify=CENTER).pack(pady=(4, 0))

    def _build_steps(self):
        for i, name in enumerate(_STEPS):
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

            self._rows.append({
                'frame': row_frame, 'accent': accent,
                'badge': badge_c, 'label': lbl, 'num': i + 1
            })

        self._render(0)

    def set_active_step(self, index):
        self._render(index)

    def _render(self, active):
        for i, row in enumerate(self._rows):
            if i < active:
                self._done(row)
            elif i == active:
                self._active(row)
            else:
                self._pending(row)

    def _done(self, row):
        bg = COLORS['sidebar_bg']
        row['frame'].config(bg=bg)
        row['accent'].config(bg=bg)
        row['badge'].config(bg=bg)
        row['badge'].delete('all')
        rounded_rect(row['badge'], 0, 0, 20, 20, 4,
                     fill=COLORS['sidebar_step_done_badge'], outline='')
        row['badge'].create_text(10, 10, text=str(row['num']),
                                 fill='white', font=('Arial', 9, 'bold'))
        row['label'].config(fg='#9AA5B4', bg=bg, font=('Arial', 10))

    def _active(self, row):
        bg = COLORS['sidebar_step_active_bg']
        row['frame'].config(bg=bg)
        row['accent'].config(bg=COLORS['primary'])
        row['badge'].config(bg=bg)
        row['badge'].delete('all')
        rounded_rect(row['badge'], 0, 0, 20, 20, 4, fill=COLORS['primary'], outline='')
        row['badge'].create_text(10, 10, text=str(row['num']),
                                 fill='white', font=('Arial', 9, 'bold'))
        row['label'].config(fg='white', bg=bg, font=('Arial', 10, 'bold'))

    def _pending(self, row):
        bg = COLORS['sidebar_bg']
        row['frame'].config(bg=bg)
        row['accent'].config(bg=bg)
        row['badge'].config(bg=bg)
        row['badge'].delete('all')
        rounded_rect(row['badge'], 0, 0, 20, 20, 4,
                     fill=COLORS['sidebar_step_pending_badge'], outline='')
        row['badge'].create_text(10, 10, text=str(row['num']),
                                 fill=COLORS['sidebar_text_muted'], font=('Arial', 9, 'bold'))
        row['label'].config(fg=COLORS['sidebar_text_muted'], bg=bg, font=('Arial', 10))
