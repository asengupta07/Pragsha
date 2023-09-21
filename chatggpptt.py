import openai

api_key = ''
openai.api_key = api_key

def chat_with_gpt3(prompt):
    try:

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n = 1,
            stop=None
        )


        reply = response.choices[0].text.strip()
        print("ChatGPT 3.5: " + reply)
    except Exception as e:
        print("An error occurred: " + str(e))

if __name__ == "__main__":
    user_input = input("You: ")
    prompt = f"You: {user_input}\nChatGPT 3.5:"
    chat_with_gpt3(prompt)
