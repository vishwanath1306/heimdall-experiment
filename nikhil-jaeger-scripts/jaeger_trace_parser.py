import json
import pandas as pd

def parse_jaeger_json(file):
    records = pd.DataFrame(columns = ['TraceID', 'Service', 'Duration'])
    whole_trace = json.load(open(file, 'r'))
    if whole_trace['data'] is None:
        return None
    for req in whole_trace['data']:
        for span in req['spans']:
            vers = ''
            tags = span['tags']
            if tags[0]['key'] == "ServiceVersion":
                vers = '_' + tags[0]['value']
            records.loc[len(records)] = [span['traceID'], span['operationName']+vers, span['duration']]
    
    return records

def get_triggered_traces(file, trigger_quantile):
    traceAggregates = pd.DataFrame(columns = ['TraceID', 'Duration'])
    whole_trace = json.load(open(file, 'r'))
    if whole_trace['data'] is None:
        return None
    for req in whole_trace['data']:
        for span in req['spans']:
            if span["operationName"] == "/wrk2-api/post/compose" and len(span['references']) == 0:
                traceAggregates.loc[len(traceAggregates)] = [span['traceID'], span['duration']]

    threshold = traceAggregates.quantile(q = trigger_quantile, numeric_only = True)['Duration']
    traceAggregates['Triggered'] = traceAggregates['Duration'] > threshold

    return traceAggregates
    

# if __name__ == "__main__":
#     filename = '../DeathStarBench/socialNetwork/jaeger-traces/tests/try2' #just a test set, change how input works
#     aggs = get_triggered_traces(filename, 0.9)
#     print(aggs)
#     print(aggs['Triggered'].value_counts())