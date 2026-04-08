import pytest
from pathlib import Path
from src.organizer import DownloadHandler
from src.security import safe_move

def test_safe_move(tmp_path):
    src = tmp_path / "test.txt"
    src.write_text("hello")
    dst = tmp_path / "dest" / "test.txt"
    # Debe mover
    assert safe_move(src, dst, None) == True
    assert not src.exists()
    assert dst.exists()

def test_safe_move_collision(tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("1")
    dst = tmp_path / "a.txt"
    dst.write_text("original")
    assert safe_move(src, dst, None) == True
    # Debe haber creado a_1.txt
    assert (tmp_path / "a_1.txt").exists()

def test_true():
    assert True