from tkinter import Entry, Spinbox


def rounded_rect(canvas, x1, y1, x2, y2, r, **kw):
    """Desenha retângulo com cantos arredondados no Canvas."""
    points = [
        x1 + r, y1,   x2 - r, y1,
        x2,     y1,   x2,     y1 + r,
        x2,     y2 - r, x2,   y2,
        x2 - r, y2,   x1 + r, y2,
        x1,     y2,   x1,     y2 - r,
        x1,     y1 + r, x1,   y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kw)


_INPUT_TYPES = (Entry, Spinbox)


def update_bg(widget, bg):
    """Atualiza recursivamente o bg de frames/labels filhos, preservando inputs."""
    for child in widget.winfo_children():
        if not isinstance(child, _INPUT_TYPES):
            try:
                child.configure(bg=bg)
            except Exception:
                pass
        update_bg(child, bg)
