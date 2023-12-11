import json


def read_trace(filename):
    
    whole_trace = json.load(open(filename, 'r'))
    data = whole_trace['data']
    print(len(data))


if __name__ == "__main__":
    filename = 'jaeger_traces.json'
    read_trace(filename=filename)