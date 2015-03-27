
import os
import yaml
import click

from clint.textui import (
    puts,
    colored,
)


@click.command('encrypted-home')
@click.option('--enable', is_flag=True,
              help='enable encrypted-home support for Juju')
@click.option('--disable', is_flag=True,
              help='disable encrypted-home support for Juju')
def encrypted_cli(disable=False, enable=False):  # pragma: no cover
    if home_is_encrypted():
        puts('You have an encrypted home directory, consider '
             'running with --enable')
    else:
        puts(colored.green('Your home directory is not encrypted.'))
        puts('You can still enable the work around if you would like to but '
             'it is not required')


def home_is_encrypted():
    return os.path.exists(os.path.join(os.path.expanduser('~'), '.ecryptfs'))


def move_root_dir():
    pass


def get_local_envs():
    local = []
    for env, data in load_environments().items():
        if data['type'] == 'local':
            local.append(env)

    return local


def load_environments():
    h = juju_home()
    envyaml = os.path.join(h, 'environments.yaml')
    if not os.path.is_file(envyaml):
        raise Exception('Whoa buddy, I think you need to run juju init first')

    with open(envyal) as f:
        yml = yaml.safe_load(f.read())

    return yml
