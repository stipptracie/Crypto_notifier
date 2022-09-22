# A Crypto Notifier Application

# Import modules


import pandas as pd
import os
import numpy as np
from pycoingecko import CoinGeckoAPI
import questionary
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import numpy as np
from pathlib import Path
from dotenv import load_dotenv


load_dotenv


# Set Variable for coingecko API
cg = CoinGeckoAPI()

#Dataframe for swing thresholds
crypto_swing_thresholds = {'Coin':['bitcoin','ethereum','ripple','cardano','solana'],'pct_change_Threshold':[0.029452,0.038992,0.044968,0.045519,0.057073]}

swing_thresholds_df = pd.DataFrame(crypto_swing_thresholds).set_index('Coin')
# create two week dataframe
 # Create two week df from already made data
two_week_daily_pct_change_df = pd.read_csv(Path('./Resources/simdata.csv'))
print(two_week_daily_pct_change_df)

# generate a dictionary as well for use when pulling dates
dictionary = two_week_daily_pct_change_df.to_dict()


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

# define dictionary get keys from values funciton
def get_keys_from_value(dictionary_data, value_data):
    # returns a list value
    return [k for k, v in dictionary_data.items() if v == value_data]


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
        client.messages.create(to=f"+1{phone_number}", from_=f"+1{twilio_phone_number}",
                                    body=information)
    # Implement your fallback code
    except TwilioRestException as e:
        print(e)
    

if __name__ == "__main__":
    # User input phone number to variable
    user_phone_number = get_user_number()
    
    # User input symbols to variable
    user_symbols = get_symbols()
    
    message_list = []
    
    for symbol in user_symbols:
            for value in two_week_daily_pct_change_df[symbol]:
                print(value)
                if np.absolute(float(value)) >= float(swing_thresholds_df.loc[symbol]):
                    # change df to dictionary and call the date
                    indexer = get_keys_from_value(dictionary[symbol], value)
                    print(indexer)
                    s = [str(i) for i in indexer]
                    # Join list items using join()
                    res = int("".join(s))
                    
                    # pull date from dictionary key value for date 
                    date = dictionary['date'][res]
                    print(dictionary['date'][res])
                               
                    information_to_send = f"BIG SWING {symbol} on {date}\n"
                    print(information_to_send)
                    message_list.append(information_to_send)
                    
                else: 
                    # change df to dictionary and call the date
                    indexer = get_keys_from_value(dictionary[symbol], value)
                    print(indexer)
                    s = [str(i) for i in indexer]
                    # Join list items using join()
                    res = int("".join(s))
                    
                    # pull date from dictionary key value for date 
                    date = dictionary['date'][res]
                    print(dictionary['date'][res])
                               
                    no_swing = f"no swing {symbol} on {date}"
                    message_list.append(no_swing)        
    
    # Generate message with list of strings
    message_list = '. '.join(message_list)
    print(message_list)
    generate_twilio_message(user_phone_number, twilio_phone_number, message_list)
    
    print(f"A message has been sent to {user_phone_number} with a two week summary report for {user_symbols}")
    