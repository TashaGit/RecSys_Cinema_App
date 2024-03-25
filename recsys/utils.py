import json

from typing import List



def parse(parsed_column) -> List:
    L = []
    data = json.loads(parsed_column)
    for i in data:
        L.append(i['name'])
    return L
