import click
import sys
from pathlib import Path
import os

sys.path.append(
    str(Path(os.path.abspath(os.path.dirname(__file__))))
)


@click.group()
def cli():
    pass


def main():
    cli()


if __name__ == '__main__':
    main()
