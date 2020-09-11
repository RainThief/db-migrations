"""seeder module"""
from typing import Dict
import sqlalchemy as sa
from sqlalchemy import Table
from util.seeder import Seeder
from models.models import Account


class AccountsSeeder(Seeder):
    """Seed accounts table"""


    def run(self) -> None:
        """run seeding logic"""
        # SEED with SQL; simplicity over efficiency for seeding
        insert_person_sql = (
            "INSERT INTO accounts (username, password, email) VALUES ('{username}', '{password}', '{email}');"
        )
        for _ in range(100):
            Seeder.connection.execute(sa.text(insert_person_sql.format(**self.account())))

        # SEED with alembic for declarative
        # use reflection
        accounts_table = Table('accounts', Seeder.meta)

        # OR declare manually
        accounts_table = sa.table('accounts',
            sa.column('username', sa.String),
            sa.column('password', sa.String),
            sa.column('email', sa.String)
        )
        data = []
        for _ in range(100):
            data.append(self.account())
        Seeder.operation.bulk_insert(accounts_table, data)

        # seed with reflected models
        accounts = self.base.classes.accounts
        session = self.create_session()
        session.bulk_save_objects([
            accounts(**self.account()),
        ])
        session.commit()

        # seed with declarative models
        session.bulk_save_objects([
            Account(**self.account()),
        ])
        session.commit()
        session.close()


    @staticmethod
    def account() -> Dict[str, str]:
        """create account dict"""
        return {
            'username': Seeder.create_unique('username', Seeder.faker.profile, ['username'])['username'],
            'password': Seeder.faker.password(length=12),
            'email': Seeder.create_unique('email', Seeder.faker.profile, ['mail'])['mail'],
        }
