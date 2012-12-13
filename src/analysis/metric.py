#!/usr/bin/env python
from __future__ import division

class Metrics:
  def __init__(self):
    self.neg_returns = {}
    self.pos_returns = {}
    self.periods = 0;
    self.day_neg_roc = {}
    self.day_pos_roc = {}
    self.tset = set()
    self.daily_roc = {} 

  def log_neg_returns(self, ticker, date, profit):
    self.tset.add(ticker)
    self.pos_returns.setdefault(ticker, [])
    self.pos_returns[ticker].append((date, profit))
  
  def log_pos_returns(self, ticker, date, profit):
    self.neg_returns.setdefault(ticker, [])
    self.tset.add(ticker)
    self.neg_returns[ticker].append((date, profit))
  
  def extend_period(self):
    self.periods = self.periods + 1
    
  def log_day_roc(self, ticker, roc):
    self.day_neg_roc.setdefault(ticker, [])
    self.day_pos_roc.setdefault(ticker, [])
    self.daily_roc.setdefault(ticker, [])
    self.daily_roc[ticker].append(roc)

    if roc > 0:
      self.day_pos_roc[ticker].append(roc)
    else:
      self.day_neg_roc[ticker].append(roc)
  
  def get_mae(self, ticker):
    time = len(self.pos_returns) + len(self.neg_returns)
    wins = losses = 0
    for pos in self.pos_returns[ticker]:
      wins = wins + pos[1]
    
    for pos in self.neg_returns[ticker]:
      losses = losses + pos[1]
    return  (1 / time) * (wins - losses)
  
  def find_mae(self):
    output = {}
    for ticker in self.tset:
      output[ticker] = self.get_mae(ticker)
    return output
  #TODO 
  def get_rmae(self, ticker):
    time = len(self.pos_returns) + len(self.neg_returns)
    wins = losses = 0
    for pos in self.pos_returns[ticker]:
      wins = wins + pos[1]
    
    for pos in self.neg_returns[ticker]:
      losses = losses + pos[1]
    return  (1 / time) * (wins - losses)
  #TODO
  def find_rmae(self):
    output = {}
    for ticker in self.tset:
      output[ticker] = self.get_mae(ticker)
    return output
  
  #FIX
  def get_mape(self, ticker):
    time = len(self.pos_returns) + len(self.neg_returns)
    wins = losses = 0
    for pos in self.pos_returns[ticker]:
      wins = wins + pos[1]
    
    for pos in self.neg_returns[ticker]:
      losses = losses + pos[1]
    return  (100 / time) * (wins - losses)
  
  #FIX
  def find_mape(self):
    output = {}
    for ticker in self.tset:
      output[ticker] = self.get_mape(ticker)
    return output
  
  def get_cdc(self, ticker):
    """Find correct directional change for ticker"""
    time = len(self.pos_returns) + len(self.neg_returns)
    return (100/time) * len(self.pos_returns)
  
  def get_max_dp(self, ticker):
    """Function returning max daily profit"""
    biggest = 0
    for d in elf.day_pos_roc[ticker]:
      biggest = max(biggest, d)
    return biggest

  def get_all_max_dp(self):
    output = {}
    for t in self.tset:
      output[t] = self.get_max_dp(t)
    return output

  def get_all_min_dp(self):
    output = {}
    for t in self.tset:
      output[t] = self.get_min_dp(t)
    return output

  def get_min_dp(self, ticker):
    """Function returning max daily profit"""
    smallest = 0
    for d in self.day_pos_roc[ticker]:
      smallest = max(smallest, d)
    return smallest

  def get_max_drawdown(self, ticker):
    memoi = []
    for d in range(len(self.daily_roc[ticker])):
      if d == 0:
        memoi.append((self.daily_roc[ticker][d], [self.daily_roc[ticker][d]]))
      elif memoi[d -1][0] + self.daily_roc[ticker][d] > self.daily_roc[ticker][d]:
        memoi.append((self.daily_roc[ticker][d], [self.daily_roc[ticker][d]])) 
      else:
        memoi.append((memoi[d-1][0] - self.daily_roc[ticker][d], memoi[d - 1][1]))
        memoi[d][1].append(self.daily_roc[ticker][d])
  
    maxdrawdown = 0
    for d in memoi:
      if d[0] < maxdrawdown:
        maxdrawdown = d[0]
    return maxdrawdown

  def get_all_drawdown(self):
    output = {}
    for t in self.tset:
      output[t] = self.get_max_drawdown(t)
    return output

  def get_num_winning_trade(self, ticker):
    wins = len(self.pos_returns)
    num_of_trades = wins + len(self.neg_returns)
    return 100 * (wins/num_of_trades)
 
  def get_all_win(self):
    output = {}
    for t in self.tset:
      output[t] = self.get_num_winning_trade(t)
    return output

  def get_num_losing_trade(self, ticker):
    wins = len(self.neg_returns)
    num_of_trades = wins + len(self.pos_returns)
    return 100 * (wins/num_of_trades)

  def get_all_losses(self):
    output = {}
    for t in self.tset:
      output[t] = self.get_num_losing_trade(t)
    return output

  def get_num_of_ups(self, ticker):
    return len(self.pos_returns[ticker])

  def get_num_of_downs(self, ticker):
    return len(self.neg_returns[ticker])

  def get_num_transactions(self, ticker):
    return len(self.neg_returns[ticker]) + len(self.pos_returns[ticker])
  
  def get_total_days(self, ticker):
    return len(self.daily_roc[ticker])

  def avg_gain(self, ticker):
    total = 0
    for pos in self.pos_returns[ticker]:
      total = total + pos[1]
    return total / self.get_num_of_ups(ticker)

  def avg_losses(self, ticker):
    total = 0 
    for pos in self.neg_returns[ticker]:
      total = total + pos[1]
    return total / self.get_num_of_downs(ticker)

  def get_gain_loss_ratio(self, ticker):
    return self.avg_gain(ticker) / self.avg_losses(ticker)

  def get_daily_rises(self, ticker):
    return len(self.day_pos_roc[ticker])

  def get_daily_losses(self, ticker):
    return len(self.day_neg_roc[ticker])
  

