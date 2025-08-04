import pandas as pd
import re
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from scipy.stats import linregress

def parse_money(value: str) -> float:
    """Convert a money string like '$2,923,706,026' to a float."""
    return float(re.sub(r"[^\d.]", "", value))

def basic_analysis(df: pd.DataFrame) -> list:
    # Clean up columns
    df["Worldwide gross"] = df["Worldwide gross"].apply(parse_money)
    df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
    df["Peak"] = pd.to_numeric(df["Peak"], errors='coerce')

    # Q1: How many $2B+ movies before 2000?
    q1 = df[(df["Worldwide gross"] >= 2e9) & (df["Year"] < 2000)].shape[0]

    # Q2: Which is the earliest film that grossed over $1.5B?
    q2_df = df[df["Worldwide gross"] > 1.5e9].sort_values("Year")
    q2 = q2_df.iloc[0]["Title"] if not q2_df.empty else "Not found"

    # Q3: Correlation between Rank and Peak
    q3 = df["Rank"].corr(df["Peak"])

    # Q4: Scatterplot with regression line
    img_str = scatterplot_with_regression(df)

    return [q1, q2, round(q3, 6), img_str]

def scatterplot_with_regression(df: pd.DataFrame) -> str:
    plt.figure(figsize=(6, 4))
    x = df["Rank"]
    y = df["Peak"]
    plt.scatter(x, y, color="blue")

    # Regression line
    slope, intercept, *_ = linregress(x, y)
    plt.plot(x, slope * x + intercept, "r--")  # dotted red line

    plt.xlabel("Rank")
    plt.ylabel("Peak")
    plt.title("Rank vs Peak")

    # Save as base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"