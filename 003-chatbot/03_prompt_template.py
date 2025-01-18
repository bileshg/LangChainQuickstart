from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You talk like a pirate. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    prompt = prompt_template.invoke(state)
    response = model.invoke(prompt)
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-4o-mini")

    config = {"configurable": {"thread_id": "abc123"}}

    query = "Hi! I'm Jim."

    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()  # output contains all messages in state

    query = "What's my name?"

    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()
