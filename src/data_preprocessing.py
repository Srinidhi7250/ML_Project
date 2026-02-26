import pandas as pd

# 1️ Load raw dataset
raw_path = "../data/raw/study_data.csv"
df = pd.read_csv(raw_path)

# 2️ Data Cleaning
df = df.dropna()          # remove missing values
df = df.drop_duplicates() # remove duplicate rows

# 3 Save cleaned dataset
processed_path = "../data/processed/clean_study_data.csv"
df.to_csv(processed_path, index=False)

print(" Processed file created successfully!")
print("Saved at:", processed_path)