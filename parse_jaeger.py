import json

def read_trace(filename):
    
    whole_trace = json.load(open(filename, 'r'))
    # print(whole_trace.keys())
    # print(type(whole_trace['data']), 
    #       type(whole_trace['total']), 
    #       type(whole_trace['limit']), 
    #       type(whole_trace['offset']),
    #       whole_trace['errors'])
    
    data = whole_trace['data']
    # print(data.keys())
    # print(len(data))
    # print(data[0].keys())
    # for key in data[0].keys():
    #     print(key, data[0][key])

    first_data = data[0]
    print(type(first_data['traceID']),
          type(first_data['spans']),
          type(first_data['processes']),
          type(first_data['warnings']))
    span_data = first_data['spans']
    # print(span_data[0].keys())
    for key in span_data[0].keys():
        print(key, type(span_data[0][key]))
    


if __name__ == "__main__":
    filename = 'jaeger_traces.json'
    read_trace(filename=filename)