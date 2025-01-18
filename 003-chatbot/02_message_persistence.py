from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

load_dotenv()

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
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
    print(f"Starting conversation with thread_id: {config['configurable']['thread_id']}")

    query = "Hi! I'm Bob."

    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()  # output contains all messages in state

    query = "What's my name?"

    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()

    # Change the thread_id to simulate a new conversation
    config2 = {"configurable": {"thread_id": "abc234"}}
    print(f"Starting conversation with thread_id: {config2['configurable']['thread_id']}")

    # The model should not remember the previous conversation
    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config2)
    output["messages"][-1].pretty_print()

    print(f"Starting conversation with thread_id: {config['configurable']['thread_id']}")
    # The model should remember the previous conversation because the thread_id is the same
    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()
