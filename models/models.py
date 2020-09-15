"""orm models"""
import sqlalchemy as sa
from .base import Base


class Account(Base):
    """seed accounts table"""

    __tablename__ = 'accounts'

    user_id = sa.Column(sa.Integer, primary_key=True)

    username = sa.Column('username', sa.String)

    password = sa.Column('password', sa.String)

    email = sa.Column('email', sa.String)
