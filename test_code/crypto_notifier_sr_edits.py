# A Crypto Notifier Application

# Import modules
import pandas as pd
import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
import questionary
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Load .env file
load_dotenv()


# Define code for ticker
def get_tickers():
    tickers = []
    return tickers

# Define code for alpaca to get what a big swing is
# create rest api
# what is ave % increase threshold by comparing x time in the past generate average daily return swing
# put user two weeks back and compare each day 
# if day has a big swing send message 
# if after two weeks send message no big swings
#

def get_user_number():
    return phone_number





# Define code for Twilio message
# Set up twilio client
# Create twilio id and tolken for use in sdk
twilio_account_id = os.environ["TWILIO_ACCOUNT_ID"]
twilio_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_phone_number = os.environ["TWILIO_PHONE_NUMBER"]

# Create twilio rest client 
client = Client(twilio_account_id, twilio_token)

# Define generate twilio message
def generate_twilio_message(phone_number, twilio_phone_number, information):
    try:
        message = client.messages.create(to=f"+1{phone_number}", from_=f"+1{twilio_phone_number}",
                                    body=information)
    # Implement your fallback code
    except TwilioRestException as e:
        print(e)
    return message

if __name__ == "__main__":    
    # User input phone number to variable
    user_phone_number = get_user_number()
    
    # User input tickers to variable
    user_tickers = get_tickers()
    
    # Generate threshold df
    for ticker in user_tickers:
        # run through coingecko to generate concatenated df of threshold values
        swing_thresholds_df = # @TODO #
    
    # Generate df for each ticker for the last two weeks
    for ticker in user_tickers:
        two_week_daily_pct_change_df = # @TODO #
        
    
    
    # Create conditional to pass information into message
    # Will need two dataframes, one with last two weeks of daily percent changes
    # Dataframe for comparing 
    # create empty list of strings to house text message
    # could create a dictionary for each day in the last two weeks day: ticker, true/false and use 
    # if dictionary[1] == True:
    #   message_list.append(day, ticker)
    message_list = []
    
    for row in two_week_daily_pct_change_df:
            for symbol in user_tickers:
                if float(row[symbol]) >= float(swing_thresholds_df[symbol]):
                    information_to_send = f"There was a big price swing on {row.index} for {symbol} \n"
                    message_list.append(information_to_send)
                else: 
                    no_swing = f"There was no big price changes for {symbol} in the last two weeks"
                    message_list.append(no_swing)        
    
    # Generate message with list of strings
    generate_twilio_message(phone_number, twilio_phone_number, message_list)
    
    print(f"A message has been sent to you phone with a two week summary report for {user_tickers}")
    

















# CODE FROM PREVIOUS WORK FOR REFERENCE

# Create a function called `sector_report` that will be the application report.
# This function will be called from the __main__ loop.
def sector_report(sectors, engine):

    # Print a welcome message for the application
    print("\n......Welcome to the Sector Analyzer Report.....\n")
    print("This report will calculate the yearly return of a financial sector based on the top five\n")
    print("companies in that sector based on market cap.\n")

    # Using questionary, give the user a list of sectors to run the report on.
    sector = questionary.select("Which sector do you wish to report on?", choices=sectors).ask()

    print("Running report ...")

    # Write a sql statement that selects all stocks from that sector.
    # Return the values in descending order by MarketCap.
    sql_sector = f"""
        SELECT * FROM NYSE
        WHERE Sector = '{sector}'
        ORDER BY MarketCap DESC
    """

    # Query the database using the sql statement written above.
    # Save the returned values in a DataFrame called `sector_df`
    sector_df = pd.read_sql_query(sql_sector, engine)

    # Create a list called `symbols`
    # to hold the "Symbol" of the top 5 stocks from the `sector_df` DataFrame
    symbols = sector_df["Symbol"][0:5]

    # The Alpaca Parameters for timeframe and daterange
    # `today` is a timestamp using Pandas Timestamp
    # `a_year_ago` is calculated using Pandas Timestamp and Timedelta
    timeframe = '1Day'
    today = pd.Timestamp.now(tz="America/New_York")
    a_year_ago = pd.Timestamp(today - pd.Timedelta(days=365)).isoformat()
    end_date = pd.Timestamp(today - pd.Timedelta(days=1)).isoformat()

    # The Alpaca tradeapi.REST object
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version="v2")

    # Use the Alpaca get_bars function to get the closing prices for the stocks.
    sector_prices_df = alpaca.get_bars(
        symbols,
        timeframe,
        start=a_year_ago,
        end=end_date
    ).df

    # Reorganize the DataFrame to have a MultiIndex.
    dfs = [
        sector_prices_df[sector_prices_df['symbol']==symbol].drop('symbol', axis=1)
        for symbol in symbols
    ]
    sector_prices_df = pd.concat(dfs, axis=1, keys=symbols)

    # An empty dictionary that will hold the daily pct change for each stock from the sector.
    symbol_pct_changes = {}

    # Calculate the daily percent change for each symbol in the sector.
    # Create a loop that selects each symbol in the symbols list.
    # Using the `sector_prices_df` DataFrame returned from the Alpaca API call,
    # call the `pct_change` function on the DataFrame's "close" column.
    for symbol in symbols:
        symbol_pct_changes[symbol] = sector_prices_df[symbol]['close'].pct_change()

    # Create a dataframe from the dictionary of daily pct changes.
    sector_pct_changes = pd.DataFrame.from_dict(symbol_pct_changes)

    # Calculate the average daily pct change for each day of the five stocks.
    sector_pct_changes['sector_pct_change'] = sector_pct_changes.mean(axis=1)

    # Sum the daily percent changes for the sector over the past year to find the sector yearly return.
    cumulative_returns = (1 + sector_pct_changes['sector_pct_change']).cumprod() - 1
    sector_yearly_rtn = cumulative_returns[-1]

    # Create a statement that displays the `results` of your `sector_yearly_return` calculation.
    # On a separate line (\n) ask the use if they would like to continue running the report.
    results = f"The cumulative return for the {sector} sector for the past year is {sector_yearly_rtn * 100}%.\nWould you like to run another report?"

    # Using the `results` statement created above,
    # prompt the user to run the report again (`y`) or exit the program (`n`).
    continue_running = questionary.select(results, choices=["y", "n"]).ask()

    # Return the `continue_running` variable from the `sector_report` function
    return continue_running


# The __main__ loop of the application.
# It is the entry point for the program.
if __name__ == "__main__":

    # # Database connection string to the clean NYSE database
    database_connection_string = 'sqlite:///../Resources/nyse.db'

    # Create an engine to interact with the database
    engine = sql.create_engine(database_connection_string)

    # Read the NYSE table into a dataframe called `nyse_df`
    nyse_df = pd.read_sql_table('NYSE', engine)

    # Get a list of the sector names from the `nyse_df` DataFrame
    # Be sure to drop n/a values and capture only unique values.
    # You will use this list of sector names for the user options in the report.
    sectors = nyse_df["Sector"]
    sectors = sectors.dropna()
    sectors = sectors.unique()

    # Create a variable named running and set it to True
    running = True

    # While running is `True` call the `sector_report` function.
    # Pass the `sectors` and the database `engine` as parameters.
    while running:
        continue_running = sector_report(sectors, engine)
        if continue_running == 'y':
            running = True
        else:
            running = False
