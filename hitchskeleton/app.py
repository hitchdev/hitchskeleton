from .template import website
import click


@click.group()
def cli():
    pass


cli.add_command(website)
