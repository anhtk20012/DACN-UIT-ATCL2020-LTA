import pandas as pd

nodes = pd.DataFrame({
    'id': [1, 2],
    'node_label': ['label1', 'label2'],
    'lineNumber': [100, 200],
    'extra_column': ['extra1', 'extra2']  
})

data_to_append = {"id": 3, "node_label": "label3", "lineNumber": 300}

nodes = nodes.append(data_to_append, ignore_index=True)

print(nodes)