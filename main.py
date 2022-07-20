import pandas as pd
import yfinance as yf


def get_corporation_actions(tickers: list) -> pd.DataFrame:
    tickers_dividends_result = list()

    result = yf.Tickers(tickers=tickers)
    for ticker in tickers:
        df = result.tickers.get(ticker).dividends
        df = df.reset_index()
        df = df[(df['Date'] >= '2020-01-01') & (df['Date'] <= '2022-12-31')]
        df_mean = df['Dividends'].mean()
        df_sum = df.sum()
        tickers_dividends_result.append({
            "ticker": ticker,
            "mean": df_mean,
            "dividends2years": df_sum['Dividends']
        })

    return pd.DataFrame(tickers_dividends_result)


def get_current_price(ticker) -> float:
    result = yf.download(ticker, period='1d')
    return result['Adj Close']


def calculate_max_price(dividends: float, perc_year: float) -> float:
    return dividends / perc_year


def handler():
    perc_year = 0.06

    tickers = ["SYNE3.SA", "PETR4.SA", "BRAP4.SA", "MRFG3.SA", "BRKM5.SA"]
    df = get_corporation_actions(tickers)
    df['currentPrice'] = df.apply(lambda x: get_current_price(x['ticker']), axis=1)
    df['maxPrice'] = df.apply(lambda x: calculate_max_price(x['mean'], perc_year), axis=1)
    print(df.to_dict(orient="records"))


handler()