# A Crypto Notifier Application

# Import modules

from email import message
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
crypto_swing_thresholds = {'Coin':['bitcoin','ethereum','ripple','cardano','solana'],'pct_change_Threshold':[0.029452,0.038992,0.044968,0.045519,0.057073]}

swing_thresholds_df = pd.DataFrame(crypto_swing_thresholds).set_index('Coin')
# create two week dataframe
 # Create two week df from already made data
two_week_daily_pct_change_df = pd.read_csv('./Resources/simdata.csv')
# if after two weeks send message no big swings
#
def get_symbols():
    symbols = []
    symbols = questionary.checkbox(
        "Select CryptoCurrencies",
        choices=["bitcoin", "ethereum", "cardano", "ripple", "solana"]
    ).ask()
    return symbols


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
    
    # User input symbols to variable
    user_symbols = ["bitcoin", "ethereum", "cardano", "ripple", "solana"]
    #get_symbols()
    
    message_list = []
    
    for symbol in user_symbols:
            for row in two_week_daily_pct_change_df.loc[:, symbol]:
                if float(row) >= float(swing_thresholds_df.loc[symbol]):
                    information_to_send = f"BIG SWING {symbol} \n"
                    message_list.append(information_to_send)
                    print(message_list)
                else: 
                    no_swing = f"no swing {symbol}"
                    message_list.append(no_swing)        
    
    # Generate message with list of strings
    message_list = '. '.join(message_list)
    print(message_list)
    #generate_twilio_message(user_phone_number, twilio_phone_number, message_list)
    
    print(f"A message has been sent to you phone with a two week summary report for {user_symbols}")
    









