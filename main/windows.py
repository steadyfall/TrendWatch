import tkinter as tkn
from api import *

def bse_process(given_window, api_key):
    def parameter_decider(option_chosen, period, ticker_symbol):
        decider_dict = {"CLOSE":'4. close', 
                        "HIGH":'2. high',
                        "LOW":'3. low'}
        parameter_for_query_api = decider_dict[option_chosen]
        bse_window.destroy()
        ticker_graph(api_key, ticker_symbol+'.BSE', period, parameter_for_query_api, option_chosen, 'BSE')
    given_window.destroy()
    bse_window = tkn.Tk()
    bse_window.title("Trends for BSE Tickers")
    bse_window.geometry("500x500")
    bse_window.resizable(width=False, height=False)
    frame = tkn.Frame(master=bse_window)
    label_bse_ticker = tkn.Label(master=bse_window, text="Enter the desired BSE ticker:", height=1, width=21, justify='center')
    bse_ticker = tkn.Entry(master=bse_window, width=9)
    label_period = tkn.Label(master=bse_window, text="Enter the no.of days :\n(min=30, max=7500)", height=2, width=21, justify='center')
    period = tkn.Entry(master=bse_window, width=9)
    label_bse_ticker.place(x=140, y=190)
    bse_ticker.place(x=301, y=190)
    label_period.place(x=140, y=215)
    period.place(x=301, y=225)
    high_button = tkn.Button(master=bse_window, text="High", width=7, relief='raised',
                             command=lambda: parameter_decider("HIGH", int(period.get()), str(bse_ticker.get())))
    low_button = tkn.Button(master=bse_window, text="Low", width=7, relief='raised',
                            command=lambda: parameter_decider("LOW", int(period.get()), str(bse_ticker.get())))
    close_button = tkn.Button(master=bse_window, text="Closing", width=7, relief='raised',
                                command=lambda: parameter_decider("CLOSE", int(period.get()), str(bse_ticker.get())))
    high_button.place(x=131, y=260)
    low_button.place(x=221, y=260)
    close_button.place(x=311, y=260)
    frame.pack(pady=5)
    frame.pack_propagate(False)
    frame.configure(height=475, width=475, bg='grey')
    bse_window.mainloop()

def crypto_process(given_window, api_key):
    def parameter_decider(option_chosen, period, crypto_symbol, market_currency='USD'):
        decider_dict = {'CLOSE': '4a. close', 
                        'HIGH': '2a. high', 
                        'LOW': '3a. low', 
                        'CLOSE (in USD)': '4b. close (USD)', 
                        'HIGH (in USD)': '2b. high (USD)', 
                        'LOW (in USD)': '3b. low (USD)'}
        parameter_for_query_api = decider_dict[option_chosen]+' ('+market_currency+')'
        real_parameter = option_chosen+' (in '+market_currency+')'
        if market_currency == "":
            market_currency = 'USD'
        if market_currency == 'USD':
            parameter_for_query_api = decider_dict[option_chosen+' (in USD)']
            real_parameter = option_chosen+' (in USD)'
        crypto_window.destroy()
        ticker_graph(api_key, crypto_symbol, period, parameter_for_query_api, real_parameter, 'Crypto', market_currency)
    given_window.destroy()
    crypto_window = tkn.Tk()
    crypto_window.title("Trends for Crypto Coins")
    crypto_window.geometry("500x500")
    crypto_window.resizable(width=False, height=False)
    frame = tkn.Frame(master=crypto_window)
    label_crypto_symbol = tkn.Label(master=crypto_window, text="Enter the crypto coin symbol:", justify='center', height=1, width=22)
    crypto_symbol = tkn.Entry(master=crypto_window, width=10)
    label_market_currency = tkn.Label(master=crypto_window, text="Enter the market currency:", justify='center', height=1, width=22)
    market_currency = tkn.Entry(master=crypto_window, width=10)
    label_period = tkn.Label(master=crypto_window, text='Enter the no.of days : \n(min=30, max=750)', justify='center', height=2, width=22)
    period = tkn.Entry(master=crypto_window, width=10)
    label_crypto_symbol.place(x=136, y=155)
    crypto_symbol.place(x=301, y=155)
    label_market_currency.place(x=136, y=183)
    market_currency.place(x=301, y=183)
    label_period.place(x=136, y=211)
    period.place(x=301, y=218)
    high_button = tkn.Button(master=crypto_window, text="High", width=7, relief='raised',
                             command=lambda: parameter_decider('HIGH', int(period.get()), str(crypto_symbol.get()), str(market_currency.get())))
    low_button = tkn.Button(master=crypto_window, text="Low", width=7, relief='raised', 
                            command=lambda: parameter_decider('LOW', int(period.get()), str(crypto_symbol.get()), str(market_currency.get())))
    close_button = tkn.Button(master=crypto_window, text="Closing", width=7, relief='raised',
                              command=lambda: parameter_decider('CLOSE', int(period.get()), str(crypto_symbol.get()), str(market_currency.get())))
    high_button_USD = tkn.Button(master=crypto_window, text="High (USD)", width=10, relief='raised',
                                 command=lambda: parameter_decider('HIGH', int(period.get()), str(crypto_symbol.get())))
    low_button_USD = tkn.Button(master=crypto_window, text="Low (USD)", width=10, relief='raised',
                                command=lambda: parameter_decider('LOW', int(period.get()), str(crypto_symbol.get())))
    close_button_USD = tkn.Button(master=crypto_window, text="Closing (USD)", width=10, relief='raised',
                                  command=lambda: parameter_decider('CLOSE', int(period.get()), str(crypto_symbol.get())))
    high_button.place(x=131, y=255)
    low_button.place(x=221, y=255)
    close_button.place(x=311, y=255)
    high_button_USD.place(x=121, y=290)
    low_button_USD.place(x=211, y=290)
    close_button_USD.place(x=301, y=290)
    frame.pack(pady=5)
    frame.pack_propagate(False)
    frame.configure(height=475, width=475, bg='grey')
    crypto_window.mainloop()

def main_window(api_key):
    window = tkn.Tk()
    window.title("TrendWatch - Better Watch The Trend!")
    window.geometry("500x500")
    window.resizable(width=False, height=False)
    frame = tkn.Frame(master=window)
    label_asking = tkn.Label(master=window, text="What do you want to do?", width=22)
    button_1 = tkn.Button(master=window, text="Crypto Coin Trends", width=15, relief='raised',command=lambda: crypto_process(window, api_key))
    button_2 = tkn.Button(master=window, text="BSE Stock Trends", width=15, relief='raised', command=lambda: bse_process(window, api_key))
    label_asking.place(x=170, y=200)
    button_1.place(x=120, y=231)
    button_2.place(x=270, y=231)
    frame.pack(pady=5)
    frame.pack_propagate(False)
    frame.configure(height=475, width=475, bg='grey')
    window.mainloop()
