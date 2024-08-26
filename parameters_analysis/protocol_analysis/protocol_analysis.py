import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load the data from the CSV file
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
csv_path = os.path.join(root_dir, 'network_traffic.csv')
df = pd.read_csv(csv_path)

# Display basic statistics about the dataset
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Display unique protocols
print("Unique Protocols:", df['protocol'].unique())

# Set the style of the visualizations
sns.set(style="whitegrid")

# Plot the distribution of protocols
plt.figure(figsize=(10, 6))
sns.countplot(x='protocol', data=df)
plt.title('Protocol Distribution')
plt.xlabel('Protocol')
plt.ylabel('Count')
plt.show()

# Feature engineering: count unique protocols per source IP
protocol_counts = df.groupby('source_ip')['protocol'].nunique().reset_index()
protocol_counts.columns = ['source_ip', 'unique_protocol_count']

# Merge with the original dataframe
df = pd.merge(df, protocol_counts, on='source_ip')

# Display the updated dataframe
print(df.head())

# Standardize the features for anomaly detection
features = ['source_port', 'destination_port', 'unique_protocol_count']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# Apply Isolation Forest for anomaly detection
isolation_forest = IsolationForest(contamination=0.01, random_state=42)
df['anomaly_score'] = isolation_forest.fit_predict(X_scaled)

# Plot the anomalies
plt.figure(figsize=(10, 6))
sns.scatterplot(x='source_port', y='destination_port', hue='anomaly_score', data=df, palette={-1: 'red', 1: 'blue'})
plt.title('Anomaly Detection in Network Traffic')
plt.xlabel('Source Port')
plt.ylabel('Destination Port')
plt.show()

# Apply DBSCAN for clustering
dbscan = DBSCAN(eps=0.5, min_samples=5)
df['cluster'] = dbscan.fit_predict(X_scaled)

# Visualize the clustering
plt.figure(figsize=(10, 6))
sns.scatterplot(x='source_port', y='destination_port', hue='cluster', data=df, palette='Set1')
plt.title('DBSCAN Clustering of Network Traffic')
plt.xlabel('Source Port')
plt.ylabel('Destination Port')
plt.show()

# Analyze potential intrusions by filtering anomalies
anomalies = df[df['anomaly_score'] == -1]
print("Potential Intrusions Detected:")
print(anomalies[['source_ip', 'destination_ip', 'protocol', 'source_port', 'destination_port']])
