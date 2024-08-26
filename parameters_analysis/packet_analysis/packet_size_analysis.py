import os

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data from the CSV file
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
csv_path = os.path.join(root_dir, 'network_traffic.csv')
df = pd.read_csv(csv_path)

# Display basic statistics about packet sizes
print(df['packet_size'].describe())

# Check for missing values in packet size
print(df['packet_size'].isnull().sum())

# Set visualization style
sns.set(style="whitegrid")

# Plot the distribution of packet sizes
plt.figure(figsize=(10, 6))
sns.histplot(df['packet_size'], kde=True, bins=50)
plt.title('Distribution of Packet Sizes')
plt.xlabel('Packet Size (Bytes)')
plt.ylabel('Frequency')
plt.show()

###
ax = sns.histplot(df['packet_size'], bins=30, kde=True)

# Get the x and y values for the KDE line
kde_x = np.linspace(df['packet_size'].min(), df['packet_size'].max(), 100)
kde_y = sns.kdeplot(df['packet_size'], bw_adjust=1).get_lines()[0].get_ydata()

# Annotate the KDE line with frequency values
for i in range(0, len(kde_x), 5):  # Adjust step (5) to control the number of annotations
    plt.annotate(f'{kde_y[i]:.2f}', xy=(kde_x[i], kde_y[i]), xytext=(0, 5),
                 textcoords='offset points', ha='center', fontsize=8, color='blue')

plt.title('Packet Size Distribution with Frequency Annotations')
plt.xlabel('Packet Size (bytes)')
plt.ylabel('Frequency')
plt.show()

###

# Assuming you have a timestamp column
df['temporal_patterns'] = pd.to_datetime(df['temporal_patterns'])

# Plot packet sizes over time
plt.figure(figsize=(14, 7))
sns.lineplot(x='temporal_patterns', y='packet_size', data=df)
plt.title('Packet Sizes Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Packet Size (Bytes)')
plt.show()

# Plot a boxplot of packet sizes to detect outliers
plt.figure(figsize=(10, 6))
sns.boxplot(x='packet_size', data=df)
plt.title('Box Plot of Packet Sizes')
plt.xlabel('Packet Size (Bytes)')
plt.show()

# Scatter plot of packet size vs. source port
plt.figure(figsize=(10, 6))
sns.scatterplot(x='source_port', y='packet_size', data=df)
plt.title('Packet Size vs. Source Port')
plt.xlabel('Source Port')
plt.ylabel('Packet Size (Bytes)')
plt.show()

# Scatter plot of packet size vs. destination port
plt.figure(figsize=(10, 6))
sns.scatterplot(x='destination_port', y='packet_size', data=df)
plt.title('Packet Size vs. Destination Port')
plt.xlabel('Destination Port')
plt.ylabel('Packet Size (Bytes)')
plt.show()

# Density plot of packet sizes
plt.figure(figsize=(10, 6))
sns.kdeplot(df['packet_size'], shade=True)
plt.title('Density Plot of Packet Sizes')
plt.xlabel('Packet Size (Bytes)')
plt.ylabel('Density')
plt.show()

# Calculate z-scores for packet size
df['z_score'] = (df['packet_size'] - df['packet_size'].mean()) / df['packet_size'].std()

# Flag anomalies (e.g., z-score > 3 or < -3)
anomalies = df[(df['z_score'] > 3) | (df['z_score'] < -3)]
print("Anomalous Packets Detected:")
print(anomalies[['temporal_patterns', 'source_ip', 'destination_ip', 'packet_size', 'protocol']])

# Visualize the anomalies
plt.figure(figsize=(14, 7))
sns.scatterplot(x='temporal_patterns', y='packet_size', data=df, hue=(df['z_score'].abs() > 3), palette={False: 'blue', True: 'red'})
plt.title('Packet Sizes Over Time with Anomalies Highlighted')
plt.xlabel('Timestamp')
plt.ylabel('Packet Size (Bytes)')
plt.show()

