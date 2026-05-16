import os
from tkinter import *

from gene_essence_interface.utils.get_initial_dir import get_initial_dir

BG        = '#FFFFFF'
FG        = '#1E293B'
MUTED     = '#64748B'
BORDER    = '#E2E8F0'
LIST_BG   = '#F8FAFC'
SEL_BG    = '#F0FBFC'
SEL_FG    = '#1A2332'
DIR_FG    = '#0E7490'
FILE_FG   = '#475569'
BTN_BG    = '#F1F5F9'
BTN_ACT   = '#E2E8F0'
PRIM_BG   = '#63C2D1'
PRIM_FG   = '#FFFFFF'
PRIM_ACT  = '#4DB8C9'


class _FileDialog(Toplevel):

    def __init__(self, parent, title, initialdir, mode, filetypes=None):
        super().__init__(parent)
        self.withdraw()
        self.title(title)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry('580x460')
        self.transient(parent)

        self._mode    = mode
        self._ft      = filetypes or []
        self._entries = []
        self.result   = None

        start = initialdir if initialdir and os.path.isdir(initialdir) else get_initial_dir()
        self._cwd = os.path.realpath(start)

        self._build_ui()
        self._load(self._cwd)
        self._center(parent)
        self.deiconify()

        self.protocol('WM_DELETE_WINDOW', self._cancel)
        self.grab_set()
        self.focus_set()
        self.wait_window(self)

    def _build_ui(self):
        top = Frame(self, bg=BG, padx=14, pady=10)
        top.pack(fill=X)

        self._up_btn = Button(
            top, text='↑  Up', command=self._go_up,
            bg=BTN_BG, fg=FG, activebackground=BTN_ACT, activeforeground=FG,
            relief='flat', padx=12, pady=5, cursor='hand2',
            highlightthickness=1, highlightbackground=BORDER,
        )
        self._up_btn.pack(side=LEFT)

        self._path_var = StringVar()
        Label(
            top, textvariable=self._path_var,
            bg=BG, fg=MUTED, font=('Arial', 9), anchor=W,
        ).pack(side=LEFT, padx=(10, 0), fill=X, expand=True)

        Frame(self, bg=BORDER, height=1).pack(fill=X)

        list_wrap = Frame(self, bg=BG, padx=14, pady=10)
        list_wrap.pack(fill=BOTH, expand=True)

        scrollbar = Scrollbar(list_wrap, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        self._lb = Listbox(
            list_wrap,
            yscrollcommand=scrollbar.set,
            bg=LIST_BG,
            fg=FG,
            selectbackground=SEL_BG,
            selectforeground=SEL_FG,
            font=('Arial', 11),
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=PRIM_BG,
            activestyle='none',
            cursor='hand2',
        )
        self._lb.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self._lb.yview)

        self._lb.bind('<Double-Button-1>', self._on_double)
        self._lb.bind('<Return>',          self._on_double)

        Frame(self, bg=BORDER, height=1).pack(fill=X)

        bot = Frame(self, bg=BG, padx=14, pady=10)
        bot.pack(fill=X)

        self._sel_var = StringVar(value='')
        Label(
            bot, textvariable=self._sel_var,
            bg=BG, fg=MUTED, font=('Arial', 9), anchor=W,
        ).pack(side=LEFT, fill=X, expand=True)

        ok_label = 'Select Folder' if self._mode == 'dir' else 'Open'
        Button(
            bot, text=ok_label, command=self._confirm,
            bg=PRIM_BG, fg=PRIM_FG, activebackground=PRIM_ACT, activeforeground=PRIM_FG,
            relief='flat', padx=18, pady=6, cursor='hand2', bd=0,
        ).pack(side=RIGHT, padx=(6, 0))

        Button(
            bot, text='Cancel', command=self._cancel,
            bg=BTN_BG, fg=FG, activebackground=BTN_ACT, activeforeground=FG,
            relief='flat', padx=18, pady=6, cursor='hand2',
            highlightthickness=1, highlightbackground=BORDER,
        ).pack(side=RIGHT)


    def _load(self, path):
        try:
            path  = os.path.realpath(path)
            items = os.listdir(path)
        except PermissionError:
            return

        self._cwd = path
        self._path_var.set(path)
        self._sel_var.set('')
        self._entries = []
        self._lb.delete(0, END)

        dirs  = sorted([n for n in items if not n.startswith('.') and os.path.isdir(os.path.join(path, n))],  key=str.lower)
        files = [] if self._mode == 'dir' else sorted(
            [n for n in items if not n.startswith('.') and os.path.isfile(os.path.join(path, n)) and self._match(n)],
            key=str.lower,
        )

        for n in dirs:
            self._lb.insert(END, f'  ▸  {n}')
            self._entries.append(('dir', os.path.join(path, n), n))

        for n in files:
            self._lb.insert(END, f'  ▪  {n}')
            self._entries.append(('file', os.path.join(path, n), n))

        for i in range(len(dirs)):
            self._lb.itemconfig(i, fg=DIR_FG)
        for i in range(len(dirs), len(dirs) + len(files)):
            self._lb.itemconfig(i, fg=FILE_FG)

        parent = os.path.dirname(path)
        self._up_btn.config(state=NORMAL if parent != path else DISABLED)

    def _match(self, name):
        if not self._ft:
            return True
        for _, pat in self._ft:
            if pat in ('*', '*.*'):
                return True
            if name.lower().endswith(pat.lstrip('*').lower()):
                return True
        return False

    def _on_double(self, _event=None):
        sel = self._lb.curselection()
        if not sel:
            return
        kind, full_path, name = self._entries[sel[0]]
        if kind == 'dir':
            self._load(full_path)
        elif self._mode == 'file':
            self.result = full_path
            self.destroy()

    def _go_up(self):
        parent = os.path.dirname(self._cwd)
        if parent != self._cwd:
            self._load(parent)

    def _confirm(self):
        sel = self._lb.curselection()
        if sel:
            kind, full_path, name = self._entries[sel[0]]
            if self._mode == 'dir':
                self.result = full_path if kind == 'dir' else self._cwd
            elif kind == 'file':
                self.result = full_path
            else:
                self._load(full_path)
                return
        elif self._mode == 'dir':
            self.result = self._cwd
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()

    def _center(self, parent):
        self.update_idletasks()
        root = parent.winfo_toplevel()
        px   = root.winfo_rootx()
        py   = root.winfo_rooty()
        pw   = root.winfo_width()
        ph   = root.winfo_height()
        w, h = 580, 460
        self.geometry(f'{w}x{h}+{px + (pw - w) // 2}+{py + (ph - h) // 2}')


def ask_directory(parent, title='Select Directory', initialdir=None):
    d = _FileDialog(parent, title, initialdir, mode='dir')
    return d.result or ''


def ask_open_filename(parent, title='Select File', filetypes=None, initialdir=None):
    d = _FileDialog(parent, title, initialdir, mode='file', filetypes=filetypes)
    return d.result or ''
