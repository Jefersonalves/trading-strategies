from datetime import datetime
import backtrader as bt
import yfinance as yf


class KeltnerChannel(bt.Indicator):
    lines = ('mid', 'upper', 'lower')
    params = dict(
                ema=20,
                atr=0.5
                )

    plotinfo = dict(subplot=False)  # plot along with data
    plotlines = dict(
        mid=dict(ls='--'),  # dashed line
        upper=dict(_samecolor=True),  # use same color as prev line (mid)
        lower=dict(_samecolor=True),  # use same color as prev line (upper)
    )

    def __init__(self):
        self.l.mid = bt.ind.EMA(period=self.p.ema)
        self.l.upper = self.l.mid + bt.ind.ATR(period=self.p.ema) * self.p.atr
        self.l.lower = self.l.mid - bt.ind.ATR(period=self.p.ema) * self.p.atr


class Strategy(bt.Strategy):
    def __init__(self):
        self.keltner = KeltnerChannel()

    def next(self):
        if self.keltner.l.lower[0] > self.data[0]:
            self.buy()
        elif self.keltner.l.upper[0] < self.data[0]:
            self.sell()


if __name__ == '__main__':
    # Create cerebro instance
    cerebro = bt.Cerebro()

    # Add Benchmark
    # benchmark = get_security_data(BENCHMARK_TICKER, START, END)
    # benchdata = bt.feeds.PandasData(dataname=benchmark, name='SPY', plot=True)
    # cerebro.adddata(benchdata)
    data = bt.feeds.YahooFinanceCSVData(dataname='asset.csv')
    cerebro.adddata(data)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Add Strategy
    cerebro.addstrategy(Strategy)
    results = cerebro.run(stdstats=False)

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()