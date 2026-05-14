import sys

def write_progress(message, progress=None, callback=None):
    if progress is not None:
        if callback:
            callback(f"[PROGRESS] {progress}", progress)
        else:
            sys.stdout.write(f"[PROGRESS] {progress}\n")
            sys.stdout.flush()

    if callback:
        callback(f"[INFO] {message}", progress)
    else:
        sys.stdout.write(f"[INFO] {message}\n")
        sys.stdout.flush()
