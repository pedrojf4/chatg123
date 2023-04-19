import openai
openai.api_key = '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'


def send_chat_gpt(msg):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                
                {"role": "user", "content": f"{msg}"}
            ]
    )
    
    return response.choices[0].message.content