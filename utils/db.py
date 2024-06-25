import sqlalchemy as sa
import os

def get_connection(data_path):
    engine = sa.create_engine(f"sqlite:///{data_path}")
    connection = engine.connect()
    return engine, connection

def get_table(db='videodata.db'):
    db_path = os.path.join(os.getcwd(), db)
    engine, connection = get_connection(db_path)
    inspect = sa.inspect(engine)

    meta_data = sa.MetaData()
    meta_data.reflect(connection)

    if inspect.has_table("videodata"):
        data_table = meta_data.tables['videodata']
    else:
        data_table = sa.Table(
            "videodata",
            meta_data,
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("file_name", sa.String),
            sa.Column("location", sa.String),
            sa.Column("human", sa.Boolean),
            sa.Column("gender", sa.String),
            sa.Column("key_frames", sa.Integer),
            sa.Column("duration", sa.Float),
            sa.Column("fps", sa.Float),
            sa.Column("resolution", sa.String),
            sa.Column("action", sa.String)
        )
        meta_data.create_all(engine, checkfirst=True)
    return connection, data_table

def insert_data(connection, table, file_name, location, gender, key_frames, duration, fps, resolution, action, is_human_present):
    gender = ','.join(gender)
    resolution = ','.join(map(str, resolution))

    query = table.insert().values(
        file_name=file_name, 
        location=location,
        human=is_human_present,
        gender=gender,
        key_frames=key_frames,
        duration=duration,
        fps=fps,
        resolution=resolution,
        action=action
    )
    connection.execute(query)
    connection.commit()

def fetch_data(connection, table, location=None, gender=None, action=None):
    query = table.select()
    if location:
        query = query.where(table.c.location == location)
    if gender:
        query = query.where(table.c.gender.contains(gender))
    if action:
        query = query.where(table.c.action == action)
    result = connection.execute(query)
    return result.mappings().all()

def drop_table(connection):
    meta_data = sa.MetaData()
    meta_data.reflect(connection)
    meta_data.tables['videodata'].drop(connection, checkfirst=False)
