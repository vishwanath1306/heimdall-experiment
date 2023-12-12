import json
from typing import Dict


def read_trace(file_name: str) -> Dict:
    return json.load(open(filename, 'r'))


'''
"2407890": {
        "width": 640,
        "height": 480,
        "location": "living room",
        "weather": none,
        "objects": {
            "271881": {
                "name": "chair",
                "x": 220,
                "y": 310,
                "w": 50,
                "h": 80,
                "attributes": ["brown", "wooden", "small"],
                "relations": {
                    "32452": {
                        "name": "on",
                        "object": "275312"
                    },
                    "32452": {
                        "name": "near",
                        "object": "279472"
                    }                    
                }
            }
        }
    }
    
'''
def convert_to_scene_graph(individual_trace):
    scene_graph_dict = {}
    scene_graph_dict[individual_trace['traceID']] = {}
    scene_graph_dict[individual_trace['traceID']]['location'] = None
    scene_graph_dict[individual_trace['traceID']]['objects'] = {}

    current_spans = individual_trace['spans']
    for span in current_spans:
        if span['traceID'] == span['spanID']:
            scene_graph_dict[individual_trace['traceID']]['location'] = span['operationName']
    print(scene_graph_dict)


if __name__ == "__main__":
    filename = 'jaeger_traces.json'
    jaeger_traces = read_trace(file_name=filename)
    for trace in jaeger_traces['data']:
        convert_to_scene_graph(trace)
