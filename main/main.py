from dotenv import load_dotenv
import os, requests, json
import datetime as dt
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import tkinter as tkn

load_dotenv()
api_key = os.getenv("API_KEY")

def daily_adjusted(api_key,ticker):
        url = "https://www.alphavantage.co/"
        query = f"query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={api_key}"
        query_url = url + query
        result = requests.get(query_url)
        json_result = json.loads(result.content)
        return json_result['Time Series (Daily)']

def stock_graph(api_key, ticker, no_of_days,parameter,real_parameter):
    data = daily_adjusted(api_key, ticker)
    end_date = dt.datetime.now().date()-dt.timedelta(days=1)
    start_date = end_date - dt.timedelta(days=no_of_days)
    period_in_str = []
    for i in range(0,no_of_days+1):
        date = str(start_date + dt.timedelta(days=i))
        if date in data.keys():
            period_in_str.append(date)
    stock_price_int = [float(data[j][parameter]) for j in period_in_str]

    #  Parameters : {'1. open', '2. high', '3. low', '4. close', '5. adjusted close', '6. volume', '7. dividend amount', '8. split coefficient'}
    
    df_dict = {'Date': period_in_str, 'Closing Price': stock_price_int}
    df = pd.DataFrame(data=df_dict)

    # to see table after running : display(df)
    
    no_of_real_days = len(period_in_str)
    decider = [(no_of_real_days+1)/2, no_of_real_days/2][no_of_real_days%2==0]
    x_ticks = [0,int(decider),no_of_real_days]
    x_labels = [str(start_date + dt.timedelta(days=i)) for i in x_ticks] 

    plt.plot(df['Date'],df['Closing Price'])
    plt.title(ticker+" ("+real_parameter+")")
    plt.xlabel("Days")
    plt.ylabel("Stock Price")
    plt.xticks(ticks=x_ticks, labels=x_labels)
    plt.autoscale(enable=False)
    plt.show()

def crypto_daily_data(api_key,crypto_symbol,market):
    query_url =  f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={crypto_symbol}&market={market}&apikey={api_key}"
    result = requests.get(query_url)
    json_result = json.loads(result.content)
    return json_result['Time Series (Digital Currency Daily)']

def parameter_crypto_graph(api_key, crypto_symbol, market, no_of_days,parameter,real_parameter):
    data = crypto_daily_data(api_key,crypto_symbol,market)
    end_date = dt.datetime.now().date()-dt.timedelta(days=1)
    start_date = end_date - dt.timedelta(days=no_of_days)
    period_in_str = []
    for i in range(0,no_of_days+1):
        date = str(start_date + dt.timedelta(days=i))
        if date in data.keys():
            period_in_str.append(date)
    crypto_price_int = [float(data[j][parameter]) for j in period_in_str]

    '''
    {'1a. open (CAD)', '1b. open (USD)', 
    '2a. high (CAD)', '2b. high (USD)', 
    '3a. low (CAD)', '3b. low (USD)', 
    '4a. close (CAD)', '4b. close (USD)', 
    '5. volume', '6. market cap (USD)'}'''

    df_dict = {'Date': period_in_str, 'Closing Price': crypto_price_int}
    df = pd.DataFrame(data=df_dict)

    # to see table after running : display(df)
    
    no_of_real_days = len(period_in_str)
    decider = [(no_of_real_days+1)/2, no_of_real_days/2][no_of_real_days%2==0]
    x_ticks = [0,int(decider),no_of_real_days]
    x_labels = [str(start_date + dt.timedelta(days=i)) for i in x_ticks] 

    plt.plot(df['Date'],df['Closing Price'])
    plt.title(crypto_symbol+" ("+real_parameter+")")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.xticks(ticks=x_ticks, labels=x_labels)
    plt.autoscale(enable=False)
    plt.show()



