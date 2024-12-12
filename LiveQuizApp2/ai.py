import openai

API_KEY = open("key.txt", "r").read().strip()
openai.api_key = API_KEY

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, world!"}]
    )
    print(response)
except openai.error.OpenAIError as e:
    print(f"Error: {e}")
