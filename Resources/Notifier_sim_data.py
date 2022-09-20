# Import modules

import os
import pandas as pd
from datetime import datetime
from pycoingecko import CoinGeckoAPI

# Set Variable for coingecko API
cg = CoinGeckoAPI()

#BTC
#Pull data from coingecko and create DataFrame for historical data for simulation of app
btc_data = cg.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='usd',from_timestamp='1654041600',to_timestamp='1663286400')
btc_df = pd.DataFrame(btc_data['prices'], columns=['date', 'price']).set_index('date')
btc_df.index = pd.to_datetime(btc_df.index, unit='ms')

#Isolate most recent 14 day prices
btc_recent_df = btc_df.tail(14)

#Calculate pct_change, drop nan values and rename column to 24-hr change.
btc_recent_df = pd.DataFrame(btc_recent_df['price'].pct_change().dropna()).rename(columns={'price':'24_hr_change'})
btc_recent_df['24_hr_change'] = btc_recent_df['24_hr_change'] * 100

#ETH
#Pull data from coingecko and create DataFrame for historical data for simulation of app
eth_data = cg.get_coin_market_chart_range_by_id(id='ethereum',vs_currency='usd',from_timestamp='1654041600',to_timestamp='1663286400')
eth_df = pd.DataFrame(eth_data['prices'], columns=['date', 'price']).set_index('date')
eth_df.index = pd.to_datetime(eth_df.index, unit='ms')

#Isolate most recent 14 day prices
eth_recent_df = eth_df.tail(14)

#Calculate pct_change, drop nan values and rename column to 24-hr change.
eth_recent_df = pd.DataFrame(eth_recent_df['price'].pct_change().dropna()).rename(columns={'price':'24_hr_change'})
eth_recent_df['24_hr_change'] = eth_recent_df['24_hr_change'] * 100

#XRP
#Pull data from coingecko and create DataFrame for historical data for simulation of app
xrp_data = cg.get_coin_market_chart_range_by_id(id='ripple',vs_currency='usd',from_timestamp='1654041600',to_timestamp='1663286400')
xrp_df = pd.DataFrame(xrp_data['prices'], columns=['date', 'price']).set_index('date')
xrp_df.index = pd.to_datetime(xrp_df.index, unit='ms')

#Isolate most recent 14 day prices
xrp_recent_df = xrp_df.tail(14)

#Calculate pct_change, drop nan values and rename column to 24-hr change.
xrp_recent_df = pd.DataFrame(xrp_recent_df['price'].pct_change().dropna()).rename(columns={'price':'24_hr_change'})
xrp_recent_df['24_hr_change'] = xrp_recent_df['24_hr_change'] * 100

#ADA
#Pull data from coingecko and create DataFrame for historical data for simulation of app
ada_data = cg.get_coin_market_chart_range_by_id(id='cardano',vs_currency='usd',from_timestamp='1654041600',to_timestamp='1663286400')
ada_df = pd.DataFrame(ada_data['prices'], columns=['date', 'price']).set_index('date')
ada_df.index = pd.to_datetime(ada_df.index, unit='ms')

#Isolate most recent 14 day prices
ada_recent_df = ada_df.tail(14)

#Calculate pct_change, drop nan values and rename column to 24-hr change. Multiply by 100 to mimic what the system returns from coingecko.
ada_recent_df = pd.DataFrame(ada_recent_df['price'].pct_change().dropna()).rename(columns={'price':'24_hr_change'})
ada_recent_df['24_hr_change'] = ada_recent_df['24_hr_change'] * 100

#SOL
#Pull data from coingecko and create DataFrame for historical data for simulation of app
sol_data = cg.get_coin_market_chart_range_by_id(id='solana',vs_currency='usd',from_timestamp='1654041600',to_timestamp='1663286400')
sol_df = pd.DataFrame(sol_data['prices'], columns=['date', 'price']).set_index('date')
sol_df.index = pd.to_datetime(sol_df.index, unit='ms')

#Isolate most recent 14 day prices
sol_recent_df = sol_df.tail(14)

#Calculate pct_change, drop nan values and rename column to 24-hr change. Multiply by 100 to mimic what the system returns from coingecko.
sol_recent_df = pd.DataFrame(sol_recent_df['price'].pct_change().dropna()).rename(columns={'price':'24_hr_change'})
sol_recent_df['24_hr_change'] = sol_recent_df['24_hr_change'] * 100

simulation_dates = pd.concat([btc_recent_df, eth_recent_df, xrp_recent_df, ada_recent_df, sol_recent_df], axis=1, join='inner')
simulation_dates_cols = ['BTC 24-hr change', 'ETH 24-hr change', 'XRP 24-hr change', 'ADA 24-hr change', 'SOL 24-hr change']
simulation_dates.columns = simulation_dates_cols
