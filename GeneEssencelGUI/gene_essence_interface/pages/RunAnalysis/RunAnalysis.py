import multiprocessing
import os
import subprocess
import sys
import threading
import time
from tkinter import *
from tkinter import messagebox

from gene_essence_engine.engine_launcher import run_engine_in_subprocess
from gene_essence_interface.config.colors import COLORS
from gene_essence_interface.database.queries.update_project_status import update_project_status
from gene_essence_interface.pages.components.CircularProgressBar import CircularProgressBar
from gene_essence_interface.pages.components.CustomButton import CustomButton
from gene_essence_interface.pages.components.NavigationSidebar import NavigationSidebar, STEPS_BY_TYPE, STEP_INDEX_BY_TYPE

BG = COLORS['background_alt']

PIPELINE_STEPS_BY_TYPE = {
    'training':   ['Load CSV', 'Normalize', 'Split Data', 'Train Models', 'Evaluate', 'Save Results', 'Deliver'],
    'prediction': ['Load CSV', 'Normalize', 'Predict', 'Save Results', 'Deliver'],
    'ensemble':   ['Load CSV', 'Normalize', 'Split Data', 'Aggregate Models', 'Evaluate', 'Save Results', 'Deliver'],
}

PROGRESS_PIPELINE_BY_TYPE = {
    'training':   [(0, 15, 0), (15, 30, 1), (30, 50, 2), (50, 80, 3), (80, 92, 4), (92, 97, 5), (97, 100, 6)],
    'prediction': [(0, 20, 0), (20, 65, 1), (65, 80, 2), (80, 95, 3), (95, 100, 4)],
    'ensemble':   [(0, 15, 0), (15, 30, 1), (30, 55, 2), (55, 80, 3), (80, 92, 4), (92, 97, 5), (97, 100, 6)],
}

INFO_CELLS_BY_TYPE = {
    'training':   ('Project', 'Type', 'Models', 'Metrics', 'Elapsed'),
    'prediction': ('Project', 'Type', 'Elapsed'),
    'ensemble':   ('Project', 'Type', 'Metrics', 'Elapsed'),
}


