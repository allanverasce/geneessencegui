from tkinter import *

# Color stops: (progress_threshold, R, G, B)
_COLOR_STOPS = [
    (0,   239,  68,  68),   # red
    (50,  245, 158,  11),   # amber
    (100,  16, 185, 129),   # green
]


def _interpolate_color(progress):
    p = max(0, min(100, progress))
    for i in range(len(_COLOR_STOPS) - 1):
        t0, r0, g0, b0 = _COLOR_STOPS[i]
        t1, r1, g1, b1 = _COLOR_STOPS[i + 1]
        if t0 <= p <= t1:
            ratio = (p - t0) / (t1 - t0)
            r = int(r0 + (r1 - r0) * ratio)
            g = int(g0 + (g1 - g0) * ratio)
            b = int(b0 + (b1 - b0) * ratio)
            return f'#{r:02x}{g:02x}{b:02x}'
    return '#10B981'


class CircularProgressBar(Canvas):
    def __init__(self, parent, size=100, progress_color='blue', bg_color='lightgray',
                 track_color='#E2E8F0', done_color=None, thickness=10, **kwargs):
        super().__init__(parent, width=size, height=size, bg=bg_color,
                         highlightthickness=0, **kwargs)
        self.size = size
        self.radius = (size - thickness) // 2
        self.center = size // 2
        self.thickness = thickness
        self.progress_color = progress_color
        self.done_color = done_color or progress_color
        self.bg_color = bg_color
        self.track_color = track_color
        self.progress = 0
        self._draw_background_circle()

    def _draw_background_circle(self):
        self.create_oval(
            self.center - self.radius, self.center - self.radius,
            self.center + self.radius, self.center + self.radius,
            outline=self.track_color, width=self.thickness
        )

    def set_progress(self, progress):
        self.progress = min(max(progress, 0), 100)
        self._draw_progress_arc()

    def _draw_progress_arc(self):
        self.delete('progress_arc', 'progress_text')

        color = _interpolate_color(self.progress)

        if self.progress == 100:
            self.create_oval(
                self.center - self.radius, self.center - self.radius,
                self.center + self.radius, self.center + self.radius,
                outline=color, width=self.thickness, tags='progress_arc'
            )
        else:
            self.create_arc(
                self.center - self.radius, self.center - self.radius,
                self.center + self.radius, self.center + self.radius,
                start=90, extent=-360 * (self.progress / 100),
                style='arc', outline=color,
                width=self.thickness, tags='progress_arc'
            )

        y_pct = self.center - 7 if self.progress == 100 else self.center
        self.create_text(
            self.center, y_pct,
            text=f'{self.progress:.0f}%',
            font=('Arial', 16, 'bold'),
            fill=color,
            tags='progress_text'
        )
        if self.progress == 100:
            self.create_text(
                self.center, self.center + 10,
                text='COMPLETE',
                font=('Arial', 7),
                fill='#94A3B8',
                tags='progress_text'
            )
