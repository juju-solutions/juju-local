import os
import re
import click
import datetime

from .helpers import sudo


@click.command('images')
@click.option('--update', default=False,
              help='update the cloud images currently cached')
def images_cli(update=False):
    cur_images = cloud_images()
    click.echo(cur_images)


def cloud_images():
    # unfortunately /var/cache/lxc is owned by root with 0o700
    # lets just never talk about the dirty things that are happening here.
    # maybe we should just let the user type "sudo juju local images"...
    scan = []
    files = []
    for d in sudo('ls /var/cache/lxc/').split('\n'):
        if 'cloud-' in d:
            for f in sudo('ls /var/cache/lxc/%s/' % d).split('\n'):
                if f.endswith('.tar.gz'):
                    scan.append('/var/cache/lxc/%s/%s' % (d, f))
    for f in (sudo('stat -c "%Y %s %n" {}'.format(
            ' '.join(scan))).strip().split('\n')):
        timestamp, size, fp = f.split()
        archseries = parse_cloudimg(os.path.basename(fp))
        if not archseries[0]:
            continue
        mod = datetime.datetime.fromtimestamp(int(timestamp))
        files.append({'modified': mod,
                      'size': size,
                      'path': fp,
                      'arch': archseries[2],
                      'series': archseries[1],
                      'distro': archseries[0],
                      })
    return files


def parse_cloudimg(s):
    mt = '([a-z0-9]+)-([0-9.0-9]+)-(?:server|cloudimg|-)+([a-z0-9]+)(.*).gz$'
    m = re.search(mt, s)
    return (m.group(1), m.group(2), m.group(3)) if m else (None, None, None)
