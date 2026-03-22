import os
if __name__ =="__main__":
    import debug
else:
    import Agent.debug

def listFiles(path="./"):
    dirs=os.listdir(path)
    Agent.debug.logger(dirs)
    return dirs








def get_funcs():
    import inspect
    global funcs, loc
    funs_in_tools = []
    for i in funcs:
        sig = inspect.signature(loc[i])
        all_params = dict(sig.parameters)
        fun = {
            "function_name" : i,
            "kwargs" : {}
        }
        for i in all_params:
            fun["kwargs"][str(i)] = all_params[i].default
        funs_in_tools.append(fun)
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
funcs.remove("os")
try:
    funcs.remove("debug")
except:
    pass
try:
    funcs.remove("Agent.debug")
except:
    pass

loc = locals()
if __name__ == "__main__":
    import debug
    print(funcs)
    print(get_funcs())
    debug.logger(get_funcs())