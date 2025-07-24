from src.utils.logging import get_logger
import click

log = get_logger(__name__)

@click.group()
def cli():
    """Dependency Doctor CLI"""
    log.info("CLI started")
    pass

if __name__ == "__main__":
    cli() 