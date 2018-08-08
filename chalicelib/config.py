"""
Variables
 avg_price: average price of your position on one stock
 shares_held: how many shares you own, aka vested shares
 shares_awarded: how many shares have been awarded to you (e.g. RSUs, restricted stock, options) but you can't sell
 stock_symbol: stock symbol of one stock, sent to RH to retrieve a quote
 stock_friendly_name: nice name of the stock for Alexa to use
 private_path: the path where your function is that's signed by your RH password to provide a level of security. You should change this.
 rh_credentials: in Secrets Manager, the secret where your Robinhood credentials are stored. Should be reflexted in policy-dev.json in .chalice
"""
#TODO SSM parameter store
avg_price = 1000.0
shares_held = 2
shares_awarded = 20
stock_symbol = 'XYZ'
stock_friendly_name = 'Example Inc'
private_path = 'mklad89'
rh_credentials = 'dev/robinhood'
