import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

eda_df = pd.read_csv("/home/ubuntu/result/prepared_dataset.csv", sep=",")

# Chart1
# Sample data for multiple lines
x = eda_df['date']
y1 = eda_df['my_total_export']
y2 = eda_df['my_total_import']
y3 = eda_df['world_export']

# Create the figure and the first axis
fig, ax1 = plt.subplots(figsize=(12,6))

# Plot the first dataset on the first axis
ax1.plot(x, y1, color='b', label="Malaysia's Exports", linewidth = 1)
ax1.plot(x, y2, color='r', label="Malaysia's Imports", linewidth=0.5)

ax1.set_xlabel('Period')
ax1.set_ylabel('Amount (US Dollars, Billions)', color='black')
ax1.tick_params('y', colors='black')

# Create the second axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot the second dataset on the second axis
ax2.plot(x, y3, color='g', label="World's Exports",linewidth=0.5)

ax2.set_ylabel('Amount (US Dollars, Billions)', color='black')
ax2.tick_params('y', colors='black')

# Set the x-axis limits
ax1.set_xlim(eda_df['date'].min(), eda_df['date'].max())

#Show only every 24th tick and label
ax1.set_xticks(x[::12])
ax1.set_xticklabels(x[::12], rotation=90)  # Adjust rotation as needed


# Add a legend
ax1.set_title("Malaysia Exports vs Malaysia Imports and World's Exports")
ax1.legend(loc='upper left')
ax2.legend(loc='upper center')

# Save the plot as a JPEG file
plt.savefig('/home/ubuntu/result/figures/my-trade_vs_global-trade.jpg', format='jpeg')

# Chart 2
x = eda_df['date']
y = np.array(eda_df['trade_balance'], float)

# Create the figure and the axis
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the line
ax.plot(x, y, color='black', label='Trade Balance (US Dollars, Billions)', linewidth = 0.5)

# Fill the area above the zero line with green
ax.fill_between(x, y, where=(y >= 0), interpolate=True, color='lightgreen', alpha=0.5, label='Positive')

# Fill the area below the zero line with red
ax.fill_between(x, y, where=(y < 0), interpolate=True, color='red', alpha=1, label='Negative')

# Set labels and title
ax.set_xlabel('Period')
ax.set_ylabel('Trade Balance Amount')
ax.set_title('Trade Balance for Malaysia')
ax.axhline(0, color='black', linewidth=0.8, linestyle='--', label='Zero Line')  # Add a horizontal line at y=0
ax.legend()

# Set the x-axis limits
ax.set_xlim(eda_df['date'].min(), eda_df['date'].max())

#Show only every 24th tick and label
ax.set_xticks(x[::12])
ax.set_xticklabels(x[::12], rotation=90)  # Adjust rotation as needed

# Plot the legend
ax.legend()

# Save the plot as a JPEG file
plt.savefig('/home/ubuntu/result/figures/my-trade-balance.jpg', format='jpeg')

# Chart 3
# Sample data for multiple lines
x = eda_df['date']
y1 = eda_df['my_total_export']
y3 = eda_df['er']

# Create the figure and the first axis
fig, ax1 = plt.subplots(figsize=(12,6))

# Plot the first dataset on the first axis
ax1.plot(x, y1, color='b', label="Malaysia's Exports", linewidth = 1)
ax1.set_xlabel('Period')
ax1.set_ylabel('Amount (US Dollars, Billions)', color='black')
ax1.tick_params('y', colors='black')

# Create the second axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot the second dataset on the second axis
ax2.plot(x, y3, color='g', label='USDMYR Exchange Rate',linewidth=0.5)
ax2.set_ylabel('USDMYR Exchange Rate (MYR)', color='black')
ax2.tick_params('y', colors='black')

# Set the x-axis limits
ax1.set_xlim(eda_df['date'].min(), eda_df['date'].max())

#Show only every 24th tick and label
ax1.set_xticks(x[::12])
ax1.set_xticklabels(x[::12], rotation=90)  # Adjust rotation as needed
ax1.set_title("Malaysia's Exports vs USDMYR Exchange Rate")

# Add a legend
ax1.legend(loc='upper left')
ax2.legend(loc='upper center')

# Show the plot
plt.savefig('/home/ubuntu/result/figures/my-exports_vs_ER.jpg', format='jpeg')


# Chart 4
# Sample data for multiple lines
x = eda_df['date']
y1 = eda_df['my_total_export']
y3 = eda_df['rbeer']

# Create the figure and the first axis
fig, ax1 = plt.subplots(figsize=(12,6))

# Plot the first dataset on the first axis
ax1.plot(x, y1, color='b', label= "Malaysia's Exports", linewidth = 1)
ax1.set_xlabel('Period')
ax1.set_ylabel('Amount (US Dollars, Billions)', color='black')
ax1.tick_params('y', colors='black')

# Create the second axis sharing the same x-axis
ax2 = ax1.twinx()

# Plot the second dataset on the second axis
ax2.plot(x, y3, color='g', label='Real Broad Effective Exchange Rate',linewidth=0.5)
ax2.set_ylabel('Index 2020 = 100', color='black')
ax2.tick_params('y', colors='black')

# Set the x-axis limits
ax1.set_xlim(eda_df['date'].min(), eda_df['date'].max())

#Show only every 24th tick and label
ax1.set_xticks(x[::12])
ax1.set_xticklabels(x[::12], rotation=90)  # Adjust rotation as needed
ax1.set_title("Malaysia's Exports vs Real Broad Effective Exchange Rate for Malaysia")

# Add a legend
ax1.legend(loc='upper left')
ax2.legend(loc='upper center')

# Show the plot
plt.savefig('/home/ubuntu/result/figures/my-exports_vs_RBEER.jpg', format='jpeg')