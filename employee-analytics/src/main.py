"""Entry point. Run from the project root with:  python -m src.main"""

from pathlib import Path

from src.analysis import calculate_statistics, create_charts, filter_employees
from src.data_loader import clean_data, load_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "employees.csv"
CHARTS_DIR = PROJECT_ROOT / "output" / "charts"


def main():
    df = load_data(DATA_FILE)
    if df is None:
        return  # loading failed; the error was already printed

    clean_df = clean_data(df)
    if clean_df.empty:
        print("No valid records left after cleaning.")
        return

    calculate_statistics(clean_df)
    filter_employees(clean_df)
    create_charts(clean_df, CHARTS_DIR)


if __name__ == "__main__":
    main()
