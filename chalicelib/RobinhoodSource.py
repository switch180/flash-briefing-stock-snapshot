import logging
from Robinhood import Robinhood
from chalicelib.AlexaResponse import AlexaResponse
logger = logging.getLogger('my-app')

'''
https://github.com/Jamonek/Robinhood
'''
class RobinhoodSource(object):
    def __init__(self, stock, stock_friendly_name, r_username, r_password):
        self.stock = stock
        self.stock_friendly_name = stock_friendly_name
        self.r_username = r_username
        self.r_password = r_password
        self.my_trader = Robinhood()
        logged_in = self.my_trader.login(username=self.r_username, password=self.r_password)
        if not logged_in:
            raise Exception("Failed to login")
        self.quote = self.my_trader.quote_data(self.stock)


    def set_position(self, avg_price, shares, unvested_shares):
        self.avg_price = avg_price
        self.shares = shares
        self.unvested_shares = unvested_shares


    @property
    def quote(self):
        return self.robinhood_quote


    @quote.setter
    def quote(self, robinhood_quote_dict):
        self.robinhood_quote = RobinhoodQuote(robinhood_quote_dict)


    def get_response(self):
        slugs = {
            'last_trade_price': float(self.quote.last_trade_price),
            'previous_close': float(self.quote.previous_close),
            'stock_friendly_name':  self.stock_friendly_name
        }
        slugs['stock_percent_change'] = 100.0 * ((slugs['last_trade_price'] - slugs['previous_close']) / slugs['previous_close'])
        slugs['stock_percent_change_abs'] = abs(slugs['stock_percent_change'])
        slugs['stock_up_down'] = 'up' if slugs['stock_percent_change'] > 0.0 else 'down'
        ar = AlexaResponse(slugs, preamble='From Robinhood')
        ar.add_blurb("{stock_friendly_name} stock is {stock_up_down} {stock_percent_change_abs:.1f}%, trading at ${last_trade_price:.0f}")
        ar.set_title(ar.get_blurbs()[0])
        if set(['avg_price', 'unvested_shares', 'shares']).intersection(dir(self)):
            slugs['portfolio_percent_change'] = 100 * ((slugs['last_trade_price'] - self.avg_price) / self.avg_price)
            slugs['portfolio_percent_change_abs'] = abs(slugs['portfolio_percent_change'])
            slugs['portfolio_up_down'] = 'up' if slugs['portfolio_percent_change'] > 0.0 else 'down'
            slugs['portfolio_vested_value'] = float(self.shares) * slugs['last_trade_price']
            slugs['portfolio_potential_value'] = (self.shares + self.unvested_shares) * slugs['last_trade_price']
            ar.add_blurb("You are {portfolio_up_down} {portfolio_percent_change_abs:.1f}" +
                " percent with a total value of approximately ${portfolio_vested_value:0.0f}" +
                " and a potential value of ${portfolio_potential_value:0.0f} if all shares vest")
        return ar


class RobinhoodQuote():
    _attrs = ['previous_close', 'has_traded', 'trading_halted', 'updated_at',
        'bid_price', 'last_trade_price', 'last_extended_hours_trade_price',
        'adjusted_previous_close', 'ask_price', 'instrument', 'last_trade_price_source',
        'ask_size', 'previous_close_date', 'symbol', 'bid_size']
    def __init__(self, quote):
        for name, value in quote.items():
            if name in dir(self):
                setattr(self, name, value)
    def __dir__(self):
        return self._attrs
    def __getattr__(self, name):
        if name in dir(self):
            return None
        else:
            raise AttributeError('{} does not exist'.format(name))
