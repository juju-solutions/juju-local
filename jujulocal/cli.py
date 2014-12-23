import click
import logging

from .images import images_cli
from .suspend import suspend_cli, resume_cli


@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('-q', '--quiet', )
def main(quiet, verbose):
    pass


main.add_command(images_cli)
main.add_command(suspend_cli)
main.add_command(resume_cli)
