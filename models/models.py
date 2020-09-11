"""orm models"""
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base: sa.ext.declarative.api.DeclarativeMeta = declarative_base()


class Account(Base):
    """seed accounts table"""

    __tablename__ = 'accounts'

    user_id = sa.Column(sa.Integer, primary_key=True)

    username = sa.Column('username', sa.String)

    password = sa.Column('password', sa.String)

    email = sa.Column('email', sa.String)
