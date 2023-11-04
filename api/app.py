from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import requests

app = Flask(__name__)

API = 'https://tradestie.com/api/v1/apps/reddit'


# home route
@app.route("/")
def index():
    header = "Top 50 Stocks discussed on \WallstreetBets"

    data = requests.get(API).json()
    dict = {}

    dict["Number of Comments"] = []
    dict["Sentiment"] = []
    dict["Sentiment Score"] = []
    dict["Ticker"] = []

    bullish_stocks = 0
    bearish_stocks = 0

    for x in data:
        dict["Ticker"].append(x['ticker'])
        dict["Number of Comments"].append(x['no_of_comments'])
        dict["Sentiment"].append(x['sentiment'])
        if x["sentiment"] == "Bullish":
            bullish_stocks += 1
        else:
            bearish_stocks += 1
        dict["Sentiment Score"].append(x['sentiment_score'])

    df = pd.DataFrame(dict)
    fig = px.bar(df,
                 x="Ticker",
                 y="Number of Comments",
                 hover_data=['Sentiment Score'],
                 color="Sentiment",
                 text_auto=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', data=data, header=header, graphJSON=graphJSON, bullish_stocks=bullish_stocks, bearish_stocks=bearish_stocks)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
