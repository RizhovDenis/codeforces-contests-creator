import click

from apps.parser.cli import parser_group


@click.group()
def main_group():
    """A place for configure services """


if __name__ == "__main__":
    main_group.add_command(parser_group)

    main_group()

