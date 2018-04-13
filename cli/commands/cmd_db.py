import click

from sqlalchemy_utils import database_exists, create_database

from winejournal.app import create_app
from winejournal.extensions import db
from winejournal.data_models.users import User
from winejournal.data_models.categories import Category
from winejournal.data_models.regions import Region
from winejournal.data_models.wines import Wine

# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
def init(with_testdb):
    """
    Initialize the database.

    :param with_testdb: Create a test database
    :return: None
    """
    db.drop_all()
    db.create_all()

    if with_testdb:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(db_uri):
            create_database(db_uri)

    return None


@click.command()
def seed():
    """
    Seed the database with an initial user.

    :return: User instance
    """
    if User.find_by_identity(app.config['SEED_ADMIN_EMAIL']) is not None:
        return None

    user = User(
        role = 'admin',
        email = app.config['SEED_ADMIN_EMAIL'],
        password = app.config['SEED_ADMIN_PASSWORD']
    )
    category = Category(
        name='Red Blend',
        owner='1'
    )
    region = Region(
        name='Columbia Valley',
        owner='1'
    )
    wine = Wine(
        name='Test Wine',
        maker='Test Maker',
        vintage='2000',
        category='1',
        region='1',
        owner='1'
    )

    db.session.add(user)
    db.session.commit()
    db.session.add(category)
    db.session.commit()
    db.session.add(region)
    db.session.commit()
    db.session.add(wine)
    db.session.commit()

    return user


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
@click.pass_context
def reset(ctx, with_testdb):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init, with_testdb=with_testdb)
    ctx.invoke(seed)

    return None


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
