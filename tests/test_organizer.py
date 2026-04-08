import pytest
from pathlib import Path
from unittest.mock import Mock
from src.organizer import DownloadHandler
from src.security import safe_move

def test_safe_move(tmp_path):
    src = tmp_path / "test.txt"
    src.write_text("hello")
    dst = tmp_path / "dest" / "test.txt"
    logger = Mock()  # <-- logger falso que acepta cualquier llamada
    assert safe_move(src, dst, logger) == True
    assert not src.exists()
    assert dst.exists()

def test_safe_move_collision(tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("1")
    dst = tmp_path / "a.txt"
    dst.write_text("original")
    logger = Mock()
    assert safe_move(src, dst, logger) == True
    assert (tmp_path / "a_1.txt").exists()

def test_true():
    assert True