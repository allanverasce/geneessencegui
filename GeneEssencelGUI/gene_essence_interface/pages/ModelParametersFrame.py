from tkinter import *

from gene_essence_interface.utils.open_url import open_url

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.components.CustomButton import CustomButton

BG = 'white'


def _type_label(value):
    if value is None:
        return 'None — optional'
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, int):
        return 'int'
    if isinstance(value, float):
        return 'float'
    if isinstance(value, str):
        return f'str'
    return type(value).__name__


class ModelParameterFrame(Frame):
    def __init__(self, parent, controller, model):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.model = model
        self.entries = {}
        self._defaults = dict(model.get('parameters', {}))
        self._params = controller.get_model_parameters(model['name']) or dict(self._defaults)

        self._build()

    def _build(self):
        # ── Header ────────────────────────────────────────────────────────────
        header = Frame(self, bg=BG)
        header.pack(fill=X, padx=16, pady=(14, 10))

        left = Frame(header, bg=BG)
        left.pack(side=LEFT, fill=BOTH, expand=True)
        Label(left, text=self.model.get('name', ''), bg=BG, fg='#1A2332',
              font=('Arial', 13, 'bold')).pack(anchor=W)
        Label(left, text='Customize hyperparameters for this model', bg=BG,
              fg='#64748B', font=('Arial', 10)).pack(anchor=W, pady=(2, 0))

        right = Frame(header, bg=BG)
        right.pack(side=RIGHT, anchor=N, pady=(2, 0))

        url = self.model.get('url', '')
        if url:
            docs = Label(right, text='🔗 docs', bg=BG, fg='#3AA6B8',
                         font=('Arial', 9), cursor='hand2',
                         highlightthickness=1, highlightbackground='#63C2D1',
                         padx=7, pady=2)
            docs.pack(side=LEFT, padx=(0, 8))
            docs.bind('<Button-1>', lambda e, u=url: open_url(u, self))

        close_btn = Label(right, text='×', bg='#F7F8FA', fg='#64748B',
                          font=('Arial', 14), cursor='hand2',
                          highlightthickness=1, highlightbackground='#E2E8F0',
                          width=2, anchor=CENTER)
        close_btn.pack(side=LEFT)
        close_btn.bind('<Button-1>', lambda e: self.winfo_toplevel().destroy())
        close_btn.bind('<Enter>',
                       lambda e: close_btn.config(bg='#FFE4E4', fg='#EF4444',
                                                   highlightbackground='#FCA5A5'))
        close_btn.bind('<Leave>',
                       lambda e: close_btn.config(bg='#F7F8FA', fg='#64748B',
                                                   highlightbackground='#E2E8F0'))

        Frame(self, bg='#E2E8F0', height=1).pack(fill=X)

        # ── Scrollable body ───────────────────────────────────────────────────
        body = Frame(self, bg=BG)
        body.pack(fill=BOTH, expand=True)

        canvas = Canvas(body, bg=BG, highlightthickness=0)
        scrollbar = Scrollbar(body, orient=VERTICAL, command=canvas.yview, width=4)

        self._scroll_frame = Frame(canvas, bg=BG)
        win = canvas.create_window((0, 0), window=self._scroll_frame, anchor='nw')

        canvas.configure(yscrollcommand=scrollbar.set)
        self._scroll_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
                    lambda e: canvas.itemconfig(win, width=e.width))

        def _wheel(e):
            canvas.yview_scroll(-1 if e.delta > 0 else 1, 'units')
        canvas.bind('<Enter>', lambda e: canvas.bind_all('<MouseWheel>', _wheel))
        canvas.bind('<Leave>', lambda e: canvas.unbind_all('<MouseWheel>'))

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        if len(self._params) > 6:
            scrollbar.pack(side=RIGHT, fill=Y)

        self._populate_rows()

        # ── Footer ────────────────────────────────────────────────────────────
        Frame(self, bg='#E2E8F0', height=1).pack(fill=X)

        footer = Frame(self, bg=BG)
        footer.pack(fill=X, padx=16, pady=10)

        self._save_btn = CustomButton(footer, text='Save Changes', variant='primary',
                                      state=DISABLED, command=self._save)
        self._save_btn.pack(side=RIGHT)

        CustomButton(footer, text='Reset Defaults', variant='secondary',
                     command=self._reset).pack(side=RIGHT, padx=(0, 8))

    def _populate_rows(self):
        for w in self._scroll_frame.winfo_children():
            w.destroy()
        self.entries.clear()

        params = list(self._params.items())
        for i, (name, value) in enumerate(params):
            is_last = i == len(params) - 1

            row = Frame(self._scroll_frame, bg=BG)
            row.pack(fill=X, padx=16)

            left = Frame(row, bg=BG)
            left.pack(side=LEFT, fill=BOTH, expand=True, pady=6)

            Label(left, text=name, bg=BG, fg='#1A2332',
                  font=('Arial', 11, 'bold')).pack(anchor=W)
            Label(left, text=_type_label(value), bg=BG, fg='#94A3B8',
                  font=('Arial', 9)).pack(anchor=W)

            entry_wrap = Frame(row, bg=COLORS['border'])
            entry_wrap.pack(side=RIGHT, pady=6)
            entry_inner = Frame(entry_wrap, bg='#F7F8FA')
            entry_inner.pack(padx=1, pady=1)

            entry = Entry(entry_inner, bg='#F7F8FA', fg='#1A2332',
                          font=('Arial', 11), relief='flat', bd=0,
                          highlightthickness=0, width=9,
                          justify=RIGHT, insertbackground='#1A2332')
            entry.insert(0, '' if value is None else str(value))
            entry.pack(padx=6, ipady=4)
            entry.bind('<KeyRelease>', lambda e: self._save_btn.config(state=NORMAL))
            self.entries[name] = entry

            if not is_last:
                Frame(self._scroll_frame, bg='#F1F5F9', height=1).pack(fill=X, padx=16)

    def _save(self):
        updated = {}
        for param, entry in self.entries.items():
            raw = entry.get().strip()
            if raw == '' or raw.lower() == 'none':
                updated[param] = None
            else:
                try:
                    updated[param] = int(raw)
                except ValueError:
                    try:
                        updated[param] = float(raw)
                    except ValueError:
                        updated[param] = raw
        self.controller.update_model_parameters(self.model['name'], updated)
        self._params.update(updated)
        self._save_btn.config(state=DISABLED)

    def _reset(self):
        self._params = dict(self._defaults)
        self.controller.update_model_parameters(self.model['name'], self._params)
        self._populate_rows()
        self._save_btn.config(state=DISABLED)