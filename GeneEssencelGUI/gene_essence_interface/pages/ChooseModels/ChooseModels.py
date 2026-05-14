import webbrowser
from tkinter import *
from tkinter import messagebox

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.database.queries.get_models import get_models
from gene_essence_interface.pages.ModelParametersFrame import ModelParameterFrame
from gene_essence_interface.pages.components.CheckCard import CheckCard
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.NavigationSidebar import NavigationSidebar, STEPS_BY_TYPE, STEP_INDEX_BY_TYPE
from gene_essence_interface.pages.components.canvas_utils import rounded_rect

BG = COLORS['background_alt']


class ChooseModels(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.parent = parent
        self.selected_models = set()
        self.models = get_models()
        self._model_data = {}   # name → {var, card, params_btn}

        self._sidebar = NavigationSidebar(self)
        self._sidebar.pack(side=LEFT, fill=Y)
        self._sidebar.set_active_step(2)

        self._content = Frame(self, bg=BG)
        self._content.pack(side=RIGHT, fill=BOTH, expand=True)

        self._body = None
        self.bind('<Visibility>', self._on_visible)

    def _on_visible(self, event):
        self._build()

    def _build(self):
        if self._body:
            self._body.destroy()
        self._model_data.clear()
        self.selected_models.clear()

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
                     command=self._go_back).pack(side=RIGHT, padx=(0, 8))

        # "Select All" checkbox
        self.select_all_var = BooleanVar()
        sel_all = CheckCard(btn_frame, title='Select All',
                            variable=self.select_all_var,
                            on_toggle=self._toggle_all)
        sel_all.pack(side=LEFT)

        # Title
        title_area = Frame(self._body, bg=BG)
        title_area.pack(fill=X, padx=20, pady=(20, 0))
        Label(title_area, text='Which models do you want to use?',
              bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold')).pack(anchor=W)

        # 2-column grid
        grid = Frame(self._body, bg=BG)
        grid.pack(fill=BOTH, expand=True, padx=20, pady=10)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        selected_in_controller = self.controller.get_models() or []

        for i, model in enumerate(self.models):
            var = BooleanVar()
            is_selected = model['name'] in selected_in_controller
            if is_selected:
                var.set(True)
                self.selected_models.add(model['name'])

            row, col = divmod(i, 2)
            card = CheckCard(grid,
                             title=model['name'],
                             subtitle=model.get('description', ''),
                             variable=var,
                             on_toggle=lambda m=model, v=var: self._on_toggle(m, v))
            card.grid(row=row, column=col, padx=5, pady=5, sticky='ew')

            web_btn = self._icon_btn(card.right_slot, '🔗',
                                     lambda url=model.get('url'): self._open_url(url),
                                     enabled=True, active=False)
            web_btn.pack(side=LEFT, padx=2)

            params_btn = self._icon_btn(card.right_slot, '⚙',
                                        lambda m=model: self._show_params(m),
                                        enabled=is_selected, active=is_selected)
            params_btn.pack(side=LEFT, padx=2)

            self._model_data[model['name']] = {
                'var': var, 'card': card, 'params_btn': params_btn,
            }

        self._update_next()
        self._sync_select_all()

    # ── Icon button ───────────────────────────────────────────────────────────

    def _icon_btn(self, parent, symbol, command, enabled=True, active=False):
        c = Canvas(parent, width=26, height=26, highlightthickness=0, bg=BG)
        state = {'enabled': enabled, 'active': active}

        def draw():
            c.delete('all')
            if not state['enabled']:
                bg, bd, fg = '#F7F8FA', '#E2E8F0', '#CBD5E1'
                c.configure(cursor='')
            elif state['active']:
                bg, bd, fg = '#F0FBFC', '#63C2D1', '#3AA6B8'
                c.configure(cursor='hand2')
            else:
                bg, bd, fg = '#F7F8FA', '#E2E8F0', '#64748B'
                c.configure(cursor='hand2')
            rounded_rect(c, 0.75, 0.75, 25.25, 25.25, 6,
                         fill=bg, outline=bd, width=1.5)
            c.create_text(13, 13, text=symbol, fill=fg, font=('Arial', 12))

        def on_hover(e):
            if state['enabled']:
                c.delete('all')
                rounded_rect(c, 0.75, 0.75, 25.25, 25.25, 6,
                             fill='#F0FBFC', outline='#63C2D1', width=1.5)
                c.create_text(13, 13, text=symbol, fill='#3AA6B8', font=('Arial', 12))

        c.bind('<Enter>', on_hover)
        c.bind('<Leave>', lambda e: draw())
        c.bind('<Button-1>', lambda e: state['enabled'] and command())

        c._state = state
        c._draw = draw
        draw()
        return c

    # ── Toggle logic ──────────────────────────────────────────────────────────

    def _on_toggle(self, model, var):
        name = model['name']
        if var.get():
            self.selected_models.add(name)
        else:
            self.selected_models.discard(name)

        data = self._model_data.get(name)
        if data and data['params_btn'].winfo_exists():
            en = var.get()
            data['params_btn']._state['enabled'] = en
            data['params_btn']._state['active'] = en
            data['params_btn']._draw()

        self._update_next()
        self._sync_select_all()

    def _toggle_all(self):
        checked = self.select_all_var.get()
        for name, data in self._model_data.items():
            data['var'].set(checked)
            if checked:
                self.selected_models.add(name)
            else:
                self.selected_models.discard(name)
            if data['params_btn'].winfo_exists():
                data['params_btn']._state['enabled'] = checked
                data['params_btn']._state['active'] = checked
                data['params_btn']._draw()
        self._update_next()

    def _sync_select_all(self):
        if self._model_data:
            all_checked = all(d['var'].get() for d in self._model_data.values())
            self.select_all_var.set(all_checked)

    def _update_next(self):
        self.next_btn.config(state=NORMAL if self.selected_models else DISABLED)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _open_url(self, url):
        if url:
            webbrowser.open(url)
        else:
            messagebox.showerror('Error', 'URL not available for this model.')

    def _show_params(self, model):
        modal = Toplevel(self)
        modal.title('')
        w, h = 420, 460
        modal.geometry(f"{w}x{h}+{(self.winfo_screenwidth() // 2) - w // 2}"
                       f"+{(self.winfo_screenheight() // 2) - h // 2}")
        modal.resizable(False, False)
        modal.configure(bg='white')
        ModelParameterFrame(modal, self.controller, model).pack(fill=BOTH, expand=True)
        modal.transient(self)
        modal.grab_set()
        self.parent.wait_window(modal)

    def on_show(self):
        t = self.controller.get_analyse_type() or 'Training'
        self._sidebar.reset_steps(STEPS_BY_TYPE[t])
        self._sidebar.set_active_step(STEP_INDEX_BY_TYPE[t]['ChooseModels'])

    def _proceed(self):
        self.controller.set_models(list(self.selected_models))
        self.controller.show_page('ChooseMetrics')

    def _go_back(self):
        self.selected_models.clear()
        for data in self._model_data.values():
            data['var'].set(False)
        self.controller.go_back()