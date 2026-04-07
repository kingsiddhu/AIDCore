from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from typing import TypedDict
import Agent
import asyncio


# Define state
class AgentState(TypedDict):
    input: str
    valid : bool
    error : bool
    action: dict
    messages : list  #memory
    result: str
    role : str

mainLLM = OllamaLLM(model="llama3.1:8b")
#mainLLM = OllamaLLM(model="qwen3.5:9b")
#mainLLM = OllamaLLM(model="mikestaub/apriel-1.5:15b-thinker-q4_k_m")

#Streaming text thingy
async def getResp(data, model):
    result = ""
    async for chunk in model.astream(data):
        print(chunk, end="", flush=True)
        result += chunk
    print()
    return result

#getResp(Agent.INIT_PROMPT, mainLLM)

# Nodes
async def valid(state):
    prompt = Agent.VALID_PROMPT

async def init(state):
    starting_mem = [{"role": "system", "content": Agent.INIT_PROMPT}]
    return {
        "valid": False,
        "error": "",
        "messages" : starting_mem
    }


async def display(state):
    prompt = f"{state['input']}"

    state["messages"].append({"role": "system", "content": Agent.DISPLAY_PROMPT})
    state["messages"].append({"role": state["role"], "content": prompt})
    res = await getResp(state["messages"], mainLLM)

    state["messages"].append({"role": "assistant", "content": res})

    #Agent.debug.logger(res)
    return {"result": res, "messages": state["messages"], "error": False}

async def toolsToUse(state):
    prompt = state["input"]
    state["messages"].append({"role": "system", "content": Agent.TOOLS_TO_USE})
    state["messages"].append({"role": "user", "content": prompt})
    res = await getResp(state["messages"], mainLLM)

    state["messages"].append({"role": "system", "content": res})
    #Agent.debug.logger(res)
    return {
        #"result": res,
        "action": Agent.parsejson.parse_response(res), "messages": state["messages"]}


async def valid_tools(state):

    return {"valid": "hellyea"}

async def is_valid(state):
    if state["valid"]:
        return 'hellyea'
    return "no"


async def toolsRun(state):
    Agent.debug.logger(state)
    data = Agent.parsejson.parse_response(state["action"])
    func_name =  data["function_name"]

    content = getattr(Agent.tools,func_name)(**data["kwargs"])

    return {"input": str(content), "role" : "system"}

def should_continue(state):
    if state["result"].endswith("END"):
        return "end"
    AgentState.error = True
    return "continue"
# Graph

builder = StateGraph(AgentState)

builder.add_node("init", init)
builder.add_node("query", display)
builder.add_node("toolget", toolsToUse)
builder.add_node("valid", valid_tools)
builder.add_node("executioner", toolsRun)

builder.set_entry_point("init")
builder.add_edge("init","query")
builder.add_edge("query", "toolget")
builder.add_edge("toolget", "valid")
builder.add_conditional_edges(
    "valid",
    is_valid,{
        "hellyea" : "executioner",
        "no" : "query"
    }

)

#builder.add_edge("executioner", END)

builder.add_conditional_edges(
    "executioner",
    should_continue,
    {
        "continue": "query",
        "end": END
    }
)


graph = builder.compile()

# Run
output = asyncio.run(graph.ainvoke({"input": "tell me what files are there in the directory './'", "role": "user"}))
Agent.debug.print_dict(output)