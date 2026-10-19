"""Functions for analysing the data and creating charts."""

import os

import matplotlib
matplotlib.use("Agg")  # save charts to files without opening a window
import matplotlib.pyplot as plt
import numpy as np


def calculate_statistics(df):
    """Print overall statistics and the average salary per department."""
    print("\n===== SUMMARY STATISTICS =====")
    print(f"Total valid employees : {len(df)}")
    print(f"Average age           : {np.mean(df['age']):.1f}")
    print(f"Average salary        : {np.mean(df['salary']):,.2f}")
    print(f"Average experience    : {np.mean(df['experience']):.1f} years")
    print(f"Highest salary        : {np.max(df['salary']):,.2f}")
    print(f"Lowest salary         : {np.min(df['salary']):,.2f}")

    dept_avg = df.groupby("department")["salary"].mean().round(2)
    print("\nAverage salary by department:")
    print(dept_avg)
    return dept_avg


def filter_employees(df):
    """Print employees matching the three required conditions."""
    columns = ["employee_id", "name", "department", "salary", "experience", "performance"]

    print("\n===== Salary greater than 50,000 =====")
    print(df[df["salary"] > 50000][columns].to_string(index=False))

    print("\n===== Experience more than 5 years =====")
    print(df[df["experience"] > 5][columns].to_string(index=False))

    print("\n===== Performance score greater than 80 =====")
    print(df[df["performance"] > 80][columns].to_string(index=False))


def create_charts(df, output_dir):
    """Create and save the three charts."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Histogram: salary distribution
    plt.figure(figsize=(8, 5))
    plt.hist(df["salary"], bins=8, color="steelblue", edgecolor="black")
    plt.title("Salary Distribution")
    plt.xlabel("Monthly Salary")
    plt.ylabel("Number of Employees")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "salary_histogram.png"))
    plt.close()

    # 2. Bar chart: average salary by department
    dept_avg = df.groupby("department")["salary"].mean()
    plt.figure(figsize=(8, 5))
    plt.bar(dept_avg.index, dept_avg.values, color="seagreen")
    plt.title("Average Salary by Department")
    plt.xlabel("Department")
    plt.ylabel("Average Monthly Salary")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "avg_salary_by_department.png"))
    plt.close()

    # 3. Scatter plot: experience vs salary
    plt.figure(figsize=(8, 5))
    plt.scatter(df["experience"], df["salary"], color="darkorange")
    plt.title("Experience vs Salary")
    plt.xlabel("Experience (years)")
    plt.ylabel("Monthly Salary")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "experience_vs_salary.png"))
    plt.close()

    print(f"\nCharts saved in: {output_dir}")
