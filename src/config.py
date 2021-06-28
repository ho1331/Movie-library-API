from os import getenv


class Config:
    DEBUG = True
    TESTING = True

    # SQLAlchemy
    DB_HOST = getenv("DB_HOST")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_DB = getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_DB}"
    )


