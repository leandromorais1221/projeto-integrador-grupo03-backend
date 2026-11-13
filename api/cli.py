import click
from flask.cli import with_appcontext
from .database.seeder_db import populate_db


@click.command('db-seed')
@with_appcontext
def db_seed():
    populate_db()
    click.echo('Banco de dados populado com sucesso!')