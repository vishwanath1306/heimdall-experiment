import json
from typing import Dict


def read_trace(file_name: str) -> Dict:
    return json.load(open(filename, 'r'))


'''
"2407890": {
        "location": "living room",
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


def convert_to_scene_graph(individual_trace: Dict) -> Dict:
    scene_graph_dict = {individual_trace['traceID']: {}}
    scene_graph_dict[individual_trace['traceID']]['location'] = None
    scene_graph_dict[individual_trace['traceID']]['objects'] = {}

    current_spans = individual_trace['spans']

    objects_dict = {}
    for span in current_spans:
        objects_dict[span['spanID']] = {"name" : span['operationName']}
        
        if span['traceID'] == span['spanID']:
            scene_graph_dict[individual_trace['traceID']]['location'] = span['operationName']

    for span in current_spans:
        for ref in span['references']:
            if ref['refType'] == 'CHILD_OF':
                objects_dict[ref['spanID']]['relations'] = {"name": "child of", "object": span['spanID']}
    scene_graph_dict[individual_trace['traceID']]['objects'] = objects_dict 
    return scene_graph_dict

def convert_traces(jaeger_traces: Dict, op_file_name: str):
    scene_graph_jsons = {}

    for trace in jaeger_traces['data']:
        scene_g  = convert_to_scene_graph(trace)
        scene_graph_jsons.update(scene_g)
    json.dump(scene_graph_jsons, open(op_file_name, 'w'), indent=4)

if __name__ == "__main__":
    filename = 'jaeger_traces.json'
    curr_traces = read_trace(file_name=filename)
    convert_traces(curr_traces, 'scene_graph.json')
