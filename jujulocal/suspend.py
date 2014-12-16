import os
import click
import jujuclient

from clint.textui import (
    puts,
    colored,
)

from .helpers import sudo


@click.command('suspend')
@click.option('-e', envvar='JUJU_ENV', help='juju environment')
def suspend_cli(env=None):  # pragma: no cover
    try:
        suspend(env)
    except Exception as e:
        return puts(colored.red('Failed to suspend {}'.format(e))

    puts(colored.green('{} has been suspended'.format(env))



@click.command('resume')
@click.option('-e', envvar='JUJU_ENV', help='juju environment')
def resume_cli(env=None):  # pragma: no cover
    pass


def suspend(env)
    pass


def resume(env)
    pass
