import datetime
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
    data = bt.feeds.GenericCSVData(
        dataname='../data/cple6_v2.csv',

        fromdate=datetime.datetime(2020, 9, 21),
        todate=datetime.datetime(2021, 9, 17),

        nullvalue=0.0,

        dtformat=('%Y-%m-%d'),

        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1
    )
    cerebro.adddata(data)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Add Strategy
    cerebro.addstrategy(Strategy)
    results = cerebro.run(stdstats=False)

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()