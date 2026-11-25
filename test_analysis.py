import pandas as pd
from analysis import clean_data


def test_cleaned_data_has_100_rows():
    df = pd.read_csv("scores_2026.csv")
    cleaned = clean_data(df)
    assert len(cleaned) == 100


def test_class_names_are_stripped():
    df = pd.read_csv("scores_2026.csv")
    cleaned = clean_data(df)
    assert set(cleaned["반"].unique()) == {"1반", "2반"}


def test_grouped_sum_matches_total():
    df = pd.read_csv("scores_2026.csv")
    cleaned = clean_data(df)

    grouped_sum = cleaned.groupby("반")["점수"].sum().sum()
    total_sum = cleaned["점수"].sum()

    assert grouped_sum == total_sum


def test_mini_class_1_average_is_80():
    df = pd.read_csv("mini.csv")
    cleaned = clean_data(df)

    class_1_average = cleaned[cleaned["반"].str.strip() == "1반"]["점수"].mean()

    assert class_1_average == 80.0