import re
import os
import time
import click
import logging
import datetime
from dateutil.parser import parse as dateparse

from clint.textui import (
    puts,
    colored,
)

from .helpers import sudo

log = logging.getLogger(__file__)


@click.command('templates')
@click.option('--upgrade', is_flag=True,
              help='run dist-upgrade on specified series')
@click.option('--rebuild', is_flag=True,
              help='rebuild template from cloudimg')
def templates_cli(rebuild, upgrade):
    containers = LocalLXC.containers('juju-.*-template')
    if upgrade:
        for c in containers:
            c.run('apt-get update')
            c.run('apt-get dist-upgrade -y')
        return
    if rebuild:
        return puts("Sorry, I'm lazy so this isn't implemented yet")
    for c in containers:
        color = colored.green
        output = str(c)
        if c.age().days > 5:
            color = colored.yellow
        if c.age().days > 10:
            color = colored.red
        if c.state == 'RUNNING':
            color = colored.red
            output = "%s (%s)" % (output, c.state)

        puts(color(output))


# Yes, LXC has a library - Juju and LXC require sudo to interact. This sucks.
class LXC(object):
    def __init__(self, name):
        self._load(name)

    @classmethod
    def containers(cls, match='.*'):
        cs = sudo('lxc-ls')
        if not cs:
            return None

        names = cs.split('\n')

        return [cls(c) for c in names if c and re.match(match, c) is not None]

    def _load(self, name):
        output = sudo('lxc-ls --fancy -F name,state,ipv4,ipv6,pid %s' % name)
        output = output.split('\n')
        if len(output) < 2:
            raise Exception('Not a valid LXC container')

        data = ' '.join(output[2].split()).split(' ')
        self.name = data[0]
        self.state = data[1]
        self.ipv4 = data[2]
        self.ipv6 = data[3]
        self.pid = data[4]

    def sync(self):
        self._load(self.name)

    def run(self, cmd):
        shutdown = False
        if self.state != 'RUNNING':
            shutdown = True
            self.start()
            time.sleep(10)

        out = sudo('lxc-attach -n %s -- %s' % (self.name, cmd))

        if shutdown:
            self.stop()

        return out

    def start(self):
        if self.state == 'RUNNING':
            return True

        sudo('lxc-start -n %s -d' % self.name)
        self.sync()

    def read(self, f):
        fpath = self.filepath(f)
        try:
            contents = sudo('cat %s' % fpath)
        except IOError:
            raise IOError('file not found: %s' % fpath)

        return contents

    def filepath(self, f):
        return '/var/lib/lxc/%s/rootfs/%s' % (self.name, f)

    def stop(self):
        if self.state == 'STOPPED':
            return True

        sudo('lxc-stop -n %s' % self.name)
        self.sync()

    def __str__(self):
        return '%s (%s) %s %s' % (self.pid, self.name, self.state, self.ipv4,
                                  self.ipv6)


class LocalLXC(LXC):
    def _load(self, name):
        super(LocalLXC, self)._load(name)

        updatef = self.filepath('/var/lib/apt/periodic/update-success-stamp')
        self.updated = dateparse(sudo('stat -c %%y %s' % updatef).strip())

    def age(self):
        return datetime.datetime.now(tz=self.updated.tzinfo) - self.updated

    def __str__(self):
        return '%s: %s days since update' % (self.name, self.age().days)
