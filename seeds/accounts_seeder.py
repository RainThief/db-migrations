"""seeder module"""
import sqlalchemy as sa
from sqlalchemy import Table
from util.seeder import Seeder


class AccountsSeeder(Seeder):
    """Seed accounts table"""


    def run(self):
        """run seeding logic"""
        # SEED with SQL; simplicity over efficiency for seeding
        insert_person_sql = (
            "INSERT INTO accounts (username, password, email) VALUES ('{username}', '{password}', '{email}');"
        )
        for _ in range(100):
            self.conn.execute(sa.text(insert_person_sql.format(
                username=Seeder.create_unique('username', Seeder.faker.profile, ['username'])['username'],
                password=Seeder.faker.password(length=12),
                email=Seeder.create_unique('email', Seeder.faker.profile, ['mail'])['mail'],
            )))

        # SEED with alembic for declarative
        # use reflection
        accounts_table = Table('accounts', self.meta)
        # OR declare manually
        accounts_table = sa.table('accounts',
            sa.column('username', sa.String),
            sa.column('password', sa.String),
            sa.column('email', sa.String)
        )
        data = []
        for _ in range(100):
            data.append(
                {
                    'username': Seeder.create_unique('username', Seeder.faker.profile, ['username'])['username'],
                    'password': Seeder.faker.password(length=12),
                    'email': Seeder.create_unique('email', Seeder.faker.profile, ['mail'])['mail'],
                }
            )
        self.operation.bulk_insert(accounts_table, data)
