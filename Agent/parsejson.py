import json

def parse_response(response):
    try:
        x = json.loads(response)
        #print(x, type(x))
        return json.loads(response)
    except:
        return json.loads(extract_json(response))

def extract_json(text):
    start = text.find('{')
    if start == -1:
        raise ValueError("No JSON found")

    depth = 0
    for i in range(start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start:i+1]

    raise ValueError("Unbalanced JSON")