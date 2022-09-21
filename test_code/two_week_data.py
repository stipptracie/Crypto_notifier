# Function to pull 2 weeks of data from symbols list

# Import required libraries and dependencies
from distutils.command.install_egg_info import to_filename
import pandas as pd
import datetime
from pycoingecko import CoinGeckoAPI

# Set up Coin Gecko Client
cg = CoinGeckoAPI()

# Get date two weeks from today
start_date_two_weeks_ago = (pd.Timestamp.now() - pd.Timedelta('14 days')).timestamp()

# Get date right now
end_date_today = (pd.Timestamp.now()).timestamp()

# Set symbols list
symbols = ['bitcoin', 'ethereum', 'ripple', 'cardano', 'solana']

# Create logic to loop through symbols and put into data frame
to_merge_dict = {}
for symbol in symbols:
    df = cg.get_coin_market_chart_range_by_id(id=f'{symbol}', vs_currency='usd', from_timestamp=start_date_two_weeks_ago, to_timestamp=end_date_today)
    df = df['prices']
    df_two_weeks = pd.DataFrame(df)
    to_merge_dict = {f'{symbol}': df_two_weeks}

