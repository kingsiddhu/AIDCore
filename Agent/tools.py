import os
import subprocess
import Agent.debug
import platform
from Agent.toolset.spotify import play_playlist, play_song, spotify_pause, spotify_resume, next_track, previous_track

if platform.system() == "Windows":
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

if platform.system() == "Linux":
    pass


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



def set_windows_volume(percent:float= 50):
    if platform.system() == "Windows":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Volume range is usually -65.25 to 0.0 (in decibels)
        # This helper sets it by scalar (0.0 to 1.0)
        volume.SetMasterVolumeLevelScalar(percent/100, None)
    else:
        # Ensure the input is within bounds
        percent = max(0, min(100, percent))
        
        # 'Master' is the standard control name
        os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {percent}%")
    print(f"{Agent.debug.COL_GRE}Linux: Adjusted volume by {percent}%{Agent.debug.RESET}")

def increase_volume(step_percent=5):
    system = platform.system()

    if system == "Windows":
        volume = get_volume_interface()
        # Get current volume scalar (0.0 to 1.0)
        current_vol = volume.GetMasterVolumeLevelScalar()
        # Convert step (e.g., 5) to scalar (0.05)
        new_vol = current_vol + (step_percent / 100.0)
        # Clamp between 0.0 and 1.0
        new_vol = max(0.0, min(1.0, new_vol))
        volume.SetMasterVolumeLevelScalar(new_vol, None)
        print(f"Windows: Volume set to {int(new_vol * 100)}%")

    elif system == "Linux":
        # Use +5% or -5% syntax for amixer
        sign = "+" if step_percent > 0 else "-"
        # amixer handles clamping automatically
        os.system(f"amixer -q sset Master {abs(step_percent)}%{sign}")
        print(f"{Agent.debug.COL_GRE}Linux: Adjusted volume by {step_percent}%{Agent.debug.RESET}")

    else:
        print("Unsupported Operating System")

def decrease_volume(step_percent=5):
    increase_volume(-step_percent)


########################
###  ADD TOOLS HERE  ###
########################









#/--------------------/#

def get_funcs():
    import inspect
    global funcs, loc
    funs_in_tools = []
    print(funcs)
    for i in funcs:
        sig = inspect.signature(loc[i])
        all_params = dict(sig.parameters)
        fun = {
            "func_name" : i,
            "kwargs" : {},
            "tool_call_id" :i+"_unique_call_id"
        }
        for i in all_params:
            fun["kwargs"][str(i)] = all_params[i].default
        funs_in_tools.append(fun)
    funs_in_tools.append({"func_name": "final", "kwargs": {},"tool_call_id" :"SYSTEM_END_ALL"})
    return funs_in_tools

funcs = list(locals().keys())

if platform.system() == "Windows":
    funcs.remove("cast")
    funcs.remove("POINTER")
    funcs.remove("CLSCTX_ALL")
    funcs.remove("AudioUtilities")
    funcs.remove("IAudioEndpointVolume")

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
if "platform" in funcs:
    funcs.remove("platform")
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
    
