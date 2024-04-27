import pandas as pd

columns = ['venue']
for i in range(18):
    columns.append(f"horse{i+1}_onehourago_win")
for i in range(18):
    columns.append(f"horse{i+1}_onehourago_place_min")
    columns.append(f"horse{i+1}_onehourago_place_max")
for i in range(18):
    columns.append(f"horse{i+1}_thirtyminago_win")
for i in range(18):
    columns.append(f"horse{i+1}_thirtyminago_place_min")
    columns.append(f"horse{i+1}_thirtyminago_place_max")
for i in range(18):
    columns.append(f"horse{i+1}_tenminago_win")
for i in range(18):
    columns.append(f"horse{i+1}_tenminago_place_min")
    columns.append(f"horse{i+1}_tenminago_place_max")

df = pd.DataFrame(columns=columns)
df.to_csv("../data/odds_result.csv", index=False)