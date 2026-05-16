import subprocess
import sys
from tkinter import *


_BG       = '#FFFFFF'
_FG       = '#1A2332'
_MUTED    = '#64748B'
_BORDER   = '#E2E8F0'
_PRIM_BG  = '#63C2D1'
_PRIM_FG  = '#FFFFFF'
_PRIM_ACT = '#4DB8C9'
_BTN_BG   = '#F1F5F9'
_BTN_ACT  = '#E2E8F0'
_INPUT_BG = '#F7F8FA'


def open_url(url, parent=None):
    try:
        cmd = ['open', url] if sys.platform == 'darwin' else ['xdg-open', url]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            _fallback(url, parent)
    except Exception:
        _fallback(url, parent)


def _fallback(url, parent):
    root = parent.winfo_toplevel() if parent else None

    dlg = Toplevel(parent)
    dlg.withdraw()
    dlg.title('Open in browser')
    dlg.configure(bg=_BG)
    dlg.resizable(False, False)
    dlg.transient(parent)

    # Header
    Frame(dlg, bg=_BG, height=6).pack(fill=X)
    Label(
        dlg, text='No browser available',
        bg=_BG, fg=_FG, font=('Arial', 13, 'bold'), anchor=W, padx=20,
    ).pack(fill=X)
    Label(
        dlg, text='Copy the link below and open it manually.',
        bg=_BG, fg=_MUTED, font=('Arial', 10), anchor=W, padx=20,
    ).pack(fill=X, pady=(2, 12))

    Frame(dlg, bg=_BORDER, height=1).pack(fill=X)

    # URL field
    url_frame = Frame(dlg, bg=_BG, padx=20, pady=14)
    url_frame.pack(fill=X)

    entry = Entry(
        url_frame,
        font=('Arial', 10),
        bg=_INPUT_BG, fg=_FG,
        relief='flat',
        bd=0,
        highlightthickness=1,
        highlightbackground=_BORDER,
        highlightcolor=_PRIM_BG,
        readonlybackground=_INPUT_BG,
        state='readonly',
    )
    entry.pack(fill=X, ipady=7)
    entry.config(state='normal')
    entry.insert(0, url)
    entry.config(state='readonly')

    def _copy():
        dlg.clipboard_clear()
        dlg.clipboard_append(url)
        copy_btn.config(text='Copied!', bg=_PRIM_ACT)
        dlg.after(1500, lambda: copy_btn.config(text='Copy', bg=_PRIM_BG))

    Frame(dlg, bg=_BORDER, height=1).pack(fill=X)

    # Bottom bar
    bot = Frame(dlg, bg=_BG, padx=20, pady=12)
    bot.pack(fill=X)

    Button(
        bot, text='Close', command=dlg.destroy,
        bg=_BTN_BG, fg=_FG, activebackground=_BTN_ACT, activeforeground=_FG,
        relief='flat', padx=18, pady=6, cursor='hand2',
        highlightthickness=1, highlightbackground=_BORDER,
    ).pack(side=RIGHT, padx=(6, 0))

    copy_btn = Button(
        bot, text='Copy', command=_copy,
        bg=_PRIM_BG, fg=_PRIM_FG, activebackground=_PRIM_ACT, activeforeground=_PRIM_FG,
        relief='flat', padx=18, pady=6, cursor='hand2', bd=0,
    )
    copy_btn.pack(side=RIGHT)

    dlg.update_idletasks()
    w, h = 460, dlg.winfo_reqheight()
    if root:
        px = root.winfo_rootx()
        py = root.winfo_rooty()
        pw = root.winfo_width()
        ph = root.winfo_height()
        dlg.geometry(f'{w}x{h}+{px + (pw - w) // 2}+{py + (ph - h) // 2}')
    else:
        dlg.geometry(f'{w}x{h}')

    dlg.deiconify()
    dlg.grab_set()
    dlg.focus_set()
    entry.focus_set()
    entry.select_range(0, END)
