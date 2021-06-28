from app import create_app
from views.users_views import user

app = create_app()

app.register_blueprint(user)


if __name__ == "__main__":
    app.run()
