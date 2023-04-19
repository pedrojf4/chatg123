from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from botChatgpt import send_message_text, send_chat_gpt
from waitress import serve
load_dotenv()


app = Flask(__name__)

#* THIS IS THE WEBHOOK

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        hmode = request.args.get('hub.mode')
        htoken = request.args.get('hub.verify_token')
        hchallenge = request.args.get('hub.challenge')
        if (hmode == 'subscribe') and (htoken == os.getenv('BUSINESS_TOKEN')):
            return hchallenge
        else:
            return 'Error', 400
    if request.method == 'POST':
        # serialize the request data into a object to access the data easily
        request_data = (request.get_json())
        changes = request_data['entry'][0]['changes'][0]
        if (request_data['object'] == 'whatsapp_business_account') and (changes['field'] == 'messages'):
            if not 'statuses' in changes['value']:
                
                sender_phone = changes['value']['contacts'][0]['wa_id']
                profile_name = changes['value']['contacts'][0]['profile']['name']
                message_text = changes['value']['messages'][0]['text']['body']

                print(sender_phone,profile_name,message_text)

                if changes['value']['messages'][0]['type'] == 'text':
                    # Get the message
                    message = changes['value']['messages'][0]['text']['body']
                    additional_data = changes['value']
                    # Send the message to the chatbot
                    ###chatbot.proccess_message(sender_phone,message,additional_data)
                    responseGPT = send_chat_gpt(message)
                    send_message_text(sender_phone,responseGPT)
                # return jsonify(request_data),200
            return 'OK', 200
        else:
            return 'Error', 400

if __name__ == "__main__":
    app.run(debug=False, port=5000)
    
     
     
 
