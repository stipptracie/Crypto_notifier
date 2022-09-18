# A Crypto Notifier Application

# Import modules

import pandas as pd
import os
import json
import requests
import numpy as np
from pycoingecko import CoinGeckoAPI
import questionary
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Set Variable for coingecko API
cg = CoinGeckoAPI()

#Dataframe for swing thresholds
crypto_swing_thresholds = {'Coin':['BTC','ETH','XRP','ADA','SOL'],'pct_change_Threshold':[0.029452,0.038992,0.044968,0.045519,0.057073]}

swing_thresholds_df = pd.DataFrame(crypto_swing_thresholds).set_index('Coin')

#two_week_daily_pct_change_df = # @TODO #

# what is ave % increase threshold by comparing x time in the past generate average daily return swing
# put user two weeks back and compare each day 
# if day has a big swing send message 
# if after two weeks send message no big swings
#
def get_tickers():
    tickers = []
    tickers = questionary.checkbox(
        "Select CryptoCurrencies",
        choices=["BTC","ETH","XRP","ADA", "SOL"]
    ).ask()
return tickers

def get_user_number():
    phone_number = []
    phone_number = questionary.text("What is your phone number?:").ask()
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


    # Create conditional to pass information into message
    # Will need two dataframes, one with last two weeks of daily percent changes
    # Dataframe for comparing 
    # create empty list of strings to house text message
    # could create a dictionary for each day in the last two weeks day: ticker, true/false and use 
    # if dictionary[1] == True:
    #   message_list.append(day, ticker)
    """message_list = []"""
    """for row in daily_pct_change_df:
            for symbol in ticker_list:
                if float(daily_percent_change_df[symbol]) >= threshold_value:
                    information_to_send = f"There was a big price swing on {daily_pct_change.index} for {symbol} \n"
                    message_list.append(information)
                else: 
                    pass        
    """
    # Generate message with list of strings
    """generate_twilio_message(phone_number, twilio_phone_number, message_list)"""
    