def bse_process():
    def closing_graph():
        stock_ticker_extracted = bse_ticker.get()+'.BSE'
        period_extracted = int(period.get())
        bse_window.destroy()
        stock_graph(api_key, stock_ticker_extracted, period_extracted,'4. close','CLOSE')
    def high_graph():
        stock_ticker_extracted = bse_ticker.get()+'.BSE'
        period_extracted = int(period.get())
        bse_window.destroy()
        stock_graph(api_key, stock_ticker_extracted, period_extracted,'2. high','HIGH')
    def low_graph():
        stock_ticker_extracted = bse_ticker.get()+'.BSE'
        period_extracted = int(period.get())
        bse_window.destroy()
        stock_graph(api_key, stock_ticker_extracted, period_extracted,'3. low','LOW')
    window.destroy()
    bse_window = tkn.Tk()
    bse_window.geometry("500x500")
    bse_window.resizable(width=False, height=False)
    frame = tkn.Frame(master=bse_window)
    label_bse_ticker = tkn.Label(master=bse_window, text="Enter the desired BSE ticker:", height=1, width=21,anchor='w')
    label_bse_ticker.place(x=120, y=190)
    bse_ticker = tkn.Entry(master=bse_window, width=12)
    bse_ticker.place(x=281, y=190)
    label_period = tkn.Label(master=bse_window, text='''Enter the no.of days :
    (min=30, max=7500):''', height=2, width=18,anchor='w')
    label_period.place(x=130, y=215)
    period = tkn.Entry(master=bse_window, width=12)
    period.place(x=281, y=225)
    high_button = tkn.Button(master=bse_window, text="High", width=10, relief='raised',command=high_graph)
    high_button.place(x=111, y=260)
    low_button = tkn.Button(master=bse_window, text="Low", width=10, relief='raised',command=low_graph)
    low_button.place(x=201, y=260)
    closing_button = tkn.Button(master=bse_window, text="Closing", width=10, relief='raised', command=closing_graph)
    closing_button.place(x=291, y=260)
    frame.pack(pady=5)
    frame.pack_propagate(False)
    frame.configure(height=475, width=475, bg='grey')
    bse_window.mainloop()

