from flask import Flask, render_template
from twitter_trend import get_trend_data

app = Flask(__name__)


@app.route("/")
def index():
    trend = get_trend_data()
    return render_template("index.html", trend=trend)


if __name__ == "__main__":
    app.run()
