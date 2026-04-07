import json

def parse_response(response):
    try:
        x = json.loads(response)
        #print(x, type(x))
        return json.loads(response)
    except:
        return response