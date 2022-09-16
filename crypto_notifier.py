# A Crypto Notifier Application

# Import modules
import pandas as pd
import sqlalchemy as sql
import os
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv
import questionary
import twilio



# Load .env file
load_dotenv()

# Set the variables for the Alpaca API and secret keys
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

# Define code for ticker
tickers = []
def get_tickers():

    tickers = questionary.checkbox(
        "Select CryptoCurrencies",
        choices=["bitcoin","ethereum","litecoin",
        ]).ask()
    print(tickers)
    return tickers

# Define code for alpaca to get what a big swing is
# create rest api
# what is ave % increase threshold by comparing x time in the past generate average daily return swing
# put user two weeks back and compare each day 
# if day has a big swing send message 
# if after two weeks send message no big swings
#
user_phone_number = []
def get_user_number():
  
    user_phone_number = questionary.text("What is your phone number?:").ask()
    print(user_phone_number)
    return user_phone_number


cg = CoinGeckoAPI()
data = cg.get_coin_history_by_id(id=["bitcoin"], date= "10-10-2020")




get_tickers()
get_user_number()
print(data)







# Define code for Twilio message
#def generate_twilio_message():
    # notify when big swing
    # two parts if big swing
    # if no big
    #return message

#if __name__ == "__main__":

















