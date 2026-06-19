import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("../data/disney_plus_titles.csv")

# Remove duplicates
df = df.drop_duplicates()

# Remove rows without title
df = df.dropna(subset=["title"])

# Clean whitespace
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].str.strip()

# Convert date_added
df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

# Create Year Added
df["year_added"] = df["date_added"].dt.year

# Extract duration number
df["duration_num"] = (
    df["duration"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(float)
)

# Missing value flags
df["country_missing"] = df["country"].isna()
df["director_missing"] = df["director"].isna()
df["cast_missing"] = df["cast"].isna()
df["rating_missing"] = df["rating"].isna()
df["genre_missing"] = df["listed_in"].isna()

# Fill missing values
df["country"] = df["country"].fillna("Unknown Country")
df["director"] = df["director"].fillna("Unknown Director")
df["cast"] = df["cast"].fillna("Unknown Cast")
df["rating"] = df["rating"].fillna("Not Rated")
df["listed_in"] = df["listed_in"].fillna("Unknown Genre")

# Remove impossible release years
df = df[
    (df["release_year"] >= 1900) &
    (df["release_year"] <= 2030)
]

# Save cleaned file
df.to_csv(
    "../data/clean_disney_plus_titles.csv",
    index=False
)

print("Cleaning completed successfully")
print("Rows:", len(df))