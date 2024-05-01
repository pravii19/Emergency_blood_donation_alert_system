import random
import json
import torch
import mysql.connector
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from twilio.rest import Client 

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents from JSON file
with open('E:/blood/project/intents.json', 'r') as json_data:
    intents = json.load(json_data)

# Load model data
FILE = "E:/blood/project/data.pth"
data = torch.load(FILE)

# Initialize model parameters
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Load and initialize the model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# Global variable to store blood group information
blood_group_info = None

# Database connection for blood donation
conn_blood_donation = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="blood_donation"
)

def get_blood_group(blood_group):
    # Connect to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="blood_donation"
    )

    # Create a cursor object to execute queries
    cursor = conn.cursor(dictionary=True)

    # Query the database for the specified blood group
    query = "SELECT name, location, phone_no FROM registration WHERE blood_group = %s"
    cursor.execute(query, (blood_group,))
    result = cursor.fetchall()

    # Close cursor and database connection
    cursor.close()
    conn.close()

    # Check if there are any results
    if result:
        # If there are results, return them
        return result
    else:
        # If no results found, return None
        return None

def get_response(msg):
    global blood_group_info  # Access the global variable

    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if tag == "blood_group":
                    # Extract the blood group from the message
                    blood_group = msg.strip().capitalize()
                    # Call the function to retrieve blood group from the database
                    blood_group_info = get_blood_group(blood_group)
                    if blood_group_info:
                        # Format the response with donor information
                        response = f"Donors with blood group {blood_group}:\n"
                        for donor in blood_group_info:
                            response += f"Name: {donor['name']}, Location: {donor['location']}, Phone: {donor['phone_no']}\n"
                        return response
                    else:
                        return "No donors found with the specified blood group."
                elif "send" in intent["patterns"]:
                    if blood_group_info:  # Check if blood_group_info is not None
                        # Send SMS to the donor phone numbers
                        for donor in blood_group_info:
                            send_sms(donor['phone_no'])
                        return random.choice(intent['responses'])  # Return a random response for "send" intent
                    else:
                        return "Cannot send SMS as donor information is not available."
                else:
                    return random.choice(intent['responses'])
                
    return "I do not understand..."

def send_sms(phone_number):
    account_sid = ''
    auth_token = ''

    # Initialize Twilio Client
    client = Client(account_sid, auth_token)

    from_phone_number = ''  # Example: Replace with your Twilio phone number

    message_body = 'Emergency !!Blood group needed AB+ || location:Madurai || Hospital Name: Meenakshi Mission'

    try:
        # Send SMS message
        message = client.messages.create(
            body=message_body,
            from_=from_phone_number,
            to=phone_number
        )
        print("Message sent successfully!")  
        print("Message SID:", message.sid)
    except Exception as e:
        print("Failed to send message:", str(e))
    
if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
