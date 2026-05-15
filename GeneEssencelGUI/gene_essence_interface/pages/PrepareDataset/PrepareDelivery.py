import os
import re
from tkinter import *
from tkinter import filedialog

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.PrepareDataset.PrepareDatasetSidebar import PrepareDatasetSidebar
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.RoundedCard import RoundedCard
from gene_essence_interface.utils.get_initial_dir import get_initial_dir

BG = COLORS['background_alt']
EMAIL_RE = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
_EMAIL_PLACEHOLDER = 'your-email@example.com'
_PLACEHOLDER_FG = '#94A3B8'


class _DeliveryCard(RoundedCard):
    def __init__(self, parent, radio_var, value, title, subtitle, **kwargs):
        super().__init__(parent, **kwargs)
        self.radio_var = radio_var
        self.value = value

        self.configure(cursor='hand2')
        self._body.configure(cursor='hand2')

        top = Frame(self._body, bg=COLORS['card_bg'], cursor='hand2')
        top.pack(fill=X, padx=12, pady=(10, 0))

        self.dot = Canvas(top, width=16, height=16, bg=COLORS['card_bg'], highlightthickness=0)
        self.dot.pack(side=LEFT, padx=(0, 10))

        text_f = Frame(top, bg=COLORS['card_bg'], cursor='hand2')
        text_f.pack(side=LEFT, fill=X, expand=True)
        Label(text_f, text=title, bg=COLORS['card_bg'],
              fg=COLORS['text'], font=('Arial', 12, 'bold')).pack(anchor=W)

        Label(self._body, text=subtitle, bg=COLORS['card_bg'],
              fg=COLORS['subtitle'], font=('Arial', 10)).pack(anchor=W, padx=14, pady=(4, 0))

        self.input_area = Frame(self._body, bg=COLORS['card_bg'])

        for w in (self, self._body, top, text_f, self.dot):
            w.bind('<Button-1>', self._select)

        radio_var.trace_add('write', self._update_display)
        self._update_display()

    def _select(self, _=None):
        self.radio_var.set(self.value)

    def _update_display(self, *_):
        selected = self.radio_var.get() == self.value
        bg = COLORS['card_selected_bg'] if selected else COLORS['card_bg']
        border = COLORS['card_selected_border'] if selected else COLORS['card_border']
        self.set_card_style(bg, border)

        self.dot.delete('all')
        color = COLORS['primary'] if selected else '#CBD5E1'
        self.dot.create_oval(1, 1, 15, 15, outline=color, width=2)
        if selected:
            self.dot.create_oval(5, 5, 11, 11, fill=COLORS['primary'], outline='')

        if selected:
            self.input_area.pack(fill=X, padx=12, pady=(0, 10))
        else:
            self.input_area.pack_forget()


