
from db_setup import create_app

app = create_app()



@app.route('/')
def index():
    return 'test'


if __name__ == "__main__":
    app.run(debug=True)



