import os
import re
import click
import datetime
import logging

from clint.textui import (
    puts,
    colored,
)

from .helpers import sudo

log = logging.getLogger(__name__)


@click.command('images')
@click.option('--update', is_flag=True,
              help='update the cloud images currently cached')
@click.option('--clean', is_flag=True,
              help='remove all cached cloud images')
def images_cli(clean=False, update=False):  # pragma: no cover
    cur_images = cloud_images()
    if not cur_images:
        return puts('There are no LXC images cached')

    if clean:
        return clean_cloud_images(cur_images)

    for img in cur_images:
        age = datetime.datetime.now() - img['modified']
        color = colored.green
        if age.days > 30:
            color = colored.yellow
        if age.days > 90:
            color = colored.red
        puts(color("%s-%s-%s: %s days old" % (img['distro'], img['series'],
                                              img['arch'], age.days)))


def cloud_images():
    # unfortunately /var/cache/lxc is owned by root with 0o700
    # lets just never talk about the dirty things that are happening here.
    # maybe we should just let the user type "sudo juju local images"...
    scan = []
    files = []
    images = sudo('ls /var/cache/lxc/')
    if not images:
        return None

    for d in images.split('\n'):
        if 'cloud-' in d:
            targz = sudo('ls /var/cache/lxc/%s/' % d)
            if not targz:
                return None

            for f in targz.split('\n'):
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


def get_cloudimg(series):
    pass


def clean_cloud_images(images):
    for f in images:
        log.debug('Deleting %s' % f['path'])
        sudo('rm -f %s' % f['path'])


def parse_cloudimg(s):
    mt = '([a-z0-9]+)-([0-9.0-9]+)-(?:server|cloudimg|-)+([a-z0-9]+)(.*).gz$'
    m = re.search(mt, s)
    return (m.group(1), m.group(2), m.group(3)) if m else (None, None, None)
