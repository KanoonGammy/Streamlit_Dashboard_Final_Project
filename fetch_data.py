import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time

data_stock = pd.read_csv("https://raw.githubusercontent.com/KanoonGammy/Technical-Analysis-Project/refs/heads/main/SET_Index.csv", index_col = "Unnamed: 0")
 
data_stock['symbol'] = data_stock.symbol.apply(lambda x: f"{x}.BK")
tickers = data_stock['symbol'].tolist()
tickers.append("^SET.BK")

data = yf.download(tickers ,start = datetime.now() - timedelta(3650))
data['Close'].to_csv("source_price.csv")
data['Volume'].to_csv("source_volume.csv")
data.to_csv("multi-index.csv")

dict_mkt = {}
for tick in tickers:
    try:
        marketCap = yf.Ticker(tick).info.get("marketCap")
        dict_mkt[tick] = marketCap 
        time.sleep(0.0001)
    except Exception as e:
        print(f"Error fetching data for {tick}: {e}")
        dict_mkt[tick] = None
        
mkt = pd.DataFrame.from_dict(dict_mkt, orient= "index", columns = ["MarketCap"])
mkt.to_csv("source_mkt.csv")
# data.to_csv(f"{datetime.now():%Y-%m-%d}.csv")

print("finish")


