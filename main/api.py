import requests, json
import datetime as dt
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

def daily_adjusted(api_key, ticker, mtype, market='USD') -> dict:
    '''
    api_key: Str
    ticker: Str
    mtype: Str
    market: Str
    This function takes in the API key and a given ticker (from Bombay Stock Exchange or Cryptocurrency), sends a GET request
    to the AlphaVantage API to return the required data in JSON format.
    '''
    url = "https://www.alphavantage.co/"
    query = f"query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={api_key}"         # BSE
    if mtype == 'Crypto':
        query =  f"query?function=DIGITAL_CURRENCY_DAILY&symbol={ticker}&market={market}&apikey={api_key}"        # Crypto
    query_url = url + query
    result = requests.get(query_url)
    json_result = json.loads(result.content)
    if mtype == 'Crypto':                                              # Crypto
        return json_result['Time Series (Digital Currency Daily)']
    return json_result['Time Series (Daily)']                          # BSE


def ticker_graph(api_key, ticker, no_of_days, parameter, real_parameter, mtype, market=None) -> None:
    '''
    api_key: Str
    ticker: Str
    no_of_days: Int
    parameter: Str
    mmtype: Str
    market: Str
    This function plots the data of the specific ticker given in Matplotlib using Pandas.
    '''
    data = daily_adjusted(api_key, ticker, mtype, market)
    end_date = dt.datetime.now().date()-dt.timedelta(days=1)
    start_date = end_date - dt.timedelta(days=no_of_days)
    period_in_str = []
    for i in range(0,no_of_days+1):
        date = str(start_date + dt.timedelta(days=i))
        if date in data.keys():
            period_in_str.append(date)
    ticker_price_int = [float(data[j][parameter]) for j in period_in_str]

    '''
    Format of the returned JSON data for BSE tickers:
    Parameters : 
    {'1. open', '2. high','3. low', '4. close', 
    '5. adjusted close', '6. volume', '7. dividend amount', '8. split coefficient'}

    Format of the returned JSON data for cryptocurrency coins:
    {'1a. open (CAD)', '1b. open (USD)', 
    '2a. high (CAD)', '2b. high (USD)', 
    '3a. low (CAD)', '3b. low (USD)', 
    '4a. close (CAD)', '4b. close (USD)', 
    '5. volume', '6. market cap (USD)'}
    '''

    df_dict = {'Date': period_in_str, 'Closing Price': ticker_price_int}
    df = pd.DataFrame(data=df_dict)
    # to see table after running : display(df)
    
    no_of_real_days = len(period_in_str)
    decider = [(no_of_real_days+1)/2, no_of_real_days/2][no_of_real_days%2==0]
    x_ticks = [0,int(decider),no_of_real_days]
    x_labels = [str(start_date + dt.timedelta(days=i)) for i in x_ticks] 

    plt.plot(df['Date'],df['Closing Price'])
    plt.title(ticker+" ("+real_parameter+")")
    plt.xlabel("Days")
    if mtype == 'BSE':
        plt.get_current_fig_manager().set_window_title(f"Trend Chart for {ticker[:-4]}")
        plt.ylabel("Stock Price")
    if mtype == 'Crypto':
        plt.get_current_fig_manager().set_window_title(f"Trend Chart for {ticker}")
        plt.ylabel("Price")
    plt.xticks(ticks=x_ticks, labels=x_labels)
    plt.autoscale(enable=False)
    plt.show()
