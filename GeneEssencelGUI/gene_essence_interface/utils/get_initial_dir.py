import os


def get_initial_dir() -> str:
    host_home = os.environ.get('HOST_HOME', '')
    if host_home and os.path.isdir(host_home):
        return host_home
    for candidate in ('/Users', '/home', '/mnt/c/Users', '/data'):
        if os.path.isdir(candidate) and os.listdir(candidate):
            return candidate
    return '/'
