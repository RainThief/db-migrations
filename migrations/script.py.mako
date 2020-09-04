# disable linting errors caused by alembic code
# pylint: disable=invalid-name,missing-function-docstring,no-member
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op, context
${imports if imports else ""}

# import seeders and utils here

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    % if upgrades:
    ${upgrades}
    % endif
    seed()


def downgrade():
    ${downgrades if downgrades else "pass"}


def seed():
    pass
