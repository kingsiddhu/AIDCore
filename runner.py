from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from typing import TypedDict
import Agent
import asyncio
import json


# Define state
class AgentState(TypedDict):
    input: str
    valid : bool
    error : bool
    action: dict
    messages : list  #memory
    checkpoint: list
    result: str
    role : str

#mainLLM = OllamaLLM(model="llama3.1:8b")
#mainLLM = OllamaLLM(model="qwen3.5:9b")
#mainLLM = OllamaLLM(model="mikestaub/apriel-1.5:15b-thinker-q4_k_m")

MODEL_MAP = {
    "music": OllamaLLM(model="phi3:mini"),
    "coding": OllamaLLM(model="deepseek-coder:6.7b"),
    #"general": OllamaLLM(model="qwen3.5:9b"),
    "general": OllamaLLM(model="llama3.1:8b"),
    "system_tool": OllamaLLM(model="phi3:mini"),
    "complex_reasoning": OllamaLLM(model="deepseek-r1:14b")
}
Agent.debug.checkpoint("MODELS_MAPPED")
#Streaming text thingy

async def getResp(data, model, debug):
    result = ""
    Agent.debug.checkpoint("GETRESp"+ str(model.get_name))
    Agent.debug.logger(data)
    async for chunk in model.astream(data):
        if debug:
            print(chunk, end="", flush=True)
        result += chunk
    print()
    return result

def clear_system_prompts(data:list):
    n = []
    for i in data:
        if i["role"] == "system":
            if i["content"].startswith(Agent.INIT_PROMPT[:20]) or i["content"].startswith("TOOL RESULT"):
                n.append(i)
        else:
            n.append(i)
    return n


#getResp(Agent.INIT_PROMPT, mainLLM)

# Nodes
async def init(state):

    starting_mem = [{"role": "system", "content": Agent.INIT_PROMPT}]
    Agent.debug.checkpoint("INITED")
    return {
        "valid": False,
        "error": False,
        "messages" : starting_mem
    }

async def assistant(state):
    prompt = f"{state['input']}"

    state["messages"] = clear_system_prompts(state["messages"])

    state["messages"].append({
        "role": "system",
        "content": "You are currently in the CHAT MODE."
        })
    
    state["messages"].append({"role": "user", "content": prompt})

    
    res = await getResp(state["messages"], MODEL_MAP["general"], True)

    state["messages"].append({"role": "assistant", "content": res})

    Agent.debug.checkpoint("ASSISNTANT")
    #Agent.debug.logger(res)

    Agent.debug.dumplog(state)

    return {"result": res, "messages": state["messages"], "error": False}


async def toolsToUse(state):
    #checkpoint = state["messages"].copy()
    
    state["messages"] = clear_system_prompts(state["messages"])
    state["messages"].append({
        "role": "system",
        "content": "You are currently in the TOOL_SELECTION phase. here are the available tools: "+ json.dumps(Agent.tools.get_funcs(), indent=2)
        })
    res = await getResp(state["messages"], MODEL_MAP["general"], Agent.debug.DebugMode)

    res = Agent.parsejson.extract_json(res)
    #state["messages"].append({"role": "system", "content": str(res)})


    Agent.debug.dumplog(state)


    #Agent.debug.logger(res)
    return {
        #"result": res,
        "action": res,
        #"checkpoint": checkpoint,
        "messages": state["messages"]
        }

async def toolsRun(state):
    Agent.debug.logger(state)
    data = Agent.parsejson.parse_response(state["action"])
    print(data, type(data))
    func_name =  data["tool_call_id"]

    if func_name == "final":
        return {"result":"   END"}

    if func_name in Agent.tools.funcs:
        #kwargs = {Agent.tools}
        content = str(getattr(Agent.tools,func_name)(**data["kwargs"]))
    else:
        content = "ILLEGAL METHOD USED"
    

    state["messages"].append({"role": "system", "content": f"TOOL RESULT:\n{content}", "tool_call_id": func_name})



    Agent.debug.dumplog(state)

    return {"messages": state["messages"]}

def should_continue(state):
    
    Agent.debug.dumplog(state)
    
    if state["result"].endswith("END"):
        return "end"
    
    if len(state["messages"]) > 10:
        return "end"

    builder.state_schema.error = True
    return "continue"
# Graph

builder = StateGraph(AgentState)

builder.add_node("init", init) #starting prompts and shi
builder.add_node("assistant", assistant) #LLM for front end convo
builder.add_node("toolget", toolsToUse) #LLM to find what tools to run
#builder.add_node("valid", valid_tools)  #another LLM to validate it.
builder.add_node("executioner", toolsRun) #Running the tool

builder.set_entry_point("init")
builder.add_edge("init","assistant")
builder.add_conditional_edges(
    "assistant",
    should_continue, {
        "continue": "toolget",
        "end": END
    }
)

builder.add_edge("toolget", "executioner")

builder.add_conditional_edges(
    "executioner",
    should_continue,
    {
        "continue": "assistant",
        "end": END
    }
)


graph = builder.compile()
Agent.debug.checkpoint("COMPILED")

# Run
output = asyncio.run(graph.ainvoke(
    {
        #"input": "tell me what files are there in the directory './'", 
        "input": "play the playlist Siddharth's Favs", 
        #"input": "list the files and then open one image you find.", 
        "role": "user"
        }
    )
)

Agent.debug.print_dict(output)