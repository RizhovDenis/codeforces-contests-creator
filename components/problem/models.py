from typing import List

import sqlalchemy as sq
from sqlalchemy.sql import text

from database.db_sync import Base, db_session
from components.topic.models import Topic

from settings import proj_conf


class Problem(Base):
    __tablename__: str = 'problems'

    id: int = sq.Column(sq.Integer, primary_key=True, autoincrement=True, nullable=False)
    count_decided: int = sq.Column(sq.Integer, nullable=False)

    name: str = sq.Column(sq.String, nullable=False)
    number: str = sq.Column(sq.String, nullable=False, unique=True)
    complexity: int = sq.Column(sq.Integer)
    url: str = sq.Column(sq.String, nullable=False)

    @classmethod
    def create(
            cls,
            name: str,
            number: str,
            complexity: int,
            count_decided: int,
            url: str
    ):

        params = {
            'name': name,
            'number': number,
            'complexity': complexity,
            'count_decided': count_decided,
            'url': url
        }

        problem = db_session.execute(
            text("""INSERT INTO problems
                (count_decided, name, number, complexity,
                url)
                values(:count_decided, :name, :number, 
                :complexity, :url)
                RETURNING * """),
            params=params
        ).fetchone()

        return problem

    @classmethod
    def update(
            cls,
            number: str,
            count_decided: int
    ):
        params = {
            'number': number,
            'count_decided': count_decided
        }

        db_session.execute(
            text("""UPDATE problems
                SET count_decided = :count_decided
                WHERE number = :number
                RETURNING * """),
            params=params
        )

    @classmethod
    def is_in_table(cls, number: str):
        params = {'number': number}
        return db_session.execute(
            text("""SELECT * FROM problems
                    WHERE number = :number """),
            params=params
        ).fetchone()

    @classmethod
    def create_batch(
            cls,
            names: List[str],
            numbers: List[str],
            complexities: List[int],
            count_decided: List[int],
            urls: List[str],
            topics: List[list],
            length_batch: int
    ):

        for idx in range(length_batch):
            if cls.is_in_table(numbers[idx]):
                cls.update(numbers[idx], count_decided[idx])
            else:
                problem = cls.create(
                    names[idx],
                    numbers[idx],
                    complexities[idx],
                    count_decided[idx],
                    urls[idx]
                )

                contest = Contest.receive_free(complexities[idx], topics[idx])
                ContestProblem.create(contest.id, problem.id)
            Topic.create_batch(numbers[idx], topics[idx])

        db_session.commit()

    @classmethod
    def get_by_contest_id(cls, contest_id: int) -> List:
        return db_session.execute(
            text("""SELECT * FROM problems pr join contests_problems cp
                        on pr.id = cp.problem_id and cp.contest_id = :contest_id"""),
            params={'contest_id': contest_id}
        ).fetchall()


class Contest(Base):
    __tablename__: str = 'contests'

    id: int = sq.Column(sq.Integer, primary_key=True, autoincrement=True, nullable=False)
    is_full: bool = sq.Column(sq.BOOLEAN, nullable=False, server_default='False')
    complexity: int = sq.Column(sq.Integer)
    topic: str = sq.Column(sq.String, nullable=False)

    @classmethod
    def get_by_id(cls, idx: int) -> List:
        return db_session.execute(
            text("""SELECT * FROM contests
                    WHERE id = :idx"""),
            params={'idx': idx}
        ).fetchall()

    @classmethod
    def get_unique_topics(cls) -> List:
        return db_session.execute(
            text("""SELECT DISTINCT topic FROM contests
                    WHERE is_full is True
                    ORDER BY topic""")
        ).fetchall()

    @classmethod
    def get_by_topic(cls, topic: str) -> List:
        return db_session.execute(
            text("""SELECT DISTINCT complexity FROM contests 
                    WHERE is_full is True and topic = :topic
                    ORDER BY complexity"""),
            params={'topic': topic}
        ).fetchall()

    @classmethod
    def get_by_topic_and_complexity(cls, topic: str, complexity: int) -> List:
        return db_session.execute(
            text("""SELECT * FROM contests
                    WHERE topic = :topic and complexity = :complexity
                    ORDER BY id"""),
            params={'topic': topic, 'complexity': complexity}
        ).fetchall()

    @classmethod
    def create(cls, complexity: int, topic: str):
        params = {
            'complexity': complexity,
            'topic': topic
        }
        contest = db_session.execute(
            text("""INSERT INTO contests (complexity, topic)
                    values(:complexity, :topic)
                    RETURNING * """),
            params=params
        ).fetchone()

        return contest

    @classmethod
    def receive_free(cls, complexity: int, topics: List[str]):
        params = {
            'complexity': complexity,
            'topics': tuple(topics)
        }

        contest = db_session.execute(
            text("""SELECT *
                    FROM contests
                    WHERE is_full is False and topic in :topics and
                        complexity = :complexity
                    LIMIT 1"""),
            params=params
        ).fetchone()

        if not contest:
            contest = cls.create(complexity, topics[0])

        return contest


class ContestProblem(Base):
    __tablename__: str = 'contests_problems'
    __table_args__ = (
        sq.PrimaryKeyConstraint('contest_id', 'problem_id'),
    )

    contest_id: int = sq.Column(sq.Integer, sq.ForeignKey('contests.id'), nullable=False)
    problem_id: int = sq.Column(
        sq.Integer,
        sq.ForeignKey('problems.id'),
        nullable=False,
        unique=True
    )

    @classmethod
    def create(cls, contest_id: int, problem_id: int):
        params = {
            'contest_id': contest_id,
            'problem_id': problem_id
        }
        contest_problem = db_session.execute(
            text("""WITH ins as (
                        INSERT INTO contests_problems (contest_id, problem_id)
                        values(:contest_id, :problem_id)
                    )
                    SELECT COUNT(*) as count FROM contests_problems
                        WHERE contest_id = :contest_id """),
            params=params
        ).fetchone()

        if contest_problem.count + 1 == proj_conf.num_problems_in_contest:
            db_session.execute(
                text("""UPDATE contests SET is_full = True
                        WHERE id = :contest_id"""),
                params={'contest_id': contest_id}
            )

