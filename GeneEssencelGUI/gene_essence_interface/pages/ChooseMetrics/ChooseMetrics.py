import webbrowser
from tkinter import *
from tkinter import messagebox

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.database.queries.get_metrics import get_metrics
from gene_essence_interface.pages.components.CheckCard import CheckCard
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.NavigationSidebar import NavigationSidebar, STEPS_BY_TYPE, STEP_INDEX_BY_TYPE
from gene_essence_interface.pages.components.canvas_utils import rounded_rect

BG = COLORS['background_alt']


class ChooseMetrics(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.parent = parent
        self.metrics = get_metrics()
        self.metrics_vars = []

        self._sidebar = NavigationSidebar(self)
        self._sidebar.pack(side=LEFT, fill=Y)
        self._sidebar.set_active_step(3)

        self._content = Frame(self, bg=BG)
        self._content.pack(side=RIGHT, fill=BOTH, expand=True)

        self._body = None
        self.bind('<Visibility>', self._on_visible)

    def _on_visible(self, event):
        for var, _ in self.metrics_vars:
            var.set(False)
        self._build()

    def _build(self):
        if self._body:
            self._body.destroy()
        self.metrics_vars = []

        self._body = Frame(self._content, bg=BG)
        self._body.pack(fill=BOTH, expand=True)

        # Bottom buttons
        btn_frame = Frame(self._body, bg=BG)
        btn_frame.pack(side=BOTTOM, fill=X, padx=20, pady=12)
        Frame(self._body, bg=COLORS['border'], height=1).pack(side=BOTTOM, fill=X)

        self.next_btn = CustomButton(btn_frame, text='NEXT →', variant='primary',
                                     state=DISABLED, command=self._proceed)
        self.next_btn.pack(side=RIGHT)
        CustomButton(btn_frame, text='← BACK', variant='secondary',
                     command=self.controller.go_back).pack(side=RIGHT, padx=(0, 8))

        self.select_all_var = BooleanVar()
        CheckCard(btn_frame, title='Select All',
                  variable=self.select_all_var,
                  on_toggle=self._toggle_all).pack(side=LEFT)

        # Title
        title_area = Frame(self._body, bg=BG)
        title_area.pack(fill=X, padx=20, pady=(20, 0))
        Label(title_area, text='Which metrics do you want to use?',
              bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold')).pack(anchor=W)

        # 2-column grid
        grid = Frame(self._body, bg=BG)
        grid.pack(fill=BOTH, expand=True, padx=20, pady=10)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        selected_in_controller = self.controller.get_metrics() or []

        for i, metric in enumerate(self.metrics):
            var = BooleanVar()
            if metric['name'] in selected_in_controller:
                var.set(True)

            row, col = divmod(i, 2)
            card = CheckCard(grid,
                             title=metric['name'],
                             subtitle=metric.get('description', ''),
                             variable=var,
                             on_toggle=self._update_next)
            card.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

            web_btn = self._icon_btn(card.right_slot, '🔗',
                                     lambda url=metric.get('url'): self._open_url(url))
            web_btn.pack(side=LEFT, padx=2)

            self.metrics_vars.append((var, metric['name']))

        self._update_next()

    # ── Icon button (same style as ChooseModels) ──────────────────────────────

    def _icon_btn(self, parent, symbol, command):
        c = Canvas(parent, width=26, height=26, highlightthickness=0, bg=BG)

        def draw(hover=False):
            c.delete('all')
            bg = '#F0FBFC' if hover else '#F7F8FA'
            bd = '#63C2D1' if hover else '#E2E8F0'
            fg = '#3AA6B8' if hover else '#64748B'
            rounded_rect(c, 0.75, 0.75, 25.25, 25.25, 6, fill=bg, outline=bd, width=1.5)
            c.create_text(13, 13, text=symbol, fill=fg, font=('Arial', 12))

        c.bind('<Enter>', lambda e: draw(True))
        c.bind('<Leave>', lambda e: draw(False))
        c.bind('<Button-1>', lambda e: command())
        c.configure(cursor='hand2')
        draw()
        return c

    # ── Logic ─────────────────────────────────────────────────────────────────

    def _update_next(self):
        count = sum(v.get() for v, _ in self.metrics_vars)
        self.next_btn.config(state=NORMAL if count > 0 else DISABLED)
        if self.metrics_vars:
            all_checked = all(v.get() for v, _ in self.metrics_vars)
            self.select_all_var.set(all_checked)

    def _toggle_all(self):
        checked = self.select_all_var.get()
        for var, _ in self.metrics_vars:
            var.set(checked)
        self._update_next()

    def _open_url(self, url):
        if url:
            webbrowser.open(url)
        else:
            messagebox.showerror('Error', 'URL not available for this metric.')

    def on_show(self):
        t = self.controller.get_analyse_type() or 'Training'
        self._sidebar.reset_steps(STEPS_BY_TYPE[t])
        self._sidebar.set_active_step(STEP_INDEX_BY_TYPE[t]['ChooseMetrics'])

    def _proceed(self):
        self.controller.set_metrics([name for v, name in self.metrics_vars if v.get()])
        self.controller.show_page('ChooseHowToReceiveTheResults')