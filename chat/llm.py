# import openai
# import os

# def get_ai_response(user_message):
#     api_key = os.getenv("OPENAI_API_KEY")
#     if not api_key:
#         return "Error: OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
    
#     try:
#         openai.api_key = api_key
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful AI assistant"},
#                 {"role": "user", "content": user_message},
#             ],
#             temperature=0.7,
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"Error communicating with OpenAI: {str(e)}"


from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or gpt-3.5-turbo if you want
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant"},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error communicating with OpenAI: {str(e)}"
