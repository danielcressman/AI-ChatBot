import faqbot
import random

def chat():
    print("Start talking with the bot! (type quit to stop)")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        result = faqbot.predict(inp)
        if result is not None: 
            responses = result['responses']
            print(random.choice(responses))
        else:
            print("I didnt get that. Can you explain or try again.")


chat()
