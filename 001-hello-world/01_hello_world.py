from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-4o-mini")

    try:
        response = model.invoke("Hello, world!")
        print(response.content)
    except Exception as e:
        print(f"Error: {e}")
