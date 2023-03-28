from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objs as go
import json

app = Flask(__name__)
IEX_API_KEY = 'sk_66c5b940a5d4481bab434ac6a181d1bc'
ALPHA_VANTAGE_API_KEY = '2NCTE8B6PKTKD323'

BASE_URL = 'https://cloud.iexapis.com/stable'


def get_stock_data(ticker):
    endpoint = f'{BASE_URL}/stock/{ticker}/chart/1m?token={IEX_API_KEY}'
    response = requests.get(endpoint)
    
    try:
        data = response.json()
    except json.JSONDecodeError:
        return "Invalid or empty response from API"

    if data and 'date' in data[0]:
        df = pd.DataFrame(data)

        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df['date'], open=df['open'], high=df['high'], low=df['low'], close=df['close'],
                                      name=ticker))
        fig.update_layout(title=f'{ticker} Stock Price')

        return fig.to_html()
    else:
        return "Date key not found in the data"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symbols', methods=['GET'])
def symbols():
    query = request.args.get('query')
    endpoint = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(endpoint)
    data = response.json()
    return jsonify(data['bestMatches'])


@app.route('/stock', methods=['GET'])
def stock():
    ticker = request.args.get('ticker')
    graph_html = get_stock_data(ticker)
    return graph_html

if __name__ == '__main__':
    app.run(debug=True)