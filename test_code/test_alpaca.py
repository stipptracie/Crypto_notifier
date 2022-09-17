conda

load_dotenv()

# Set Alpaca API key and secret by calling the os.getenv function and referencing the environment variable names
# Set each environment variable to a notebook variable of the same name
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

# Define Start date and end date
start_date = pd.Timestamp("2019-05-01", tz="America/New_York").isoformat()
end_date = pd.Timestamp("2020-05-01", tz="America/New_York").isoformat()

# Set timeframe to one day (1Day)
timeframe = "1Day"

def get_tickers():
    tickers_list = []
    choices = ['AAPL', 'SBUX', 'MSFT']
    items = questionary.checkbox(choices=choices).ask()
    tickers_list.append(items)
    
    return tickers_list

# Create alpaca rest API
alpaca = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    api_version="v2")

if __name__ == '__main__':
    # Get tickers
    tickers = get_tickers()
    
    # Create Data frame
    prices_df = alpaca.get_bars(
        tickers,
        timeframe,
        start=start_date,
        end=end_date
        ).df

    for ticker in tickers:
        ticker = prices_df[prices_df['symbol']==ticker]

    
    