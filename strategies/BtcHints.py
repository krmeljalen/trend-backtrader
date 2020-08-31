import backtrader as bt

class BtcHints(bt.Strategy):
    params = (('period', 10), ('devfactor', 1),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.btc_price = self.datas[0].close
        self.google_sentiment = self.datas[1].close
        self.bbands = bt.indicators.BollingerBands(self.google_sentiment,
                period=self.params.period, devfactor=self.params.devfactor)

        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Existing order - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, 
                              order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None

    def next(self):
        # Check for open orders
        if self.order:
            return

        #Long signal 
        if self.google_sentiment > self.bbands.lines.top[0]:
            # Check if we are in the market
            if not self.position:
                self.log('Google Sentiment Value: %.2f' % 
                          self.google_sentiment[0])
                self.log('Top band: %.2f' % self.bbands.lines.top[0])
                # We are not in the market, we will open a trade
                self.log('***BUY CREATE, %.2f' % self.btc_price[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
                # Logging          

        #Short signal
        elif self.google_sentiment < self.bbands.lines.bot[0]:
            # Check if we are in the market
            if not self.position:
                self.log('Google Sentiment Value: %.2f' % 
                          self.google_sentiment[0])
                self.log('Bottom band: %.2f' % self.bbands.lines.bot[0])
                # We are not in the market, we will open a trade
                self.log('***SELL CREATE, %.2f' % self.btc_price[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                # Logging
        
        #Neutral signal - close any open trades     
        else:
            if self.position:
                # We are in the market, we will close the existing trade
                self.log('Google Sentiment Value: %.2f' % 
                          self.google_sentiment[0])
                self.log('Bottom band: %.2f' % self.bbands.lines.bot[0])
                self.log('Top band: %.2f' % self.bbands.lines.top[0])
                self.log('CLOSE CREATE, %.2f' % self.btc_price[0])
                self.order = self.close()
