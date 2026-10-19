# Employee Data Analytics System

## Objective
Load employee data from a CSV file, clean it, analyze it, and generate charts for management.

## Technologies
Python 3, Pandas, NumPy, Matplotlib, Git & GitHub

## Installation
```bash
git clone <your-repo-url>
cd employee-analytics
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

## Run
```bash
python -m src.main
```

## Features
- Loads `data/employees.csv` with error handling (missing, empty, badly formatted file)
- Cleans data: duplicates, missing values, wrong types, invalid values, unique IDs
- Statistics: count, average age/salary/experience, highest/lowest salary, average salary per department
- Filters: salary > 50,000, experience > 5 years, performance > 80
- Charts saved to `output/charts`: salary histogram, average salary by department, experience vs salary scatter plot
