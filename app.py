from flask import Flask
from flask import request
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    getp = request.args.get("formula")
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    <p>Formula: {getp}</p>
    """.format(time=the_time, getp = getp)
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

