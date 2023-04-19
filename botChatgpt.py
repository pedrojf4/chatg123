import requests
import json
import os
import openai
from dotenv import load_dotenv
load_dotenv()


        # set the URL and HEADERS constants
URL = f'https://graph.facebook.com/{os.getenv("API_VERSION")}/{os.getenv("FROM_PHONE_NUMBER_ID")}/messages'
HEADERS = {'Content-Type': 'application/json', 'Authorization': f'Bearer {os.getenv("ACCESS_TOKEN")}'}

openai.api_key = os.getenv("OPENAI_KEY")


def send_message_text(sender_phone,message):
    data = {
        "messaging_product": "whatsapp",
        "to": sender_phone,
        "type": "text",
        "text":{
            "body": message
        }
        }
    data = json.dumps(data)
    response = requests.post(url=URL,headers=HEADERS, data=data)
    # here you can send the content of response.text to your API and track logs
    #print('####THE RESPONSE####',response.text)


def send_chat_gpt(msg):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                
                {"role": "user", "content": f"{msg}"}
            ]
    )

    return response.choices[0].message.content

