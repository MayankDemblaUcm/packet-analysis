import os

import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt

# Load the network traffic data
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
csv_path = os.path.join(root_dir , 'network_traffic.csv')
df = pd.read_csv(csv_path)

# Aggregate data to reduce complexity
# Group by Source IP and Destination IP, then aggregate ports
agg_df = df.groupby(['source_ip', 'destination_ip']).agg({
    'source_port': lambda x: ','.join(map(str, set(x))),
    'destination_port': lambda x: ','.join(map(str, set(x)))
}).reset_index()

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph with aggregated port information
for _, row in agg_df.iterrows():
    G.add_edge(row['source_ip'], row['destination_ip'],
               label=f"{row['source_port']}->{row['destination_port']}")

# Simplify the layout
pos = nx.spring_layout(G, k=0.15, iterations=20)

# Draw the graph with simpler design
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000, font_size=8, font_weight='bold', edge_color='gray')
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color='red')

plt.title('Simplified Network Traffic Visualization')
plt.show()
