from app import create_app

app = create_app()


@app.route("/")
@app.route("/index")
def index():
    return "Hello, Pasha!"


if __name__ == "__main__":
    app.run()
