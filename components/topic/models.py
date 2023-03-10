from typing import List

import sqlalchemy as sq
from sqlalchemy.sql import text

from database.db_sync import Base, db_session


class Topic(Base):
    __tablename__: str = 'topics'

    id: int = sq.Column(sq.Integer, primary_key=True, autoincrement=True, nullable=False)
    problem_number: str = sq.Column(sq.String, sq.ForeignKey('problems.number'), nullable=False)
    name: str = sq.Column(sq.String, nullable=False)

    @classmethod
    def create(cls, number: str, name: str):
        params = {
            'number': number,
            'name': name
        }

        db_session.execute(
            text("""INSERT INTO topics (problem_number, name)
                    values (:number, :name)"""),
            params=params
        )

    @classmethod
    def is_in_table(cls, number: str, name: str):
        params = {
            'number': number,
            'name': name
        }

        return db_session.execute(
            text("""SELECT * FROM topics
                    WHERE problem_number = :number 
                    and name = :name"""),
            params=params
        ).fetchone()

    @classmethod
    def create_batch(cls, number: str, names: List[str]):
        for name in names:
            if not name:
                continue

            if not cls.is_in_table(number, name):
                cls.create(number, name)
