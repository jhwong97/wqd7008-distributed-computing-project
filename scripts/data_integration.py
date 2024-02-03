import pandas as pd

df_exmaus=pd.read_csv("/home/ubuntu/result/EXMAUS_data_transformed.csv", sep=",").drop("realtime_start",axis=1).drop_duplicates(subset='date')

df_rbmybis=pd.read_csv("/home/ubuntu/result/RBMYBIS_data_transformed.csv", sep=",").drop("realtime_start", axis=1).drop_duplicates(subset='date')

df_export=pd.read_csv("/home/ubuntu/result/export_data_transformed.csv", sep=",")
df_export=df_export[['date', 'total_export']]

df_import=pd.read_csv("/home/ubuntu/result/import_data_transformed.csv", sep=",")
df_import=df_import[['date', 'total_import']]

df_world_export=pd.read_csv("/home/ubuntu/result/W00-W00_data_transformed.csv", sep=",")
df_world_export=df_world_export[['date','world_export']]

result_df = pd.merge(df_export, df_import, on='date', how='left')
result_df = pd.merge(result_df, df_exmaus, on='date', how='left')
result_df = pd.merge(result_df, df_rbmybis, on='date', how='left')
result_df = pd.merge(result_df, df_world_export, on='date', how='left')

file_path = "/home/ubuntu/result/integrated_dataset.csv"
result_df.to_csv(file_path,index=False)