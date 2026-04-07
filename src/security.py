import os
import shutil  # <--- IMPORTANTE: importa shutil
import re
from pathlib import Path

def sanitize_path(base_path: str, user_input_path: str) -> Path:
    """Evita directory traversal (../)"""
    base = Path(base_path).resolve()
    candidate = (base / user_input_path).resolve()
    if not str(candidate).startswith(str(base)):
        raise ValueError("Path traversal detected")
    return candidate

def safe_move(src: Path, dst: Path, logger):
    """Mueve archivo verificando permisos y colisiones"""
    if not src.exists():
        logger.error(f"Source missing: {src}")
        return False
    if not os.access(src.parent, os.R_OK | os.W_OK):
        logger.error(f"No permissions to read/write {src.parent}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Evita sobreescribir: añade sufijo
    if dst.exists():
        counter = 1
        new_dst = dst.with_stem(f"{dst.stem}_{counter}")
        while new_dst.exists():
            counter += 1
            new_dst = dst.with_stem(f"{dst.stem}_{counter}")
        dst = new_dst
    # Aquí está la corrección: usa shutil.move, no src.shutil.move
    shutil.move(str(src), str(dst))
    logger.info(f"Moved {src} -> {dst}")
    return True