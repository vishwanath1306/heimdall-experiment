import pandas as pd
import math
import sys
from jaeger_trace_parser import parse_jaeger_json, get_triggered_traces


def bayesfactor(et, eh, nt, nh): #e is segment executed, n is segment not executed, t is triggered, and h is healthy
    if (et+nt) == 0:
        num = 0
    else:
        num = et / (et + nt)
    den = eh / (eh + nh)
    if den == 0:
        return sys.maxsize
    return num/den

def ochiai(et, eh, nt, nh): #e is segment executed, n is segment not executed, t is triggered, and h is healthy
    prod = (et + nt) * (et + eh)
    den = math.sqrt(prod)
    if den == 0:
        return sys.maxsize
    return et/den


def tarantula(et, eh, nt, nh): #e is segment executed, n is segment not executed, t is triggered, and h is healthy
    if (et+nt) == 0:
        num = 0
    else:
        num = et / (et + nt)
    den = (num) + (eh / (eh + nh))
    if den == 0:
        return sys.maxsize
    return num/den

def zoltar(et, eh, nt, nh): #e is segment executed, n is segment not executed, t is triggered, and h is healthy
    if et == 0:
        aug = 0
    else:
        aug = (10000 * nt * eh) / et
    den = et + nt + eh + aug
    if den == 0:
        return sys.maxsize
    return et/den

def wongii(et, eh, nt, nh): #e is segment executed, n is segment not executed, t is triggered, and h is healthy
    return et - eh


def get_service_counts(service, traces_df, triggeredTraces, notTriggeredTraces):
    executed = traces_df[traces_df["Service"] == service]
    #print(executed)
    executedTraces = executed['TraceID']
    #print(triggeredTraces)
    # print(set(executedTraces) & set(triggeredTraces))
    # print(set(executedTraces) & set(notTriggeredTraces))

    triggered_included = len(set(executedTraces) & set(triggeredTraces))
    notrigger_included = len(set(executedTraces) & set(notTriggeredTraces))
    triggered_excluded = len(triggeredTraces) - triggered_included
    notrigger_excluded = len(notTriggeredTraces) - notrigger_included
    stat = [service, triggered_included, notrigger_included, triggered_excluded, notrigger_excluded]
    #print(stat)
    return stat


def evaluate_traces(traceRecords, traceAggregates):
    # traceRecords = pd.read_csv(traceFile)
    # traceAggregates = pd.read_csv(aggFile)

    serviceList = traceRecords['Service'].unique()

    triggeredTraces = traceAggregates[traceAggregates['Triggered']]['TraceID']
    notTriggeredTraces = traceAggregates[traceAggregates['Triggered'] == False]['TraceID']


    stats = pd.DataFrame(columns = ['Service', 'exec_trig', 'exec_notrig', 'noexec_trig', 'noexec_notrig'])
    for service in serviceList:
        stats.loc[len(stats.index)] = get_service_counts(service, traceRecords, triggeredTraces, notTriggeredTraces)


    stats['Heimdall'] = stats.apply(lambda x: bayesfactor(x['exec_trig'], x['exec_notrig'], x['noexec_trig'], x['noexec_notrig']), axis=1)
    stats['Ochiai'] = stats.apply(lambda x: ochiai(x['exec_trig'], x['exec_notrig'], x['noexec_trig'], x['noexec_notrig']), axis=1)
    stats['Tarantula'] = stats.apply(lambda x: tarantula(x['exec_trig'], x['exec_notrig'], x['noexec_trig'], x['noexec_notrig']), axis=1)
    stats['Zoltar'] = stats.apply(lambda x: zoltar(x['exec_trig'], x['exec_notrig'], x['noexec_trig'], x['noexec_notrig']), axis=1)
    stats['Wong-II'] = stats.apply(lambda x: wongii(x['exec_trig'], x['exec_notrig'], x['noexec_trig'], x['noexec_notrig']), axis=1)


    stats = stats.sort_values('Heimdall', ascending = False, ignore_index = True)
    return stats
    


if __name__ == "__main__":
    file = "/users/nikbapat/DeathStarBench/socialNetwork/jaeger-traces/test/20230325182546"
    traces = parse_jaeger_json(file)
    agg = get_triggered_traces(file, 0.9)
    res = evaluate_traces(traces, agg)
    print(res)