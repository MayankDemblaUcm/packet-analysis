import os
import socket

import pandas as pd
import plotly.graph_objects as go

# Load the data from the CSV file
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
csv_path = os.path.join(root_dir, 'network_traffic.csv')
df = pd.read_csv(csv_path)

def get_domain(ip):
    try:
        domain = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        domain = "Unknown"
    return domain

# Group by source and destination to create flows
flows = df.groupby(['source_ip', 'destination_ip']).agg({
    'total_packets': 'sum',
    'packet_size': list,
    'inter_arrival_time': list,
    'temporal_patterns': list
}).reset_index()

# Create the table
table_data = []

for index, row in flows.iterrows():
    packet_details = "<br>".join([
        f"Mean size: {size} bytes, Flow time: {time} ms, total packets: {row['total_packets']}, time: {timestamp}"
        for size, time, timestamp in zip(row['packet_size'], row['inter_arrival_time'], row['temporal_patterns'])
    ])

    table_data.append([
        row['source_ip'] + '<br>(' + get_domain(row['source_ip']) +  ')',
        row['destination_ip'] + '<br>(' + get_domain(row['destination_ip']) +  ')',
        row['total_packets'],
        packet_details
    ])

fig = go.Figure(data=[go.Table(
    columnwidth=[200, 200, 50, 400],
    header=dict(
        values=["Source IP", "Destination IP", "Total Packets", "Packet Details"],
        fill_color='paleturquoise',
        align='left',
        font=dict(size=12)
    ),
    cells=dict(
        values=[list(col) for col in zip(*table_data)],
        fill_color='lavender',
        align='left',
        font=dict(size=10),
        height=30,
        format=[None, None, None, None],
        line_color='darkslategray',
    ))
])

# Update layout to make it scrollable and fit text
fig.update_layout(
    title="Scrollable Network Flow Table with Resized Columns",
    height=800,  # Adjust height to enable scrolling
    margin=dict(l=0, r=0, t=30, b=0),
)

fig.show()