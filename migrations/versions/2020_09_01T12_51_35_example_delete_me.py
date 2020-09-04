# disable linting errors caused by alembic auto generated code
# pylint: disable=invalid-name,missing-function-docstring,no-member
"""example delete me

Revision ID: 2020_09_01T12_51_35
Revises:
Create Date: 2020-09-01 12:51:35.147129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2020_09_01T12_51_35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.get_bind().execute("""
    CREATE TABLE accounts (
	    user_id serial PRIMARY KEY,
	    username VARCHAR ( 50 ) UNIQUE NOT NULL,
	    password VARCHAR ( 50 ) NOT NULL,
	    email VARCHAR ( 255 ) UNIQUE NOT NULL,
	    created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
        );
    """)
    seed()


def downgrade():
    op.get_bind().execute("DROP TABLE accounts")


def seed():
    insert_person_sql = (
        "INSERT INTO accounts (username, password, email) VALUES ('{username}', '{password}', '{email}');"
    )
    op.get_bind().execute(sa.text(insert_person_sql.format(
        username='MyUsername',
        password='MyPassword',
        email='MyEmail@email.com',
    )))
