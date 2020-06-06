import datetime
import backtrader as bt
from strategies.BtcSentiment import BtcSentiment

cerebro = bt.Cerebro()

#Set data parameters and add to Cerebro
data = bt.feeds.GenericCSVData(
    # Date,Symbol,Open,High,Low,Close,Volume BTC,Volume USD
    dataname="data/btc_daily.csv",
    fromdate=datetime.datetime(2017, 1, 1),
    todate=datetime.datetime(2020, 6, 1),
    dtformat=('%Y-%m-%d'),
    datetime=0,
    open=2,
    high=3,
    low=4,
    close=5,
    volume=6,
    openinterest=-1,
    time=-1,
    timeframe=bt.TimeFrame.Days)

trends = bt.feeds.GenericCSVData(
    # Date,Trend
    dataname="data/btc_trends.csv",
    fromdate=datetime.datetime(2017, 1, 1),
    todate=datetime.datetime(2020, 6, 1),
    dtformat=('%Y-%m-%d'),
    datetime=0,
    close=1,
    open=-1,
    high=-1,
    low=-1,
    volume=-1,
    openinterest=-1,
    time=-1,
    timeframe=bt.TimeFrame.Days)

cerebro.adddata(data)
cerebro.adddata(trends)

cerebro.addstrategy(BtcSentiment)

if __name__ == '__main__':
    #Run Cerebro Engine
    start_portfolio_value = cerebro.broker.getvalue()
    print('Starting Portfolio Value: %.2f' % start_portfolio_value) 

    cerebro.run() 

    end_portfolio_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % end_portfolio_value) 

    pnl = end_portfolio_value - start_portfolio_value 
    print('PnL: %.2f' % pnl)
    cerebro.plot(style='candlestick',volume=False)
