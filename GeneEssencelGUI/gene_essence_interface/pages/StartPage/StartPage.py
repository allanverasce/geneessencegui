from tkinter import *
from PIL import Image, ImageTk

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.NavigationSidebar import build_partners_footer
from gene_essence_interface.utils import resource_path

# (label, description)
FEATURES = [
    ("Training", "train models with your genetic data"),
    ("Prediction", "use a trained model for predictions"),
    ("Ensemble", "combines multiple models for greater accuracy"),
    ("Dataset Prep", "prepare RNA input files for analysis"),
]


class StartPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS['background_alt'])
        self.controller = controller
        self._build_left()
        self._build_right()

    def _build_left(self):
        left = Frame(self, bg=COLORS['sidebar_bg'], width=200)
        left.pack(side=LEFT, fill=Y)
        left.pack_propagate(False)

        # Partners no bottom — igual ao NavigationSidebar (packed primeiro para grudar embaixo)
        build_partners_footer(left, COLORS['sidebar_bg'])

        # Logo — mesmo frame/tamanho/fonte do NavigationSidebar._build_logo
        f = Frame(left, bg=COLORS['sidebar_bg'])
        f.pack(fill=X, padx=14, pady=(20, 8))

        sidebar_hex = COLORS['sidebar_bg'].lstrip('#')
        sidebar_rgb = tuple(int(sidebar_hex[i:i+2], 16) for i in (0, 2, 4))
        raw = Image.open(resource_path("assets/gene_essence_logo.png")).resize((42, 42), Image.LANCZOS).convert('RGBA')
        bg_img = Image.new('RGBA', raw.size, sidebar_rgb + (255,))
        bg_img.paste(raw, mask=raw.split()[3])
        self._sidebar_logo_img = ImageTk.PhotoImage(bg_img.convert('RGB'))
        Label(f, image=self._sidebar_logo_img, bg=COLORS['sidebar_bg']).pack(anchor=CENTER, pady=(0, 6))

        Label(f, text='GeneEssenceGUI', bg=COLORS['sidebar_bg'],
              fg=COLORS['primary'], font=('Arial', 12, 'bold')).pack()
        Label(f, text='Integrating DEG and NCBI datasets through ensemble machine learning for essential gene prediction',
              bg=COLORS['sidebar_bg'], fg='#9AA5B4',
              font=('Arial', 10), wraplength=162, justify=CENTER).pack(pady=(4, 0))

        # Divider — igual ao NavigationSidebar._build_divider
        Frame(left, bg=COLORS['sidebar_divider'], height=1).pack(fill=X, padx=12, pady=(8, 0))

        # Features
        for label, desc in FEATURES:
            row = Frame(left, bg=COLORS['sidebar_bg'])
            row.pack(fill=X, padx=14, pady=3)
            dot = Canvas(row, width=6, height=6, bg=COLORS['sidebar_bg'], highlightthickness=0)
            dot.pack(side=LEFT, padx=(0, 8), pady=(5, 0))
            dot.create_oval(0, 0, 6, 6, fill=COLORS['primary'], outline='')
            text_frame = Frame(row, bg=COLORS['sidebar_bg'])
            text_frame.pack(side=LEFT, fill=X, expand=True)
            Label(text_frame, text=label, bg=COLORS['sidebar_bg'], fg='#CBD5E1',
                  font=('Arial', 10, 'bold'), anchor=W).pack(anchor=W)
            Label(text_frame, text=desc, bg=COLORS['sidebar_bg'], fg='#9AA5B4',
                  font=('Arial', 9), wraplength=140, justify=LEFT, anchor=W).pack(anchor=W)

    def _build_right(self):
        right = Frame(self, bg=COLORS['background_alt'])
        right.pack(side=RIGHT, fill=BOTH, expand=True)

        center = Frame(right, bg=COLORS['background_alt'])
        center.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Big logo — imagem real
        img = Image.open(resource_path("assets/gene_essence_logo.png")).resize((88, 88), Image.LANCZOS)
        self._logo_img = ImageTk.PhotoImage(img)
        Label(center, image=self._logo_img, bg=COLORS['background_alt']).pack(pady=(0, 12))

        Label(center, text='GeneEssenceGUI', bg=COLORS['background_alt'],
              fg=COLORS['text'], font=('Arial', 22, 'bold')).pack()

        Label(center, text='Ensemble machine learning for essential gene\nprediction using DEG and NCBI datasets.',
              bg=COLORS['background_alt'], fg=COLORS['subtitle'],
              font=('Arial', 11), justify=CENTER, wraplength=340).pack(pady=(8, 0))

        CustomButton(center, text='START ANALYSIS', font_size=13, variant='primary',
                     command=lambda: self.controller.show_page('ChooseAnalysisType')
                     ).pack(pady=(24, 0), ipadx=10)

        CustomButton(center, text='PREPARE DATASET', font_size=13, variant='secondary',
                     command=lambda: self.controller.show_page('PrepareDataset')
                     ).pack(pady=(10, 0), ipadx=10)