"""Functions for loading and cleaning the employee data."""

import pandas as pd

REQUIRED_COLUMNS = [
    "employee_id", "name", "age", "department",
    "salary", "experience", "performance",
]
NUMERIC_COLUMNS = ["employee_id", "age", "salary", "experience", "performance"]


def load_data(file_path):
    """Load the CSV file. Returns a DataFrame, or None if something is wrong."""
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: file not found -> {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: the file is empty -> {file_path}")
        return None
    except pd.errors.ParserError:
        print(f"Error: the file is not formatted correctly -> {file_path}")
        return None

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        print(f"Error: missing required columns: {missing_cols}")
        return None

    print("First 5 records:")
    print(df.head())
    print(f"\nTotal records loaded: {len(df)}")
    return df


def clean_data(df):
    """Clean the DataFrame and return the valid records."""
    df = df.copy()
    start = len(df)

    # 1. Remove exact duplicate rows
    df = df.drop_duplicates()

    # 2. Treat blank names/departments as missing
    for col in ["name", "department"]:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)

    # 3. Convert numeric columns (bad values like "abc" become NaN)
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4. Remove rows with missing required fields
    print("\nMissing values per column:")
    print(df[REQUIRED_COLUMNS].isna().sum())
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # 5. Remove invalid values
    df = df[
        (df["age"] > 0)
        & (df["salary"] >= 0)
        & (df["experience"] >= 0)
        & (df["performance"].between(0, 100))
    ]

    # 6. employee_id must be unique
    df = df.drop_duplicates(subset="employee_id", keep="first")

    # 7. Use suitable data types
    df = df.astype({
        "employee_id": int,
        "age": int,
        "salary": float,
        "experience": float,
        "performance": float,
    })

    df = df.reset_index(drop=True)
    print(f"\nCleaning finished: {start} records -> {len(df)} valid records "
          f"({start - len(df)} removed)")
    return df
