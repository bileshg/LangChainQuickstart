from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-4o-mini")

    response = model.invoke(
        [
            HumanMessage(content="Hi! I'm Bob"),
            AIMessage(content="Hello Bob! How can I assist you today?"),
            HumanMessage(content="What's my name?"),
        ]
    )

    print(response.content)
