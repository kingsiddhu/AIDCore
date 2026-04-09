import os
import subprocess
import Agent.debug
from Agent.toolset.spotify import play_playlist_by_name, play_song, get_playlists, spotify_pause, spotify_resume, next_track, previous_track

def list_files(dir_path="./"):
    dirs=os.listdir(dir_path)
    Agent.debug.logger(dirs)

    return dirs


def read_file(file_path="hello.txt", open_mode = "r"):
    if not os.path.abspath(os.curdir) in os.path.abspath(file_path):
        raise EOFError
    if not os.path.exists(file_path):
        raise EOFError
    elif not os.path.isfile(file_path):
        raise EOFError
    else:
        with open(file_path, open_mode) as f:
            return f.read()


def write_file(content: str = "",file_path="hello.txt", open_mode = "r"):
    if not os.path.abspath(os.curdir) in os.path.abspath(file_path):
        raise EOFError
    elif not os.path.isfile(file_path):
        raise EOFError
    else:
        with open(file_path, open_mode) as f:
            return f.write(content)

def open_photo(image_path:str=""):
    # Simple execution
    subprocess.run(["eog", image_path])
    return f"{image_path} image opened successfully. You are sucessfull in doing so."


def get_funcs():
    import inspect
    global funcs, loc
    funs_in_tools = []
    print(funcs)
    for i in funcs:
        sig = inspect.signature(loc[i])
        all_params = dict(sig.parameters)
        fun = {
            "tool_call_id" : i,
            "kwargs" : {}
        }
        for i in all_params:
            fun["kwargs"][str(i)] = all_params[i].default
        funs_in_tools.append(fun)
    funs_in_tools.append({"tool_call_id": "final", "kwargs": {}})
    return funs_in_tools

funcs = list(locals().keys())

funcs.remove("__name__")
funcs.remove("__doc__")
funcs.remove("__package__")
funcs.remove("__loader__")
funcs.remove("__spec__")
try:
    funcs.remove("__builtins__")
except:
    pass
try:
    funcs.remove("builtin")
except:
    pass
funcs.remove("__file__")
funcs.remove("__cached__")
if "sys" in funcs:
    funcs.remove("sys")
funcs.remove("os")
funcs.remove("subprocess")
try:
    funcs.remove("debug")
except:
    pass
try:
    funcs.remove("Agent.debug")
except:
    pass
try:
    funcs.remove("Agent")
except:
    pass
loc = locals()
if __name__ == "__main__":
    import json
    print(funcs)
    Agent.debug.logger(json.dumps(get_funcs(), indent=2))
    
