from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-4o-mini")

    try:
        messages = [
            SystemMessage("Translate the following from English into Italian"),
            HumanMessage("hi!"),
        ]
        for token in model.stream(messages):
            print(token.content, end=" | ")
    except Exception as e:
        print(f"Error: {e}")
