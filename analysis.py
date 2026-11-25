import pandas as pd


def load_data(path):
    """CSV 파일을 읽어 데이터프레임으로 반환한다."""
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="cp949")


def diagnose(df):
    """원본 데이터의 문제를 확인한다."""
    print("데이터 크기:", df.shape)
    print("\n결측치:")
    print(df.isnull().sum())
    print("\n중복 행:", df.duplicated().sum())
    print("\n반 종류:", df["반"].unique())
    print("\n과목 종류:", df["과목"].unique())
    print("\n점수 최솟값:", df["점수"].min())
    print("점수 최댓값:", df["점수"].max())


def clean_data(df):
    """잘못된 데이터를 정리한다."""
    df = df.dropna(subset=["점수"])
    df = df.drop_duplicates()
    df = df[df["점수"].between(0, 100)]
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    return df


def analyze(df):
    """반별 평균과 과목별 평균을 계산한다."""
    print("\n반별 평균:")
    print(df.groupby("반")["점수"].mean())

    print("\n반별 과목 평균:")
    print(df.groupby(["반", "과목"])["점수"].mean())

    print("\n반별 인원:")
    print(df.groupby("반")["점수"].count())


if __name__ == "__main__":
    data = load_data("scores_2026.csv")

    print("=== 원본 데이터 진단 ===")
    diagnose(data)

    cleaned = clean_data(data)

    print("\n=== 정제 후 데이터 ===")
    print("정제 후 행 개수:", len(cleaned))

    print("\n=== 분석 결과 ===")
    analyze(cleaned)