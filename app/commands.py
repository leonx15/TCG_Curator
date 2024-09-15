from flask.cli import with_appcontext
import click
from .__init__ import init_collections

@click.command('init-data')
@with_appcontext
def init_data_command():
    """Inicjalizuje dane z plików JSON."""
    init_collections()
    click.echo('Dane zostały zaimportowane.')
