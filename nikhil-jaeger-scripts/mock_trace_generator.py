import pandas as pd
import random


def generate_mock_trace(traceID, services, versions, percent_error, badService = 0, badVersion = 0): 
    records = pd.DataFrame(columns = ['TraceID', 'Service', 'Duration'])

    for s in range(services):
        version = random.randint(1,3)
        service_version = "s" + str(s) + "v" + str(version)
        latency = random.uniform(98.0, 102.0)
        if s == badService and version == badVersion:
            latency += percent_error
        records.loc[len(records)] = [traceID, service_version, latency]
    
    return records



def create_mock_dataset(numTraces, num_services, num_versions, trigger_quantile, percent_error, output_suffix):
    traceServices = pd.DataFrame(columns = ['TraceID', 'Service', 'Duration'])

    for i in range(numTraces):
        id = "t_000" + str(i)
        traceServices = pd.concat([traceServices, generate_mock_trace(i, num_services, num_versions, percent_error, 3, 3)]) #manually injecting latency into service 3 node 3

    traceAggregates = traceServices.groupby('TraceID').sum(numeric_only=True)
    threshold = traceAggregates.quantile(trigger_quantile)['Duration']
    traceAggregates['Triggered'] = traceAggregates['Duration'] > threshold

    traceServices.to_csv('clean_traces/mock_services_' + output_suffix + '.csv', index=False)
    traceAggregates.to_csv('clean_traces/mock_aggregates_'+ output_suffix+ '.csv')


create_mock_dataset(100, 5, 3, 0.9, 5, 'small')
create_mock_dataset(100, 5, 3, 0.9, 2, 'small_lowerror')
create_mock_dataset(1000, 10, 3, 0.9, 5, 'medium')
create_mock_dataset(1000, 10, 3, 0.9, 2, 'medium_lowerror')
create_mock_dataset(1000, 10, 3, 0.99, 10, 'medium_highthreshold')
create_mock_dataset(5000, 10, 3, 0.9, 5, 'large')