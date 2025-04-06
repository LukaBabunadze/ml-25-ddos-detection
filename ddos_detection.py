import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re

# Function to parse log lines, keeping original timezone
def parse_log_line(line):
    pattern = r'\[(.*?)\]'
    match = re.search(pattern, line)
    if match:
        timestamp_str = match.group(1)
        try:
            # Parse timestamp as-is (e.g., 2024-03-22 18:00:46+04:00)
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S%z')
            return timestamp
        except ValueError as e:
            print(f"Error parsing timestamp '{timestamp_str}': {e}")
            return None
    return None

# Read and parse the log file
# For this example, I'll simulate reading your provided log snippet
# Replace this with actual file reading if you have the full log saved
log_file = "luka_babunadze_1_server.log"  # Replace with your log file name or use the provided data
timestamps = []

# If using a file, replace this block with file reading
with open(log_file, 'r') as file:
    for line in file:
        timestamp = parse_log_line(line)
        if timestamp:
            timestamps.append(timestamp)

# Convert timestamps to a DataFrame
df = pd.DataFrame(timestamps, columns=['timestamp'])

# Group by 10-second intervals
df['interval'] = df['timestamp'].dt.floor('10s')
request_counts = df.groupby('interval').size().reset_index(name='count')

# Debugging: Print time range and max request count
print(f"Time range: {request_counts['interval'].min()} to {request_counts['interval'].max()}")
max_count_row = request_counts.loc[request_counts['count'].idxmax()]
print(f"Max requests: {max_count_row['count']} at {max_count_row['interval']}")

# Calculate rolling mean and standard deviation (window of 5 intervals, ~50 seconds)
request_counts['rolling_mean'] = request_counts['count'].rolling(window=5, center=True).mean()
request_counts['rolling_std'] = request_counts['count'].rolling(window=5, center=True).std()

# Define a threshold for detecting anomalies (mean + 2*std)
request_counts['threshold'] = request_counts['rolling_mean'] + 2 * request_counts['rolling_std']

# Identify potential DDoS attack times
ddos_candidates = request_counts[request_counts['count'] > request_counts['threshold']]

# Print detected DDoS attack times
print("Potential DDoS Attack Times:")
for index, row in ddos_candidates.iterrows():
    print(f"Time: {row['interval']}, Request Count: {row['count']}")

# Visualization
plt.figure(figsize=(14, 7))
plt.plot(request_counts['interval'], request_counts['count'], label='Requests per 10s', color='blue')
plt.plot(request_counts['interval'], request_counts['rolling_mean'], label='Rolling Mean', color='green', linestyle='--')
plt.plot(request_counts['interval'], request_counts['threshold'], label='Threshold (Mean + 2*STD)', color='red', linestyle='--')
plt.scatter(ddos_candidates['interval'], ddos_candidates['count'], color='red', label='Potential DDoS Attacks', zorder=5)
plt.xlabel('Time (+04:00)')
plt.ylabel('Number of Requests')
plt.title('Request Frequency Analysis for DDoS Detection (10s Intervals)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig('ddos_detection_plot.png')
plt.show()

# Regression analysis
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.arange(len(request_counts)).reshape(-1, 1)  # Time index
y = request_counts['count'].values

model = LinearRegression()
model.fit(X, y)
trend_line = model.predict(X)

# Regression plot
plt.figure(figsize=(14, 7))
plt.plot(request_counts['interval'], request_counts['count'], label='Requests per 10s', color='blue')
plt.plot(request_counts['interval'], trend_line, label='Regression Trend', color='orange', linestyle='--')
plt.xlabel('Time (+04:00)')
plt.ylabel('Number of Requests')
plt.title('Regression Analysis of Request Frequency')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save the regression plot
plt.savefig('regression_analysis_plot.png')
plt.show()

# Print regression details
print(f"Regression Slope (Requests per 10s): {model.coef_[0]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")