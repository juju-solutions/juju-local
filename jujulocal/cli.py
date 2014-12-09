import click

from .images import images_cli


@click.group()
def main():
    pass


main.add_command(images_cli)
