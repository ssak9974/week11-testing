
import pytest
from load_scores import load_scores


def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5


def test_빈_줄은_건너뛴다():
    kept, skipped = load_scores("scores.csv")
    assert len(skipped) == 5


def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert ("최,네번", 77) in kept


def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize("점수, 유효한가", [
    (0, True),
    (100, True),
    (101, False),
])
def test_점수_경계값(tmp_path, 점수, 유효한가):
    파일 = tmp_path / "임시.csv"
    파일.write_text(
        f"name,score\n학생,{점수}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(파일)
    assert (len(kept) == 1) == 유효한가
