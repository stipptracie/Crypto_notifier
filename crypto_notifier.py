# A Crypto Notifier Application

# Import modules

import pandas as pd
import os
import numpy as np
from pycoingecko import CoinGeckoAPI
import questionary
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()

# Set Variable for coingecko API
cg = CoinGeckoAPI()

#Dataframe for swing thresholds
crypto_swing_thresholds = {'Coin':['bitcoin','ethereum','ripple','cardano','solana'],'pct_change_Threshold':[0.029452,0.038992,0.044968,0.045519,0.057073]}

swing_thresholds_df = pd.DataFrame(crypto_swing_thresholds).set_index('Coin')

# what is ave % increase threshold by comparing x time in the past generate average daily return swing
# put user two weeks back and compare each day 
# if day has a big swing send message 
# if after two weeks send message no big swings
#
def get_tickers():
    tickers = []
    tickers = questionary.checkbox(
        "Select CryptoCurrencies",
        choices=["bitcoin","ethereum","ripple","cardano", "solana"]
    ).ask()
    return tickers


def get_user_number():
    phone_number = []
    phone_number = questionary.text("What is your 10 digit phone number?:").ask()
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
        client.messages.create(to=f"+1{phone_number}", from_=f"+1{twilio_phone_number}",
                                    body=information)
    # Implement your fallback code
    except TwilioRestException as e:
        print(e)


if __name__ == "__main__":
    # User input phone number to variable
    user_phone_number = get_user_number()
    
    # User input tickers to variable
    user_tickers = get_tickers()

    # Create conditional to pass information into message
    # Create empty message list to house information
    message_list = []
    
    for ticker in user_tickers:   
        daily_pct = cg.get_price(ids=f'{ticker}', vs_currencies='usd',include_24hr_change='true')
        daily_pct_df = pd.DataFrame(daily_pct)
        daily_pct_df = daily_pct_df.T
        compare_value = np.absolute(daily_pct_df.loc[:, 'usd_24h_change'])
        if compare_value[0] >= float((swing_thresholds_df.loc[ticker][0]))*100:
            information_to_send = f"There was a big price swing for {ticker} today compared to the last three years worth of daily changes \n"
            message_list.append(information_to_send)
        else:
            no_big_swing = f'There was no significant price swing for {ticker} from yesterday compared to the last three years worth of daily changes'
            message_list.append(no_big_swing)
            
    generate_twilio_message(user_phone_number, twilio_phone_number, message_list)
    
    print(f"A message has been sent to your phone {user_phone_number} with a two week summary report for {user_tickers}")
    

    









