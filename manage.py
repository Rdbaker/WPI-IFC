#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script."""
import os
from glob import glob
from subprocess import call

from flask.ext.sqlalchemy import sqlalchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate, MigrateCommand
from flask_script import Command, Manager, Option, Server, Shell
from flask_script.commands import Clean, ShowUrls

import ifc.models as models
from ifc.app import create_app
from ifc.database import db
from ifc.settings import DevConfig, ProdConfig
from seeds import FRATERNITIES, ROLES

CONFIG = ProdConfig if os.environ.get('IFC_ENV') == 'prod' else DevConfig
HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')
CREATE_DB = 'create database %s'
DEFAULT_DB = 'postgres'

app = create_app(CONFIG)
manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """Return context dict for a shell session so you can access app, db, and the User model by default."""
    return {'app': app, 'db': db, 'models': models}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


class Lint(Command):
    """Lint and check code style with flake8 and isort."""

    def get_options(self):
        """Command line options."""
        return (
            Option('-f', '--fix-imports', action='store_true', dest='fix_imports', default=False,
                   help='Fix imports using isort, before linting'),
        )

    def run(self, fix_imports):
        """Run command."""
        skip = ['requirements']
        root_files = glob('*.py')
        root_directories = [name for name in next(os.walk('.'))[1] if
                            not name.startswith('.') and not name.startswith('migrations')]
        files_and_directories = [arg for arg in root_files + root_directories if arg not in skip]

        def execute_tool(description, *args):
            """Execute a checking tool with its arguments."""
            command_line = list(args) + files_and_directories
            print('{}: {}'.format(description, ' '.join(command_line)))
            rv = call(command_line)
            if rv is not 0:
                exit(rv)

        if fix_imports:
            execute_tool('Fixing import order', 'isort', '-rc')
        execute_tool('Checking code style', 'flake8')


@manager.command
def seed_db():
    """Seed the database with the initial data, this should only be run once per computer."""
    for role in ROLES:
        try:
            models.Role.create(**role)
            print "Role: " + role['title'] + " successfully created"
        except IntegrityError:
            db.session().rollback()
            print "Role: " + role['title'] + " already exists"
    for frat in FRATERNITIES:
        try:
            models.Fraternity.create(**frat)
            print "Fraternity: " + frat['title'] + " successfully created"
        except IntegrityError:
            db.session().rollback()
            print "Fraternity: " + frat['title'] + " already exists"


@manager.command
def setup_db():
    """Set up the local and test databases."""
    (base_uri, local_db) = app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)
    engine = sqlalchemy.create_engine('/'.join([base_uri, DEFAULT_DB]))
    conn = engine.connect()
    conn.execute('commit')
    conn.execute(CREATE_DB % local_db)
    conn.execute('commit')
    test_db = local_db + '_test'
    conn.execute(CREATE_DB % test_db)
    conn.close()


manager.add_command('server', Server(host='localhost', port=5050))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command('urls', ShowUrls())
manager.add_command('clean', Clean())
manager.add_command('lint', Lint())

if __name__ == '__main__':
    manager.run()
