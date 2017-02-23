import pandas
import tushare as ts
import numpy as np
import collections

class BankAccount:
    def __init__(self, deposit,interest_rate=3):
        self.deposit = deposit
        self.balance = deposit        
    
    def show_bank_account(self):
        print "balance:¥{}".format(self.balance)

class StockAccount(BankAccount):
    def __init__(self, balance, interest_rate=3,trading_expense=0.2, initial_holdings={}):
        BankAccount.__init__(self, balance, interest_rate)
        self.trading_expense = trading_expense/100
        self.holdings = initial_holdings
        self.trading_history = {}
        
    def record_trading_history(function):
        def add_trading_history(self, stock_code, price, shares, date):
            self.trading_history[date] = self.trading_history.get(date, [])
            self.trading_history[date].append((function.func_name,stock_code, price,shares))
            return function(self, stock_code, price, shares, date)
        return add_trading_history
    
    @record_trading_history
    def buy(self, stock_code, price, shares, date):
        cost = price*shares*(1+self.trading_expense)
        self.balance = self.balance - cost
        self.holdings[stock_code] = self.holdings.get(stock_code, 0) + shares
    
    @record_trading_history
    def sell(self, stock_code, price,shares, date):
        self.holdings[stock_code] = self.holdings.get(stock_code, 0)
        self.holdings[stock_code] = self.holdings[stock_code] - shares
        self.balance = self.balance + price*shares*(1-self.trading_expense) 
    
    def check_stock_account(self, stock_price = {}):
        asset = sum([(stock_price[key]*value) for key,value in self.holdings.iteritems()])+self.balance
        self.show_bank_account()
        print 'holdings:{}'.format(self.holdings)
        print 'asset:¥{}'.format(asset)
        print 'P&L:¥{}'.format(asset - self.deposit)

class TradeSim: #class designed to handle all trading strategies
    def __init__(self, hist_prices, stock_acount ):
            self.hist_prices = hist_prices
            self.account = stock_acount
    
    def buy_sell(self, expected_price, market_price, date):
        shares_to_buy = 100*abs(expected_price - market_price)/market_price*100
        if shares_to_buy > 100:
            if expected_price > market_price:
                self.account.buy(stock_code, market_price, shares_to_buy, date)
            else:
                self.account.sell(stock_code, market_price,shares_to_buy, date)
        else:
            return

    def back_testing(self, start_date, end_date, target_stocks, expected_prices): # BackTesting on trading strategy
        for date in self.hist_prices[(self.hist_prices['date'] > start_date) & (self.hist_prices['date'] <= end_date)]['date']:
            market_price = self.hist_prices[self.hist_prices['code'] in target_stocks & date == self.hist_prices['date'] == date]
            expected_price = expected_prices[expected_price['date'] == date ]
            return map(lambda x: buy_sell(expected_price[x], market_price[x], date), target_stocks) #apply buy_sell on each stock