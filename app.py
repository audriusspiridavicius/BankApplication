from flask import render_template
from db_setup import app





@app.route('/')
def index():
    return render_template('homepage.html')



@app.route("/clients")
def clients():
    return render_template('clients.html')

@app.route("/banks")
def banks():
    return render_template('banks.html')





if __name__ == "__main__":
    app.run(debug=True)



