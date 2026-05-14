import os
import subprocess
import threading
import time
from tkinter import *

from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.pages.PrepareDataset.PrepareDatasetSidebar import PrepareDatasetSidebar
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.utils.resource_path import resource_path

BG = COLORS['background_alt']


class RunPreparation(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self._start_time = None
        self._done = False
        self._process = None

        self._out_dir = ''

        self._sidebar = PrepareDatasetSidebar(self)
        self._sidebar.pack(side=LEFT, fill=Y)
        self._sidebar.set_active_step(1)

        self._right = Frame(self, bg=BG)
        self._right.pack(side=RIGHT, fill=BOTH, expand=True)

        self._build()
        self.bind('<Visibility>', self._on_visible)

    def _build(self):
        # Title
        title_row = Frame(self._right, bg=BG)
        title_row.pack(fill=X, padx=20, pady=(16, 8))
        self._title_lbl = Label(title_row, text='Preparing dataset…',
                                bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold'))
        self._title_lbl.pack(anchor=W)

        # Success banner (hidden until done)
        _BBG = COLORS['success_banner_bg']
        self._banner = Frame(self._right, bg=_BBG,
                             highlightthickness=1,
                             highlightbackground=COLORS['success_banner_border'])

        top_row = Frame(self._banner, bg=_BBG)
        top_row.pack(fill=X, padx=12, pady=10)

        icon_c = Canvas(top_row, width=24, height=24, bg=_BBG, highlightthickness=0)
        icon_c.pack(side=LEFT, padx=(0, 10))
        icon_c.create_oval(1, 1, 23, 23, fill=COLORS['success'], outline='')
        icon_c.create_text(12, 13, text='✓', fill='white', font=('Arial', 12, 'bold'))

        text_col = Frame(top_row, bg=_BBG)
        text_col.pack(side=LEFT, fill=X, expand=True)
        self._banner_title = Label(text_col, text='', bg=_BBG,
                                   fg=COLORS['success'], font=('Arial', 12, 'bold'))
        self._banner_title.pack(anchor=W)
        self._banner_sub = Label(text_col, text='', bg=_BBG,
                                 fg='#065F46', font=('Arial', 10))
        self._banner_sub.pack(anchor=W)

        CustomButton(top_row, text='+ New Preparation', variant='success',
                     command=self._new_preparation).pack(side=RIGHT, padx=(10, 0))

        # Output path row
        self._path_row = Frame(self._banner, bg='#F0FDF4',
                               highlightthickness=1, highlightbackground='#BBF7D0')
        Label(self._path_row, text='OUTPUT', bg='#F0FDF4', fg='#059669',
              font=('Arial', 9, 'bold')).pack(side=LEFT, padx=(10, 4), pady=6)
        self._path_value_lbl = Label(self._path_row, text='', bg='#F0FDF4',
                                     fg='#065F46', font=('Courier', 9), anchor=W)
        self._path_value_lbl.pack(side=LEFT, fill=X, expand=True, pady=6)
        CustomButton(self._path_row, text='Open Folder', variant='success',
                     font_size=9, command=self._open_output_folder).pack(side=RIGHT, padx=(4, 8), pady=4)

        # Bottom buttons
        btn_frame = Frame(self._right, bg=BG)
        btn_frame.pack(side=BOTTOM, fill=X, padx=20, pady=12)
        Frame(self._right, bg=COLORS['border'], height=1).pack(side=BOTTOM, fill=X)

        self._back_btn = CustomButton(btn_frame, text='← BACK', variant='secondary',
                                      command=lambda: self.controller.show_page('StartPage'))
        self._back_btn.pack(side=RIGHT, padx=(0, 8))

        # Terminal
        self._build_terminal()

    def _build_terminal(self):
        term_wrap = Frame(self._right, bg=COLORS['terminal_bg'],
                          highlightthickness=1, highlightbackground='#2D4057')
        term_wrap.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        header = Frame(term_wrap, bg=COLORS['terminal_header_bg'])
        header.pack(fill=X)
        for color in ('#FF5F57', '#FEBC2E', '#28C840'):
            c = Canvas(header, width=8, height=8,
                       bg=COLORS['terminal_header_bg'], highlightthickness=0)
            c.pack(side=LEFT, padx=(8 if color == '#FF5F57' else 4, 0), pady=7)
            c.create_oval(0, 0, 8, 8, fill=color, outline='')
        Label(header, text='dataset.log', bg=COLORS['terminal_header_bg'],
              fg=COLORS['sidebar_steps_label'], font=('Courier', 10)).pack(side=LEFT, padx=10)

        self._log = Text(
            term_wrap, bg=COLORS['terminal_bg'], fg=COLORS['terminal_msg_norm'],
            font=('Courier', 11), state=DISABLED, wrap=CHAR, width=1,
            highlightthickness=0, relief='flat', padx=10, pady=8,
        )
        self._log.pack(fill=BOTH, expand=True)
        self._log.tag_config('ts',       foreground=COLORS['terminal_ts'])
        self._log.tag_config('tag_info', foreground=COLORS['terminal_tag_info'],  font=('Courier', 11, 'bold'))
        self._log.tag_config('tag_ok',   foreground=COLORS['terminal_tag_ok'],    font=('Courier', 11, 'bold'))
        self._log.tag_config('tag_err',  foreground=COLORS['terminal_tag_err'],   font=('Courier', 11, 'bold'))
        self._log.tag_config('msg_norm', foreground=COLORS['terminal_msg_norm'])
        self._log.tag_config('msg_ok',   foreground=COLORS['terminal_msg_ok'])
        self._log.tag_config('msg_err',  foreground=COLORS['terminal_msg_err'])

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def _on_visible(self, _event):
        self._done = False
        self._banner.pack_forget()
        self._path_row.pack_forget()
        self._clear_log()
        self._title_lbl.config(text='Preparing dataset…')
        self._back_btn.config(state=DISABLED)
        self._start_time = time.time()
        self._update_elapsed()
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        params = self.controller.get_prepare_params() or {}
        jar = resource_path('prepareDataset2RNA.jar')

        if params.get('mode') == 'training':
            self._out_dir = os.path.dirname(params.get('annotation', ''))
        else:
            self._out_dir = params.get('genbank', '')

        if params.get('mode') == 'training':
            cmd = [
                'java', '-jar', jar,
                '-a', params.get('annotation', ''),
                '-f', params.get('fasta', ''),
                '-g', params.get('genbank', ''),
            ]
        else:
            cmd = [
                'java', '-jar', jar,
                '-p', params.get('genbank', ''),
            ]

        self._log_line('[INFO]', 'Starting dataset preparation…', 'tag_info', 'msg_norm')

        try:
            env = os.environ.copy()
            extra_paths = '/opt/homebrew/opt/openjdk/bin:/usr/local/bin:/usr/bin'
            env['PATH'] = extra_paths + ':' + env.get('PATH', '')

            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env,
            )
            for line in self._process.stdout:
                line = line.rstrip()
                if not line:
                    continue
                if any(k in line.lower() for k in ('error', 'exception', 'failed')):
                    self._log_line('[ERR]', line, 'tag_err', 'msg_err')
                elif any(k in line.lower() for k in ('ok', 'success', 'generated', 'saved')):
                    self._log_line('[ OK ]', line, 'tag_ok', 'msg_ok')
                else:
                    self._log_line('[INFO]', line, 'tag_info', 'msg_norm')

            self._process.wait()

            if self._process.returncode == 0:
                self._log_line('[ OK ]', 'Dataset generated successfully.', 'tag_ok', 'msg_ok')
                self.after(0, self._on_success)
            else:
                self._log_line('[ERR]', f'Process exited with code {self._process.returncode}.',
                               'tag_err', 'msg_err')
                self.after(0, self._on_failure)

        except FileNotFoundError:
            self._log_line('[ERR]', 'Java not found. Please install Java and try again.',
                           'tag_err', 'msg_err')
            self.after(0, self._on_failure)
        except Exception as e:
            self._log_line('[ERR]', str(e), 'tag_err', 'msg_err')
            self.after(0, self._on_failure)

    def _on_success(self):
        self._done = True
        elapsed = int(time.time() - self._start_time)
        m, s = elapsed // 60, elapsed % 60
        self._title_lbl.config(text='Dataset ready')
        self._banner_title.config(text='Dataset generated successfully')
        self._banner_sub.config(text=f'Total time: {m:02d}:{s:02d}')
        self._back_btn.config(state=NORMAL)

        self._banner.pack(fill=X, padx=20, pady=(0, 8), before=self._log.master)

        if self._out_dir:
            self._path_value_lbl.config(text=self._out_dir)
            self._path_row.pack(fill=X, padx=12, pady=(0, 10))

    def _on_failure(self):
        self._done = True
        self._title_lbl.config(text='Preparation failed')
        self._back_btn.config(state=NORMAL)

    # ── Log helpers ───────────────────────────────────────────────────────────

    def _log_line(self, tag_text, msg, tag_style, msg_style):
        def _write():
            ts = time.strftime('%H:%M:%S')
            self._log.config(state=NORMAL)
            self._log.insert(END, ts + ' ', 'ts')
            self._log.insert(END, f'{tag_text} ', tag_style)
            self._log.insert(END, msg + '\n', msg_style)
            self._log.config(state=DISABLED)
            self._log.see(END)
        self.after(0, _write)

    def _clear_log(self):
        self._log.config(state=NORMAL)
        self._log.delete('1.0', END)
        self._log.config(state=DISABLED)

    def _update_elapsed(self):
        if self._done or self._start_time is None:
            return
        self.after(1000, self._update_elapsed)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _open_output_folder(self):
        if self._out_dir and os.path.exists(self._out_dir):
            subprocess.Popen(['open', self._out_dir])

    def _new_preparation(self):
        if self._process and self._process.poll() is None:
            self._process.terminate()
        self.controller.show_page('PrepareDataset')
