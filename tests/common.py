from sqlalchemy import orm

Session = orm.scoped_session(orm.sessionmaker())
# from https://factoryboy.readthedocs.io/en/stable/orms.html#managing-sessions
