import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time/<city>')
def get_time(city):
    if city == 'newyork':
        time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
        return str(time)
    elif city == 'seoul':
        time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        return str(time)

if __name__ == '__main__':
    app.run(debug=True, port=5000)