class RunAnalysis(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.parent = parent
        self.data_to_analyze = None
        self._analysis_done = False
        self._start_time = None
        self._current_pipeline_step = -1
        self._current_type = 'training'
        self._info_cells = {}
        self._pipe_icons = []
        self._pipe_labels = []

        self._sidebar = NavigationSidebar(self)
        self._sidebar.pack(side=LEFT, fill=Y)
        self._sidebar.set_active_step(6)

        self._right = Frame(self, bg=BG)
        self._right.pack(side=RIGHT, fill=BOTH, expand=True)

        self._build()
        self.bind('<Visibility>', self._on_visible)

    def on_show(self):
        t = self.controller.get_analyse_type() or 'Training'
        self._sidebar.reset_steps(STEPS_BY_TYPE[t])
        self._sidebar.set_active_step(STEP_INDEX_BY_TYPE[t]['RunAnalysis'])

    def _build(self):
        title_row = Frame(self._right, bg=BG)
        title_row.pack(fill=X, padx=20, pady=(16, 8))
        self._title_lbl = Label(title_row, text='Running analysis',
                                bg=BG, fg=COLORS['text'], font=('Arial', 16, 'bold'))
        self._title_lbl.pack(anchor=W)

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

        self._new_analysis_btn = CustomButton(top_row, text='+ New Analysis',
                                              variant='success',
                                              command=self.controller.start_new_analysis)
        self._new_analysis_btn.pack(side=RIGHT, padx=(10, 0))

        self._path_row = Frame(self._banner, bg='#F0FDF4',
                               highlightthickness=1, highlightbackground='#BBF7D0')
        Label(self._path_row, text='SAVED TO', bg='#F0FDF4', fg='#059669',
              font=('Arial', 9, 'bold')).pack(side=LEFT, padx=(10, 4), pady=6)
        self._path_value_lbl = Label(self._path_row, text='', bg='#F0FDF4',
                                     fg='#065F46', font=('Courier', 9), anchor=W)
        self._path_value_lbl.pack(side=LEFT, fill=X, expand=True, pady=6)
        CustomButton(self._path_row, text='Open Folder', font_size=9, variant='secondary',
                     command=self._view_results_action).pack(side=RIGHT, padx=(4, 10), pady=4)

        self._info_bar = Frame(self._right, bg=COLORS['card_bg'],
                               highlightthickness=1, highlightbackground=COLORS['card_border'])
        self._info_bar.pack(fill=X, padx=20, pady=(0, 8))

        run_area = Frame(self._right, bg=BG)
        run_area.pack(fill=BOTH, expand=True, padx=20, pady=(0, 4))

        self._build_terminal(run_area)
        self._build_right_panel(run_area)

    def _build_terminal(self, parent):
        term_wrap = Frame(parent, bg=COLORS['terminal_bg'],
                          highlightthickness=1, highlightbackground='#2D4057')
        term_wrap.pack(side=LEFT, fill=BOTH, expand=True)

        header = Frame(term_wrap, bg=COLORS['terminal_header_bg'])
        header.pack(fill=X)
        for color in ('#FF5F57', '#FEBC2E', '#28C840'):
            c = Canvas(header, width=8, height=8, bg=COLORS['terminal_header_bg'],
                       highlightthickness=0)
            c.pack(side=LEFT, padx=(8 if color == '#FF5F57' else 4, 0), pady=7)
            c.create_oval(0, 0, 8, 8, fill=color, outline='')
        self._term_title_lbl = Label(header, text='analysis.log', bg=COLORS['terminal_header_bg'],
                                     fg=COLORS['sidebar_steps_label'], font=('Courier', 10))
        self._term_title_lbl.pack(side=LEFT, padx=10)

        self.log_display = Text(
            term_wrap, bg=COLORS['terminal_bg'], fg=COLORS['terminal_msg_norm'],
            font=('Courier', 11), state=DISABLED, wrap=CHAR, width=1,
            highlightthickness=0, relief='flat', padx=10, pady=8,
            insertbackground=COLORS['primary']
        )
        self.log_display.pack(fill=BOTH, expand=True)

        self.log_display.tag_config('ts', foreground=COLORS['terminal_ts'])
        self.log_display.tag_config('tag_info', foreground=COLORS['terminal_tag_info'],
                                    font=('Courier', 11, 'bold'))
        self.log_display.tag_config('tag_ok', foreground=COLORS['terminal_tag_ok'],
                                    font=('Courier', 11, 'bold'))
        self.log_display.tag_config('tag_err', foreground=COLORS['terminal_tag_err'],
                                    font=('Courier', 11, 'bold'))
        self.log_display.tag_config('tag_warn', foreground=COLORS['terminal_tag_warn'],
                                    font=('Courier', 11, 'bold'))
        self.log_display.tag_config('msg_info', foreground=COLORS['terminal_msg_info'])
        self.log_display.tag_config('msg_ok', foreground=COLORS['terminal_msg_ok'])
        self.log_display.tag_config('msg_err', foreground=COLORS['terminal_msg_err'])
        self.log_display.tag_config('msg_norm', foreground=COLORS['terminal_msg_norm'])

    def _build_right_panel(self, parent):
        right_panel = Frame(parent, bg=BG, width=160)
        right_panel.pack(side=RIGHT, fill=Y, padx=(10, 0))
        right_panel.pack_propagate(False)

        ring_card = Frame(right_panel, bg=COLORS['card_bg'],
                          highlightthickness=1, highlightbackground=COLORS['card_border'])
        ring_card.pack(fill=X, pady=(0, 8))
        self.progress_bar = CircularProgressBar(ring_card, size=110,
                                                progress_color=COLORS['primary'],
                                                bg_color=COLORS['card_bg'],
                                                track_color=COLORS['border'],
                                                done_color=COLORS['success'],
                                                thickness=10)
        self.progress_bar.pack(padx=16, pady=12)

        self._pipe_card = Frame(right_panel, bg=COLORS['card_bg'],
                                highlightthickness=1, highlightbackground=COLORS['card_border'])
        self._pipe_card.pack(fill=X, pady=(0, 8))

        self._rebuild_pipeline_card('training')

    def _rebuild_info_bar(self, atype, data):
        for w in self._info_bar.winfo_children():
            w.destroy()
        self._info_cells = {}

        keys = INFO_CELLS_BY_TYPE.get(atype, INFO_CELLS_BY_TYPE['training'])
        for key in keys:
            cell = Frame(self._info_bar, bg=COLORS['card_bg'])
            cell.pack(side=LEFT, fill=X, expand=True, padx=12, pady=7)
            Label(cell, text=key.upper(), bg=COLORS['card_bg'],
                  fg='#94A3B8', font=('Arial', 10)).pack(anchor=W)
            val_lbl = Label(cell, text='—', bg=COLORS['card_bg'],
                            fg=COLORS['primary'] if key == 'Elapsed' else COLORS['text'],
                            font=('Arial', 12, 'bold'))
            val_lbl.pack(anchor=W)
            self._info_cells[key] = val_lbl
            if key != 'Elapsed':
                Frame(self._info_bar, bg=COLORS['card_border'],
                      width=1).pack(side=LEFT, fill=Y, pady=4)

        self._info_cells['Project'].config(text=data.get('project_name', '—'))
        self._info_cells['Type'].config(text=(data.get('analysis_type') or '').capitalize())
        if 'Models' in self._info_cells:
            models = data.get('selected_models') or []
            self._info_cells['Models'].config(text=str(len(models)) if models else '—')
        if 'Metrics' in self._info_cells:
            metrics = data.get('selected_metrics') or []
            self._info_cells['Metrics'].config(text=str(len(metrics)) if metrics else '—')
        self._info_cells['Elapsed'].config(text='00:00')

    def _rebuild_pipeline_card(self, atype):
        for w in self._pipe_card.winfo_children():
            w.destroy()

        Label(self._pipe_card, text='PIPELINE', bg=COLORS['card_bg'],
              fg='#94A3B8', font=('Arial', 9, 'bold')).pack(anchor=W, padx=10, pady=(8, 4))

        steps = PIPELINE_STEPS_BY_TYPE.get(atype, PIPELINE_STEPS_BY_TYPE['training'])
        self._pipe_icons = []
        self._pipe_labels = []
        for i, step in enumerate(steps):
            row = Frame(self._pipe_card, bg=COLORS['card_bg'])
            row.pack(fill=X, padx=10, pady=2)
            ic = Canvas(row, width=14, height=14, bg=COLORS['card_bg'], highlightthickness=0)
            ic.pack(side=LEFT, padx=(0, 6))
            lbl = Label(row, text=step, bg=COLORS['card_bg'],
                        fg=COLORS['pip_pending_fg'], font=('Arial', 10))
            lbl.pack(side=LEFT)
            self._pipe_icons.append(ic)
            self._pipe_labels.append(lbl)
            if i < len(steps) - 1:
                Frame(self._pipe_card, bg=COLORS['card_border'], width=1, height=5).pack(anchor=W, padx=16)

        Label(self._pipe_card, text='', bg=COLORS['card_bg']).pack(pady=(0, 4))
        self._render_pipeline(-1)

    def _render_pipeline(self, active_step):
        for i, (ic, lbl) in enumerate(zip(self._pipe_icons, self._pipe_labels)):
            ic.delete('all')
            if i < active_step:
                ic.create_oval(1, 1, 13, 13, fill=COLORS['pip_done_bg'], outline='')
                ic.create_text(7, 7, text='✓', fill=COLORS['pip_done_fg'], font=('Arial', 8, 'bold'))
                lbl.config(fg=COLORS['subtitle'], font=('Arial', 10))
            elif i == active_step:
                ic.create_oval(1, 1, 13, 13, fill=COLORS['pip_active_bg'], outline='')
                ic.create_text(7, 7, text='●', fill='white', font=('Arial', 8))
                lbl.config(fg=COLORS['text'], font=('Arial', 10, 'bold'))
            else:
                ic.create_oval(1, 1, 13, 13, fill=COLORS['pip_pending_bg'], outline='')
                lbl.config(fg=COLORS['pip_pending_fg'], font=('Arial', 10))

    def _advance_pipeline_from_message(self, msg):
        m = msg.lower()
        atype = self._current_type

        if any(k in m for k in ('csv', 'load', 'start')):
            step = 0
        elif 'normaliz' in m:
            step = 1
        elif atype == 'prediction':
            if 'predict' in m:
                step = 2
            elif 'sav' in m:
                step = 3
            elif any(k in m for k in ('email', 'zip', 'deliver', 'sent')):
                step = 4
            else:
                return
        else:
            if any(k in m for k in ('split', 'stratif')):
                step = 2
            elif any(k in m for k in ('train', 'aggregat', 'assembl')):
                step = 3
            elif any(k in m for k in ('predict', 'evaluat', 'metric')):
                step = 4
            elif 'sav' in m:
                step = 5
            elif any(k in m for k in ('email', 'zip', 'deliver', 'sent')):
                step = 6
            else:
                return

        if step > self._current_pipeline_step:
            self._current_pipeline_step = step
            self._render_pipeline(step)

    def _on_visible(self, event):
        self.data_to_analyze = self.controller.get_data_to_analyze()
        self._analysis_done = False
        self._current_pipeline_step = -1

        atype = (self.data_to_analyze.get('analysis_type') or 'training').lower()
        self._current_type = atype

        self._rebuild_info_bar(atype, self.data_to_analyze)
        self._rebuild_pipeline_card(atype)
        self.progress_bar.set_progress(0)
        self._banner.pack_forget()
        self._path_row.pack_forget()

        self._term_title_lbl.config(
            text=f"analysis.log — {self.data_to_analyze.get('project_name', '')}")

        self._start_time = time.time()
        self._update_elapsed()

        threading.Thread(target=self._start_analysis, daemon=True).start()

    def _start_analysis(self):
        self.update_log('[INFO] Starting analysis...')
        self.progress_bar.set_progress(10)
        try:
            self.queue = multiprocessing.Queue()
            self.process = multiprocessing.Process(
                target=run_engine_in_subprocess, args=(self.data_to_analyze, self.queue)
            )
            self.process.start()
            self.after(100, self._check_queue)
        except Exception as e:
            self.update_log(f'[ERROR] Failed to start analysis: {e}')
            self._on_done(error=True)

    def _check_queue(self):
        try:
            try:
                while not self.queue.empty():
                    item = self.queue.get_nowait()
                    if 'done' in item:
                        self.progress_bar.set_progress(100)
                        self._render_pipeline(len(self._pipe_icons))
                        self.update_log('[OK] Analysis completed successfully.')
                        update_project_status(
                            self.data_to_analyze['project_name'],
                            self.data_to_analyze['analysis_type'].capitalize(),
                            'Completed'
                        )
                        self._on_done()
                        return
                    if 'message' in item:
                        self.update_log(item['message'])
                    if 'progress' in item and item['progress'] is not None:
                        self.progress_bar.set_progress(item['progress'])
                        self._sync_pipeline_from_progress(item['progress'])
            except Exception:
                pass

            if not self.process.is_alive():
                if self.queue.empty():
                    if self.process.exitcode != 0:
                        self.update_log(
                            f'[ERROR] Process failed (exit code {self.process.exitcode}).')
                        self._on_done(error=True)
                    return

            self.after(100, self._check_queue)
        except Exception as e:
            self.update_log(f'[ERROR] Queue monitoring failed: {e}')
            self._on_done(error=True)

    def _sync_pipeline_from_progress(self, progress):
        pipeline = PROGRESS_PIPELINE_BY_TYPE.get(self._current_type, PROGRESS_PIPELINE_BY_TYPE['training'])
        for lo, hi, step in pipeline:
            if lo <= progress < hi and step > self._current_pipeline_step:
                self._current_pipeline_step = step
                self._render_pipeline(step)
                break

    def _extract_progress_value(self, msg):
        try:
            return int(msg.split('[PROGRESS]')[1].strip().replace('%', ''))
        except (IndexError, ValueError):
            return None

    def _on_done(self, error=False):
        self._analysis_done = True
        if not error:
            elapsed = int(time.time() - self._start_time)
            m, s = elapsed // 60, elapsed % 60
            self._banner_title.config(text='Analysis completed successfully')
            self._banner_sub.config(text=f'Total time: {m:02d}:{s:02d}')
            method = (self.data_to_analyze or {}).get('result_delivery_method', '')
            contact = (self.data_to_analyze or {}).get('delivery_contact', '')
            if method == 'local' and contact:
                project_dir = os.path.join(contact, 'GeneEssenceGUI',
                                           self.data_to_analyze['project_name'])
                self._path_value_lbl.config(text=project_dir)
                self._path_row.pack(fill=X, padx=12, pady=(0, 10))
            self._banner.pack(fill=X, padx=20, pady=(0, 8), before=self._info_bar)
            self._title_lbl.config(text='Analysis complete')
        self._enable_buttons()

    def _enable_buttons(self):
        pass

    def update_log(self, message):
        if '[PROGRESS]' in message:
            pv = self._extract_progress_value(message)
            if pv is not None:
                self.progress_bar.set_progress(pv)
                self._sync_pipeline_from_progress(pv)
            return

        ts = time.strftime('%H:%M:%S')
        self.log_display.config(state=NORMAL)
        self.log_display.insert(END, ts + ' ', 'ts')

        if '[INFO]' in message:
            msg = message.replace('[INFO]', '').strip()
            self.log_display.insert(END, '[INFO] ', 'tag_info')
            self.log_display.insert(END, msg + '\n', 'msg_info')
            self._advance_pipeline_from_message(msg)
        elif '[ERROR]' in message:
            msg = message.replace('[ERROR]', '').strip()
            self.log_display.insert(END, '[ERR]  ', 'tag_err')
            self.log_display.insert(END, msg + '\n', 'msg_err')
        elif '[OK]' in message or 'completed' in message.lower():
            msg = message.replace('[OK]', '').strip()
            self.log_display.insert(END, '[ OK ] ', 'tag_ok')
            self.log_display.insert(END, msg + '\n', 'msg_ok')
        elif '[WARN]' in message:
            msg = message.replace('[WARN]', '').strip()
            self.log_display.insert(END, '[WARN] ', 'tag_warn')
            self.log_display.insert(END, msg + '\n', 'msg_norm')
        else:
            self.log_display.insert(END, '[INFO] ', 'tag_info')
            self.log_display.insert(END, message + '\n', 'msg_norm')
            self._advance_pipeline_from_message(message)

        self.log_display.config(state=DISABLED)
        self.log_display.see(END)

    def _update_elapsed(self):
        if self._start_time is None:
            return
        elapsed = int(time.time() - self._start_time)
        if 'Elapsed' in self._info_cells:
            self._info_cells['Elapsed'].config(text=f'{elapsed // 60:02d}:{elapsed % 60:02d}')
        if not self._analysis_done:
            self.after(1000, self._update_elapsed)

    def _view_results_action(self):
        try:
            method = self.data_to_analyze.get('result_delivery_method', '')
            contact = self.data_to_analyze.get('delivery_contact', '')
            if method == 'email':
                messagebox.showinfo('Results', f'Results sent to: {contact}')
            elif method == 'local':
                project_dir = os.path.join(contact, 'GeneEssenceGUI',
                                           self.data_to_analyze['project_name'])
                if os.path.exists(project_dir):
                    self._open_directory(project_dir)
                else:
                    messagebox.showwarning('Not Found', f'Directory not found: {project_dir}')
            else:
                messagebox.showerror('Error', 'Unknown delivery method.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def _open_directory(self, path):
        try:
            if sys.platform == 'win32':
                os.startfile(path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', path], check=True)
            else:
                for cmd in ['pcmanfm', 'nautilus', 'thunar', 'xdg-open']:
                    try:
                        subprocess.run([cmd, path], check=True)
                        return
                    except FileNotFoundError:
                        continue
        except Exception as e:
            messagebox.showinfo('Directory', f'Results at: {path}\n\n{e}')
