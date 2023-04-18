import pandas as pd
import os
from jaeger_trace_parser import parse_jaeger_json, get_triggered_traces
from issue_localizer import evaluate_traces
from tracesampler import headSampling, retroactiveSampling


def hitrateeval(results):
    result = [0, 0, 0, 0]
    n = 1
    for serv in results['Service']:
        if serv == "compose_unique_id_server_v2":
            result[3] = 1/n
            if n <= 1:
                result[0] = 1
            if n <= 3:
                result[1] = 1
            if n <= 5:
                result[2] = 1
            
            return result
        n += 1
    return result

        

if __name__ == "__main__":
    directory = "/users/nikbapat/DeathStarBench/socialNetwork/jaeger-traces/s100"
    count = 0
    errors = 0
    heimdall_metrics = [0, 0, 0, 0]
    ochiai_metrics = [0, 0, 0, 0]
    tarantula_metrics = [0, 0, 0, 0]
    zoltar_metrics = [0, 0, 0, 0]
    wongii_metrics = [0, 0, 0, 0]



    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            count += 1
            print(count, errors)
            # print(file)
            traces = parse_jaeger_json(file)
            agg = get_triggered_traces(file, 0.9)

            

            if traces is None and agg is None:
                errors += 1
                count -= 1
                continue

            # traces, agg = headSampling(traces, agg, 0.2)
            traces, agg = retroactiveSampling(traces, agg, 0.6)

            res = evaluate_traces(traces, agg)

            heimdall = res.sort_values('Heimdall', ascending = False, ignore_index = True)
            metrics = hitrateeval(heimdall)
            heimdall_metrics[0] += metrics[0]
            heimdall_metrics[1] += metrics[1]
            heimdall_metrics[2] += metrics[2]
            heimdall_metrics[3] += metrics[3]

            ochiai = res.sort_values('Ochiai', ascending = False, ignore_index = True)
            metrics = hitrateeval(ochiai)
            ochiai_metrics[0] += metrics[0]
            ochiai_metrics[1] += metrics[1]
            ochiai_metrics[2] += metrics[2]
            ochiai_metrics[3] += metrics[3]

            # tarantula = res.sort_values('Tarantula', ascending = False, ignore_index = True)
            # metrics = hitrateeval(tarantula)
            # tarantula_metrics[0] += metrics[0]
            # tarantula_metrics[1] += metrics[1]
            # tarantula_metrics[2] += metrics[2]
            # tarantula_metrics[3] += metrics[3]

            # zoltar = res.sort_values('Zoltar', ascending = False, ignore_index = True)
            # metrics = hitrateeval(zoltar)
            # zoltar_metrics[0] += metrics[0]
            # zoltar_metrics[1] += metrics[1]
            # zoltar_metrics[2] += metrics[2]
            # zoltar_metrics[3] += metrics[3]

            # wongii = res.sort_values('Wong-II', ascending = False, ignore_index = True)
            # metrics = hitrateeval(wongii)
            # wongii_metrics[0] += metrics[0]
            # wongii_metrics[1] += metrics[1]
            # wongii_metrics[2] += metrics[2]
            # wongii_metrics[3] += metrics[3]

    print("Heimdall: HR1 " + str(heimdall_metrics[0]/count) + ", HR3 " + str(heimdall_metrics[1]/count) + ", HR5 " +str(heimdall_metrics[2]/count) + ", MRR " + str(heimdall_metrics[3]/count))
    print("Ochiai: HR1 " + str(ochiai_metrics[0]/count) + ", HR3 " + str(ochiai_metrics[1]/count) + ", HR5 " +str(ochiai_metrics[2]/count) + ", MRR " + str(ochiai_metrics[3]/count))        
    # print("Tarantula: HR1 " + str(tarantula_metrics[0]/count) + ", HR3 " + str(tarantula_metrics[1]/count) + ", HR5 " +str(tarantula_metrics[2]/count) + ", MRR " + str(tarantula_metrics[3]/count))
    # print("Zoltar: HR1 " + str(zoltar_metrics[0]/count) + ", HR3 " + str(zoltar_metrics[1]/count) + ", HR5 " +str(zoltar_metrics[2]/count) + ", MRR " + str(zoltar_metrics[3]/count))
    # print("Wong-II: HR1 " + str(wongii_metrics[0]/count) + ", HR3 " + str(wongii_metrics[1]/count) + ", HR5 " +str(wongii_metrics[2]/count) + ", MRR " + str(wongii_metrics[3]/count))
