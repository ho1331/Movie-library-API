from os import getenv


class Config:
    # WEB
    DEBUG = True
    TESTING = True

    # SQLAlchemy
    DB_HOST = getenv("DB_HOST")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    SECRET_KEY = getenv("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432"
    )

    # DOC
    SWAGGER = {"title": "Project documentation", "doc_dir": "./docs/"}