class PrepareDelivery(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.radio_var = StringVar(value='')
        self.email_var = StringVar(value='')
        self.directory_var = StringVar(value='')

        sidebar = PrepareDatasetSidebar(self)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.set_active_step(1)

        self._content = Frame(self, bg=BG)
        self._content.pack(side=RIGHT, fill=BOTH, expand=True)

        self.bind('<Visibility>', self._on_visible)
        self._build()

    def _build(self):
        btn_frame = Frame(self._content, bg=BG)
        btn_frame.pack(side=BOTTOM, fill=X, padx=20, pady=12)
        Frame(self._content, bg=COLORS['border'], height=1).pack(side=BOTTOM, fill=X)

        self.next_btn = CustomButton(btn_frame, text='NEXT →', variant='primary',
                                     state=DISABLED, command=self._proceed)
        self.next_btn.pack(side=RIGHT)
        CustomButton(btn_frame, text='← BACK', variant='secondary',
                     command=self.controller.go_back).pack(side=RIGHT, padx=(0, 8))

        title_area = Frame(self._content, bg=BG)
        title_area.pack(fill=X, padx=20, pady=(20, 0))
        Label(title_area, text='How do you want to receive the results?',
              bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold')).pack(anchor=W)

        cards = Frame(self._content, bg=BG)
        cards.pack(fill=X, padx=20, pady=14)

        self._email_card = _DeliveryCard(
            cards, self.radio_var, 'email',
            'Receive by Email',
            'Send the results as a ZIP file to your email address.'
        )
        self._email_card.pack(fill=X, pady=(0, 8))
        self._build_email_input(self._email_card.input_area)

        self._local_card = _DeliveryCard(
            cards, self.radio_var, 'local',
            'Save Locally',
            'Choose a folder on your computer to save the results.'
        )
        self._local_card.pack(fill=X)
        self._build_local_input(self._local_card.input_area)

        self.radio_var.trace_add('write', self._update_next)

    def _build_email_input(self, parent):
        entry_wrap = Frame(parent, bg=COLORS['border'])
        entry_wrap.pack(fill=X)
        entry_inner = Frame(entry_wrap, bg='#F7F8FA')
        entry_inner.pack(fill=X, padx=1, pady=1)
        self._email_entry = Entry(entry_inner,
                                  bg='#F7F8FA', fg=_PLACEHOLDER_FG,
                                  font=('Arial', 11), relief='flat', bd=0,
                                  highlightthickness=0,
                                  insertbackground=COLORS['text'])
        self._email_entry.insert(0, _EMAIL_PLACEHOLDER)
        self._email_entry.pack(fill=X, expand=True, ipady=5, padx=6)
        self._email_entry.bind('<FocusIn>', self._on_email_focus_in)
        self._email_entry.bind('<FocusOut>', self._on_email_focus_out)
        self._email_entry.bind('<KeyRelease>', self._on_email_key)

        self._email_error = Label(parent, text='', fg=COLORS['error'],
                                  bg=COLORS['card_selected_bg'], font=('Arial', 9))
        self._email_error.pack(anchor=W, pady=(4, 0))

    def _build_local_input(self, parent):
        row = Frame(parent, bg=COLORS['card_bg'])
        row.pack(fill=X)

        entry_wrap = Frame(row, bg=COLORS['border'])
        entry_wrap.pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
        entry_inner = Frame(entry_wrap, bg='#F7F8FA')
        entry_inner.pack(fill=X, padx=1, pady=1)
        self._dir_label = Label(entry_inner, text='No folder selected',
                                fg=COLORS['subtitle'], bg='#F7F8FA',
                                font=('Arial', 11), anchor=W)
        self._dir_label.pack(fill=X, expand=True, ipady=5, padx=6)

        CustomButton(row, text='Browse…', font_size=10, variant='secondary',
                     command=self._select_dir).pack(side=RIGHT)

    def _on_email_focus_in(self, _):
        if self._email_entry.get() == _EMAIL_PLACEHOLDER:
            self._email_entry.delete(0, END)
            self._email_entry.config(fg=COLORS['text'])

    def _on_email_focus_out(self, _):
        if not self._email_entry.get():
            self._email_entry.insert(0, _EMAIL_PLACEHOLDER)
            self._email_entry.config(fg=_PLACEHOLDER_FG)
        self._validate_email()

    def _on_email_key(self, _):
        self.email_var.set(self._email_entry.get())
        self._validate_email()

    def _on_visible(self, _):
        receipt_type = self.controller.get_prepare_receipt_type()
        contact = self.controller.get_prepare_receipt_in()
        if receipt_type:
            self.radio_var.set(receipt_type)
        if receipt_type == 'email' and contact:
            self._email_entry.delete(0, END)
            self._email_entry.insert(0, contact)
            self._email_entry.config(fg=COLORS['text'])
            self.email_var.set(contact)
        elif receipt_type == 'local' and contact and os.path.exists(contact):
            self._dir_label.config(text=os.path.basename(contact),
                                   fg=COLORS['success'], bg='#F7F8FA')
            self.directory_var.set(contact)
        self._update_next()

    def _validate_email(self, *_):
        if not self._email_error.winfo_exists():
            return
        email = self.email_var.get()
        if self.radio_var.get() == 'email':
            if re.match(EMAIL_RE, email):
                self._email_error.config(text='')
            else:
                self._email_error.config(text='Invalid email format.')
        self._update_next()

    def _select_dir(self):
        path = filedialog.askdirectory(title='Select Directory', initialdir=get_initial_dir())
        if path:
            self._dir_label.config(text=os.path.basename(path),
                                   fg=COLORS['success'], bg='#F7F8FA')
            self.directory_var.set(path)
        self._update_next()

    def _update_next(self, *_):
        mode = self.radio_var.get()
        valid = (mode == 'email' and re.match(EMAIL_RE, self.email_var.get())) or \
                (mode == 'local' and self.directory_var.get())
        self.next_btn.config(state=NORMAL if valid else DISABLED)

    def _proceed(self):
        mode = self.radio_var.get()
        self.controller.set_prepare_receipt_type(mode)
        self.controller.set_prepare_receipt_in(
            self.email_var.get() if mode == 'email' else self.directory_var.get()
        )
        self.controller.show_page('PrepareConfirm')
