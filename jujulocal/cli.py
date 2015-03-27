import click
import logging

from .images import images_cli
from .suspend import suspend_cli, resume_cli

logging.basicConfig()
log = logging.getLogger('jujulocal')


@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet', is_flag=True)
def main(quiet, verbose):
    if quiet:
        log.setLevel(logging.CRITICAL)
    if verbose:
        log.setLevel(logging.INFO - (verbose * 10))


main.add_command(images_cli)
main.add_command(suspend_cli)
main.add_command(resume_cli)
