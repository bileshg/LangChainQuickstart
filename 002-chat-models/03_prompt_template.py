from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-4o-mini")

    system_template = "Translate the following from English into {language}"

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{text}")]
    )

    prompt = prompt_template.invoke({"language": "Italian", "text": "hi!"})
    print(prompt)
    for message in prompt.to_messages():
        print(message)

    response = model.invoke(prompt)
    print(response.content)
