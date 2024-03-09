import openai
import gradio
import re
import os
from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv('openai_api_key')
openai.api_key = api_key


messages = [{"role": "system", "content": "Welcome! I'm a medical expert specializing in patient diagnosis and treatment. Please feel free to ask me any medical-related questions."}]

def is_medical_query(user_input):
    medical_keywords = ['medical', 'doctor', 'patient', 'diagnosis', 'treatment', 'symptom', 'prescription', 'hospital', 'clinic','medicine']
    for keyword in medical_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', user_input.lower()):
            return True
    return False

def CustomChatGPT(user_input):
    global messages
    messages.append({"role": "user", "content": user_input})
    
    # Check if the user input is medical-related
    if not is_medical_query(user_input):
        return "Please ask a medical-related question."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

demo = gradio.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="Medical Assistant")
demo.launch(share=True)

