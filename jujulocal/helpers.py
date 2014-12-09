import subprocess


def _as_text(bytestring):
    """Naive conversion of subprocess output to Python string"""
    return bytestring.decode('utf-8', 'replace')


def do(cmd, env=None, su=False):
    shell = False
    if isinstance(cmd, str):
        cmd = cmd.split(' ')

    if su:
        cmd = ['sudo'] + cmd
        cmd = ' '.join(cmd)
        shell = True

    try:
        p = subprocess.Popen(cmd, env=env, shell=shell, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise OSError(2, 'cmd not found, do you have %s installed?' % cmd[0])
    out, err = p.communicate()
    if p.returncode:
        raise IOError('cmd command failed {!r}:\n'
                      '{}'.format(cmd, _as_text(err)))
    return _as_text(out) if out else None


def sudo(cmd, env=None):
    return do(cmd, env=env, su=True)
