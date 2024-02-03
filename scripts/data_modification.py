import pandas as pd

# Data modification
print("Modifying dataset for eda and modelling usage...")
df = pd.read_csv("/home/ubuntu/result/integrated_dataset.csv", sep=",")
df = df.drop_duplicates().dropna()
eda_df = df.copy()

column_names = ['date', 'my_total_export', 'my_total_import', 'er', 'rbeer', 'world_export']
eda_df.columns = column_names
eda_df['my_total_export'] = (eda_df['my_total_export']/eda_df['er'])/10**9
eda_df['my_total_import'] = (eda_df['my_total_import']/eda_df['er'])/10**9
eda_df['world_export'] = (eda_df['world_export']*(10**6))/10**9
eda_df['trade_balance'] = eda_df['my_total_export'] - eda_df['my_total_import']

eda_df.to_csv("/home/ubuntu/result/prepared_dataset.csv", index=False)
print("SUCCESS: Dataset for EDA and Modelling is ready.")