def crypto_process():
    def closing_graph():
        crypto_symbol_extracted = crypto_symbol.get()
        market_currency_extracted=market_currency.get()
        period_extracted = int(period.get())
        parameter_for_query_api='4a. close '+'('+market_currency_extracted+')'
        real_parameter = 'CLOSE '+'(in '+market_currency_extracted+')'
        crypto_window.destroy()
        parameter_crypto_graph(api_key, crypto_symbol_extracted, market_currency_extracted, period_extracted,parameter_for_query_api,real_parameter)
    def high_graph():
        crypto_symbol_extracted = crypto_symbol.get()
        market_currency_extracted=market_currency.get()
        period_extracted = int(period.get())
        parameter_for_query_api='2a. high '+'('+market_currency_extracted+')'
        real_parameter = 'HIGH '+'(in '+market_currency_extracted+')'
        crypto_window.destroy()
        parameter_crypto_graph(api_key, crypto_symbol_extracted, market_currency_extracted, period_extracted,parameter_for_query_api,real_parameter)
    def low_graph():
        crypto_symbol_extracted = crypto_symbol.get()
        market_currency_extracted=market_currency.get()
        period_extracted = int(period.get())
        parameter_for_query_api='3a. low '+'('+market_currency_extracted+')'
        real_parameter = 'LOW '+'(in '+market_currency_extracted+')'
        crypto_window.destroy()
        parameter_crypto_graph(api_key, crypto_symbol_extracted, market_currency_extracted, period_extracted,parameter_for_query_api,real_parameter)
    def closing_usd_graph():
        crypto_symbol_extracted = crypto_symbol.get()
        market_currency_extracted=market_currency.get()
        period_extracted = int(period.get())
        parameter_for_query_api='4b. close (USD)'
        real_parameter = 'CLOSE '+'(in USD)'
        crypto_window.destroy()
        parameter_crypto_graph(api_key, crypto_symbol_extracted, market_currency_extracted, period_extracted,parameter_for_query_api,real_parameter)
    def high_usd_graph():
        crypto_symbol_extracted = crypto_symbol.get()
        market_currency_extracted=market_currency.get()
        period_extracted = int(period.get())
        parameter_for_query_api='2b. high (USD)'
        real_parameter = 'HIGH '+'(in USD)'
        crypto_window.destroy()
        parameter_crypto_graph(api_key, crypto_symbol_extracted, market_currency_extracted, period_extracted,parameter_for_query_api,real_parameter)
    def low_usd_graph():
        crypto_symbol_extracted = crypto_symbol.get()
        market_currency_extracted=market_currency.get()
        period_extracted = int(period.get())
        parameter_for_query_api='3b. low (USD)'
        real_parameter = 'LOW '+'(in USD)'
        crypto_window.destroy()
        parameter_crypto_graph(api_key, crypto_symbol_extracted, market_currency_extracted, period_extracted,parameter_for_query_api,real_parameter)
    window.destroy()
    crypto_window = tkn.Tk()
    crypto_window.geometry("500x500")
    crypto_window.resizable(width=False, height=False)
    frame = tkn.Frame(master=crypto_window)
    label_crypto_symbol = tkn.Label(master=crypto_window, text="Enter the crypto coin symbol:", height=1, width=22)
    label_crypto_symbol.place(x=116, y=155)
    crypto_symbol = tkn.Entry(master=crypto_window, width=12)
    crypto_symbol.place(x=281, y=155)
    label_market_currency = tkn.Label(master=crypto_window, text="Enter the market currency:", height=1, width=20)
    label_market_currency.place(x=124, y=183)
    market_currency = tkn.Entry(master=crypto_window, width=12)
    market_currency.place(x=281, y=183)
    label_period = tkn.Label(master=crypto_window, text='''Enter the no.of days :
(min=30, max=750)''', height=2, width=18)
    label_period.place(x=130, y=211)
    period = tkn.Entry(master=crypto_window, width=12)
    period.place(x=281, y=218)
    high_button = tkn.Button(master=crypto_window, text="High", width=10, relief='raised',command=high_graph)
    high_button.place(x=111, y=255)
    low_button = tkn.Button(master=crypto_window, text="Low", width=10, relief='raised',command=low_graph)
    low_button.place(x=201, y=255)
    closing_button = tkn.Button(master=crypto_window, text="Closing", width=10, relief='raised',command=closing_graph)
    closing_button.place(x=291, y=255)
    high_button_USD = tkn.Button(master=crypto_window, text="High (USD)", width=10, relief='raised',command=high_usd_graph)
    high_button_USD.place(x=111, y=290)
    low_button_USD = tkn.Button(master=crypto_window, text="Low (USD)", width=10, relief='raised',command=low_usd_graph)
    low_button_USD.place(x=201, y=290)
    closing_button_USD = tkn.Button(master=crypto_window, text="Closing (USD)", width=10, relief='raised',command=closing_usd_graph)
    closing_button_USD.place(x=291, y=290)
    frame.pack(pady=5)
    frame.pack_propagate(False)
    frame.configure(height=475, width=475, bg='grey')
    crypto_window.mainloop()


window = tkn.Tk()
window.geometry("500x500")
window.resizable(width=False, height=False)
frame = tkn.Frame(master=window)
label_asking = tkn.Label(master=window, text="What do you want to do?", width=22)
label_asking.place(x=175, y=205)
button_1 = tkn.Button(master=window, text="Crypto Coin Trends", width=15, relief='raised',command=crypto_process)
button_1.place(x=142, y=230)
button_2 = tkn.Button(master=window, text="BSE Stock Trends", width=15, relief='raised', command=bse_process)
button_2.place(x=260, y=230)
frame.pack(pady=5)
frame.pack_propagate(False)
frame.configure(height=475, width=475, bg='grey')
window.mainloop()