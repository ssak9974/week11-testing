
import pytest
from load_scores import load_scores


def test_normal_scores(tmp_path):
    """정상적인 성적을 읽는다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,90\n지훈,85\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 90), ("지훈", 85)]
    assert skipped == []


def test_header_only(tmp_path):
    """헤더만 있는 파일은 빈 목록을 반환한다."""
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == []


def test_file_not_found():
    """파일이 없으면 FileNotFoundError가 발생한다."""
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_wrong_column_count(tmp_path):
    """열 개수가 2개가 아니면 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,90,추가\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == [(2, "민수,90,추가", "열 개수가 2가 아님")]


def test_empty_score(tmp_path):
    """점수가 비어 있으면 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "점수가 비어 있음"


def test_non_integer_score(tmp_path):
    """점수가 정수가 아니면 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,abc\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "점수가 정수가 아님"


@pytest.mark.parametrize("score", [-1, 101])
def test_score_out_of_range(tmp_path, score):
    """점수가 0~100 범위를 벗어나면 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        f"name,score\n민수,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "점수가 0~100 밖"


def test_empty_name(tmp_path):
    """이름이 비어 있으면 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped[0][2] == "이름이 비어 있음"


@pytest.mark.parametrize("score", [0, 100])
def test_boundary_scores(tmp_path, score):
    """최솟값 0과 최댓값 100은 정상 처리한다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        f"name,score\n민수,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", score)]
    assert skipped == []


def test_duplicate_names(tmp_path):
    """이름이 같아도 두 사람 모두 남긴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n민수,90\n민수,80\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 90), ("민수", 80)]
    assert skipped == []


def test_blank_line(tmp_path):
    """빈 줄은 기록하지 않고 건너뛴다."""
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n\n민수,90\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("민수", 90)]
    assert skipped == []
