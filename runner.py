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
    content : str
    result: str

mainLLM = OllamaLLM(model="llama3.1:8b")

#Streaming text thingy
async def getResp(text, model):
    result = ""
    async for chunk in model.astream(text):
        print(chunk, end="", flush=True)
        result += chunk
    return result

getResp(Agent.INIT_PROMPT, mainLLM)

# Nodes
async def valid(state):
    prompt = Agent.VALID_PROMPT

async def init(state):
    prompt = Agent.INIT_PROMPT
    res = await getResp(prompt, mainLLM)
    return {
        "valid": False,
        "error": ""
    }


async def display(state):
    AgentState.error = False
    prompt = Agent.SYSTEM_PROMPTS.DISPLAY_PROMPT+f"{state['input']}"
    res = await getResp(prompt, mainLLM)
    #Agent.debug.logger(res)
    return {"result": res}

async def toolsToUse(state):
    prompt = Agent.TOOLS_TO_USE + state["input"]
    res = await getResp(prompt, mainLLM)

    #Agent.debug.logger(res)
    return {"action": Agent.parsejson.parse_response(res)}

async def valid_tools(state):

    return {"valid": "hellyea"}

async def is_valid(state):
    if state["valid"]:
        return 'hellyea'
    return "no"
async def toolsRun(state):
    Agent.debug.logger(state)
    data = Agent.parsejson.parse_response(state["action"])
    getattr(Agent.tools, data["function_name"])(**data["kwargs"])
    return {"input": str(data)}

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
builder.add_node("executor", toolsRun)

builder.set_entry_point("init")
builder.add_edge("init","query")
builder.add_edge("query", "toolget")
builder.add_edge("toolget", "valid")
builder.add_conditional_edges(
    "valid",
    is_valid,{
        "hellyea" : "executor",
        "no" : "query"
    }

)

#builder.add_edge("executor", END)

builder.add_conditional_edges(
    "executor",
    should_continue,
    {
        "continue": "query",
        "end": END
    }
)


graph = builder.compile()

# Run
output = asyncio.run(graph.ainvoke({"input": "tell me what files are there in the directory './'"}))
Agent.debug.print_dict(output)