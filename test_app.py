# Testing Twilio Software

# Import required libraries and dependencies
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from dotenv import load_dotenv
import questionary


# Load environment variables (should have twilio information)
load_dotenv()

# Create twilio id and tolken for use in sdk
twilio_account_id = os.environ["TWILIO_ACCOUNT_ID"]
twilio_token = os.environ["TWILIO_AUTH_TOKEN"]

# Create twilio rest client 
client = Client(twilio_account_id, twilio_token)

# Define a function that asks user for phone number
def get_user_phone_number():
    looper = True
    choices = ['Yes', 'No']
    try:    
        while looper == True:
            user_phone_number = questionary.text("Please enter your 10 digit phone number: ").ask()
            if len(user_phone_number) == 10:
                print(f"You have entered: {user_phone_number}")
                confirmation = questionary.select("Is this the correct number?", choices=choices).ask()
                if confirmation == 'Yes':
                    break
                if confirmation == 'No':
                    pass
                    
            else:
                print("Please try and re-enter your 10 digit phone number")
                print() 
    except Exception as e:
        print(e)
    return user_phone_number

# Define twilio alert for user
def twilio_alert(phone_number, twilio_phone_number, information):
    try:
        message = client.messages.create(to=f"+1{phone_number}", from_=f"+1{twilio_phone_number}",
                                    body=information)
        print(information, "was sent to:", phone_number, message)
    except TwilioRestException as e:
    # Implement your fallback code
        print(e)

if __name__ == '__main__':
    # Define information to send
    information_from_user = questionary.text("What would you like to send?: ").ask()
    # Define twilio number
    twilio_number = os.environ["TWILIO_PHONE_NUMBER"]
    # Call user request for phone number
    user_phone_number = get_user_phone_number()
    # Call the function to send the message
    twilio_alert(user_phone_number, twilio_number, information_from_user)
    
