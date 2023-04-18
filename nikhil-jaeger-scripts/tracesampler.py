import pandas as pd
from jaeger_trace_parser import parse_jaeger_json, get_triggered_traces


def headSampling(traces, agg, rate):
    if rate == 1.0:
        return traces, agg
    else:
        subAgg = agg.sample(frac=rate, replace=False)
        subTrace = traces[traces['TraceID'].isin(subAgg['TraceID'])]
        return subTrace, subAgg


def retroactiveSampling(traces, agg, rate):
    if rate == 1.0:
        return traces, agg
    else:
        triggered = agg[agg['Triggered'] == True]
        healthy = agg[agg['Triggered'] == False]
        healthy_needed = int(len(agg) * rate)
        healthy_needed -= len(triggered)
        randHealthy = healthy.sample(n = healthy_needed, replace=False)

        subAgg = pd.concat([triggered, randHealthy])
        subTrace = traces[traces['TraceID'].isin(subAgg['TraceID'])]
        return subTrace, subAgg


if __name__ == "__main__":
    file = '/users/nikbapat/DeathStarBench/socialNetwork/jaeger-traces/s100/20230326131427'
    traces = parse_jaeger_json(file)
    agg = get_triggered_traces(file, 0.9)

    # head = headSampling(traces, agg, 0.5)
    # print(head[0])
    # print(head[1])
    # print(head[1]['Triggered'].value_counts())

    retro = retroactiveSampling(traces, agg, 0.5)
    print(retro[0])
    print(retro[1])
    print(retro[1]['Triggered'].value_counts())