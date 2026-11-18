
import pytest
from load_scores import load_scores


def test_normal(tmp_path):
    """정상적인 성적 데이터를 읽는다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "민수,85\n"
        "지훈,95\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 85), ("지훈", 95)]
    assert skipped == []


def test_header_only(tmp_path):
    """헤더만 있는 파일을 처리한다."""
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == []


def test_wrong_column_count(tmp_path):
    """열 개수가 2개가 아닌 줄을 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "민수,85,추가\n"
        "지훈\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 2


def test_empty_score(tmp_path):
    """점수가 비어 있는 줄을 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "민수,\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


def test_non_integer_score(tmp_path):
    """정수가 아닌 점수를 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "민수,abc\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


@pytest.mark.parametrize("score", [-1, 101])
def test_score_out_of_range(tmp_path, score):
    """0~100 범위를 벗어난 점수를 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        f"name,score\n민수,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


def test_boundary_scores(tmp_path):
    """점수의 최솟값과 최댓값을 허용한다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "민수,0\n"
        "지훈,100\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 0), ("지훈", 100)]
    assert skipped == []


def test_empty_name(tmp_path):
    """이름이 비어 있는 줄을 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        ",85\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


def test_blank_line(tmp_path):
    """빈 줄은 기록하지 않고 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "\n"
        "민수,85\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 85)]
    assert skipped == []


def test_duplicate_names(tmp_path):
    """같은 이름이 여러 번 나와도 모두 남긴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "민수,85\n"
        "민수,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 85), ("민수", 90)]
    assert skipped == []


def test_file_not_found():
    """파일이 없으면 FileNotFoundError를 발생시킨다."""
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")
