import pandas as pd
from coordinates_translate import convert_cor as cvr

df_water_quality = pd.read_csv("Amsterdam2007-2023_utf-8.csv", encoding='utf-8',  low_memory=False)

filtered_df = df_water_quality[df_water_quality['fewsparameternaam'] == "Escherichia coli (uitgedrukt in KVE/dl)"]

filtered_df.to_csv("filtered_data.csv", index=False)
