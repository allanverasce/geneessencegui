import json
import os
from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.database.queries.get_data_project import get_data_project
from gene_essence_interface.pages.components.RoundedCard import RoundedCard
from gene_essence_interface.utils.get_database_connection import get_database_connection


class LoadProjectFrame(Frame):
    """Scrollable list of existing projects for the current analysis type."""

    _NORMAL   = ('white',   '#E2E8F0')
    _HOVER    = ('#F8FEFF', '#A8DCE6')
    _SELECTED = ('#F0FBFC', '#63C2D1')

    def __init__(self, parent, controller, selected_project, analyse_type, **kwargs):
        try:
            parent_bg = parent.cget('bg')
        except Exception:
            parent_bg = COLORS['background_alt']
        super().__init__(parent, bg=parent_bg, **kwargs)

        self.controller = controller
        self.selected_project = selected_project
        self.analyse_type = analyse_type
        self._items = {}
        self._all_projects = []
        self._scroll = lambda e: None

        projects = self._fetch_projects()
        self.selected_project.set('Choose the project')

        if not projects:
            Label(self, text='No projects available for this analysis type.',
                  bg=parent_bg, fg=COLORS['subtitle'],
                  font=('Arial', 11)).pack(padx=4, pady=12, anchor=W)
            return

        self._all_projects = projects

        # Search bar
        search_outer = Frame(self, bg='white', highlightthickness=1,
                             highlightbackground='#E2E8F0')
        search_outer.pack(fill=X, pady=(0, 8))

        Label(search_outer, text='⌕', bg='white', fg='#94A3B8',
              font=('Arial', 11)).pack(side=LEFT, padx=(8, 2), pady=5)

        self._search_var = StringVar()
        self._search_entry = Entry(search_outer, textvariable=self._search_var,
                                   bg='white', fg='#94A3B8', relief=FLAT,
                                   font=('Arial', 11), insertbackground=COLORS['text'],
                                   highlightthickness=0)
        self._search_entry.insert(0, 'Search by name or type…')
        self._search_entry.bind('<FocusIn>', self._on_focus_in)
        self._search_entry.bind('<FocusOut>', self._on_focus_out)
        self._search_entry.pack(side=LEFT, fill=X, expand=True, pady=5, padx=(0, 8))
        self._search_var.trace_add('write', self._filter)

        # Scrollable canvas
        canvas_frame = Frame(self, bg=parent_bg)
        canvas_frame.pack(fill=BOTH, expand=True)

        canvas = Canvas(canvas_frame, bg=parent_bg, highlightthickness=0)
        scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview, width=4)

        self._list_frame = Frame(canvas, bg=parent_bg)
        list_win = canvas.create_window((0, 0), window=self._list_frame, anchor='nw')

        canvas.configure(yscrollcommand=scrollbar.set,
                         height=min(len(projects) * 58, 192))

        self._list_frame.bind('<Configure>',
                              lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
                    lambda e: canvas.itemconfig(list_win, width=e.width))

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        if len(projects) > 3:
            scrollbar.pack(side=RIGHT, fill=Y)

        def _wheel(e):
            canvas.yview_scroll(-1 if e.delta > 0 else 1, 'units')

        self._scroll = _wheel
        canvas.bind('<MouseWheel>', _wheel)
        self._list_frame.bind('<MouseWheel>', _wheel)

        for name, status in projects:
            self._add_item(name, status)

        # Detail card (hidden until a project is selected)
        self._detail_card = None
        self._detail_placeholder = Frame(self, bg=parent_bg)
        self._detail_placeholder.pack(fill=X, pady=(8, 0))

    # ── DB ────────────────────────────────────────────────────────────────────

    def _fetch_projects(self):
        try:
            with get_database_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT project_name, file_path_csv, status FROM project WHERE project_type = ?",
                    (self.analyse_type,))
                return [(r[0], r[2]) for r in cur.fetchall() if os.path.isfile(r[1])]
        except Exception as e:
            print(f"Error fetching projects: {e}")
            return []

    # ── Search ────────────────────────────────────────────────────────────────

    def _on_focus_in(self, _):
        if self._search_entry.get() == 'Search by name or type…':
            self._search_entry.delete(0, END)
            self._search_entry.config(fg=COLORS['text'])
        self._deselect_all()

    def _deselect_all(self):
        for n in self._items:
            self._apply_style(n, *self._NORMAL)
        self.selected_project.set('Choose the project')
        if self._detail_card:
            self._detail_card.destroy()
            self._detail_card = None

    def _on_focus_out(self, _):
        if not self._search_entry.get():
            self._search_entry.insert(0, 'Search by name or type…')
            self._search_entry.config(fg='#94A3B8')

    def _filter(self, *_):
        q = self._search_var.get().lower()
        if q == 'search by name or type…':
            q = ''
        for name, _ in self._all_projects:
            data = self._items.get(name)
            if data is None:
                continue
            visible = not q or q in name.lower() or q in self.analyse_type.lower()
            if visible:
                data['card'].pack(fill=X, pady=(0, 6))
            else:
                data['card'].pack_forget()

    # ── Items ─────────────────────────────────────────────────────────────────

    def _add_item(self, name, status):
        completed  = status and status.lower() in ('completed', 'success', 'done')
        status_bg  = '#D1FAE5' if completed else '#FEE2E2'
        status_fg  = '#047857' if completed else '#DC2626'
        status_txt = '✓ Completed' if completed else '✗ Failed'

        card = RoundedCard(self._list_frame, card_bg='white', border='#E2E8F0', border_width=1.5)
        card.configure(cursor='hand2')
        card._body.configure(cursor='hand2')
        card.pack(fill=X, pady=(0, 6))

        left = Frame(card._body, bg='white', cursor='hand2')
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=(12, 8), pady=8)

        Label(left, text=name, bg='white', fg='#1A2332',
              font=('Arial', 11, 'bold'), anchor=W, cursor='hand2').pack(anchor=W)

        badge_row = Frame(left, bg='white', cursor='hand2')
        badge_row.pack(anchor=W, pady=(3, 0))

        type_badge = Label(badge_row, text=self.analyse_type, bg='#F1F5F9', fg='#64748B',
                           font=('Arial', 9), padx=6, pady=2, cursor='hand2')
        type_badge.pack(side=LEFT)

        status_badge = Label(card._body, text=status_txt, bg=status_bg, fg=status_fg,
                             font=('Arial', 9, 'bold'), padx=8, pady=2, cursor='hand2')
        status_badge.pack(side=RIGHT, padx=(0, 12), pady=12)

        self._items[name] = {
            'card': card, 'left': left, 'badge_row': badge_row,
            'type_badge': type_badge, 'status_badge': status_badge,
            'status_bg': status_bg, 'status_fg': status_fg,
        }

        def on_click(e, n=name): self._select_item(n)

        def on_enter(e, n=name):
            if self.selected_project.get() != n:
                self._apply_style(n, *self._HOVER)

        def on_leave(e, n=name, c=card):
            if self.selected_project.get() != n:
                x, y = c.winfo_pointerxy()
                rx, ry = c.winfo_rootx(), c.winfo_rooty()
                if not (rx <= x <= rx + c.winfo_width() and ry <= y <= ry + c.winfo_height()):
                    self._apply_style(n, *self._NORMAL)

        for w in self._descendants(card):
            w.bind('<Button-1>', on_click)
            w.bind('<Enter>', on_enter)
            w.bind('<Leave>', on_leave)
            w.bind('<MouseWheel>', self._scroll)

    def _apply_style(self, name, bg, border):
        data = self._items[name]
        data['card'].set_card_style(bg=bg, border=border)
        # Restore badge colors wiped by RoundedCard.update_bg
        data['type_badge'].configure(bg='#F1F5F9', fg='#64748B')
        data['status_badge'].configure(bg=data['status_bg'], fg=data['status_fg'])

    def _select_item(self, name):
        for n in self._items:
            self._apply_style(n, *(self._SELECTED if n == name else self._NORMAL))
        self.selected_project.set(name)
        self._show_detail(name)

    # ── Detail card ───────────────────────────────────────────────────────────

    def _show_detail(self, name):
        if self._detail_card:
            self._detail_card.destroy()
            self._detail_card = None

        project = get_data_project(self.analyse_type, name)
        if not project:
            return

        completed = project.get('status', '').lower() in ('completed', 'success', 'done')
        badge_bg  = '#D1FAE5' if completed else '#FEE2E2'
        badge_fg  = '#047857' if completed else '#DC2626'
        badge_txt = 'Completed' if completed else 'Failed'

        card = RoundedCard(self._detail_placeholder, card_bg='white',
                           border='#E2E8F0', border_width=1.5)
        card.pack(fill=X)
        self._detail_card = card

        body = card._body

        # Header row: name + status badge
        header = Frame(body, bg='white')
        header.pack(fill=X, padx=14, pady=(10, 8))
        Label(header, text=name, bg='white', fg='#1A2332',
              font=('Arial', 11, 'bold')).pack(side=LEFT)
        Label(header, text=badge_txt, bg=badge_bg, fg=badge_fg,
              font=('Arial', 9, 'bold'), padx=8, pady=2).pack(side=RIGHT)

        # Separator
        Frame(body, bg='#F1F5F9', height=1).pack(fill=X, padx=14)

        # Build rows depending on analysis type
        rows = [('Analysis type', self.analyse_type)]

        if self.analyse_type != 'Prediction':
            models_raw = project.get('selected_models', '[]')
            try:
                models_list = json.loads(models_raw) if isinstance(models_raw, str) else models_raw
            except Exception:
                models_list = []
            rows.append(('Models', ', '.join(models_list) if models_list else '—'))

            metrics_raw = project.get('selected_metrics', '[]')
            try:
                metrics_list = json.loads(metrics_raw) if isinstance(metrics_raw, str) else metrics_raw
            except Exception:
                metrics_list = []
            rows.append(('Metrics', ', '.join(metrics_list) if metrics_list else '—'))

        delivery = project.get('result_delivery_method', '') or '—'
        rows.append(('Delivery', delivery))

        for i, (label, value) in enumerate(rows):
            is_last = i == len(rows) - 1
            self._info_row(body, label, value, is_last)

    def _info_row(self, parent, label, value, last=False):
        row = Frame(parent, bg='white')
        row.pack(fill=X, padx=14)
        Label(row, text=label, bg='white', fg='#64748B',
              font=('Arial', 10)).pack(side=LEFT, pady=6)
        Label(row, text=value, bg='white', fg='#1A2332',
              font=('Arial', 10, 'bold')).pack(side=RIGHT, pady=6)
        if not last:
            Frame(parent, bg='#F1F5F9', height=1).pack(fill=X, padx=14)

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _descendants(widget):
        result = [widget]
        for child in widget.winfo_children():
            result.extend(LoadProjectFrame._descendants(child))
        return result
