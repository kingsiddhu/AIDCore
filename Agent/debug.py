

BOLD = "\x1B[1m"
UNDER = "\x1B[4m"
RESET = "\x1B[0m"

COL_BLA = "\x1B[90m"
COL_RED = "\x1B[91m"
COL_GRE = "\x1B[92m"
COL_YEL = "\x1B[93m"
COL_BLU = "\x1B[94m"
COL_MAG = "\x1B[95m"
COL_CYN = "\x1B[96m"
COL_WHI = "\x1B[97m"

FOR_BLA = "\x1B[100m"
FOR_RED = "\x1B[101m"
FOR_GRE = "\x1B[102m"
FOR_YEL = "\x1B[103m"
FOR_BLU = "\x1B[104m"
FOR_MAG = "\x1B[105m"
FOR_CYN = "\x1B[106m"
FOR_WHI = "\x1B[107m"

def logger(data):
    print()
    if type(data) is dict:
        print_dict(data)
    elif type(data) is list:
        print_list(data)
    else:
        print(COL_MAG+data+RESET)
    print()

def print_dict(dic:dict, level=1):
    print("    "*(level-1) + "{")
    for i in dic.keys():
        if type(dic[i]) is dict:
            print_dict(dic[i], level+1)
        elif type(dic[i]) is str:
            print("    "*level +  COL_GRE + "\"" + i + "\"" + RESET + " : " + COL_BLU + "\"" + dic[i] + "\"" + RESET + ",")
        else:
            print("    "*level +  COL_GRE + "\"" + i + "\"" + RESET + " : " + COL_MAG + str(dic[i]) + RESET + ",")
    print("    "*(level-1) + "}")

def print_list(lis:list, level=1):
    print("    "*(level-1) + "[")
    for i in lis:
        if type(i) is dict:
            print_dict(i, level+1)
        elif type(i) is list:
            print_list(i, level+1)
        else:
            print("    "*level + COL_MAG +str(i)+RESET + ",")
    print("    "*(level-1) + "]")
