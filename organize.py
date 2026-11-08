#!/usr/bin/env python3
"""file-organizer: 폴더 안의 파일을 확장자(또는 날짜)별로 자동 분류합니다.

사용 예:
    python organize.py ~/Downloads              # 미리보기 (실제로 옮기지 않음)
    python organize.py ~/Downloads --apply      # 실제 이동
    python organize.py ~/Downloads --by date --apply
    python organize.py ~/Downloads --undo       # 마지막 정리 되돌리기
"""
import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

LOG_NAME = ".organize_log.json"

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".hwp", ".hwpx", ".rtf", ".odt"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".tsv"},
    "Presentations": {".ppt", ".pptx", ".key"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".m4a", ".aac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".java", ".c", ".cpp", ".go", ".rs", ".sh"},
    "Installers": {".exe", ".msi", ".dmg", ".pkg", ".deb", ".apk"},
}


def category_of(path: Path) -> str:
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "Others"


def target_folder(path: Path, mode: str) -> str:
    if mode == "date":
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m")
    return category_of(path)


def unique_path(dest: Path) -> Path:
    """같은 이름이 있으면 name (1).ext 형태로 피합니다."""
    if not dest.exists():
        return dest
    i = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({i}){dest.suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def organize(root: Path, mode: str, apply: bool) -> None:
    moves = []
    for item in sorted(root.iterdir()):
        SKIP_EXT = {".lnk", ".ini", ".tmp"}
        if not item.is_file():
            continue
        if item.name.startswith((".", "~$")) or item.suffix.lower() in SKIP_EXT:
            continue
        if item.name == Path(__file__).name:
            continue
        dest = unique_path(root / target_folder(item, mode) / item.name)
        moves.append((item, dest))

    if not moves:
        print("정리할 파일이 없습니다.")
        return

    for src, dest in moves:
        print(f"{src.name}  ->  {dest.relative_to(root)}")

    if not apply:
        print(f"\n[미리보기] {len(moves)}개 파일. 실제로 옮기려면 --apply 를 붙이세요.")
        return

    done = []
    for src, dest in moves:
        dest.parent.mkdir(exist_ok=True)
        shutil.move(str(src), str(dest))
        done.append({"from": str(src), "to": str(dest)})
    (root / LOG_NAME).write_text(json.dumps(done, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n완료: {len(done)}개 파일 이동. (되돌리기: --undo)")


def undo(root: Path) -> None:
    log = root / LOG_NAME
    if not log.exists():
        sys.exit("되돌릴 기록이 없습니다.")
    entries = json.loads(log.read_text(encoding="utf-8"))
    restored = 0
    for e in reversed(entries):
        src, dest = Path(e["from"]), Path(e["to"])
        if dest.exists() and not src.exists():
            shutil.move(str(dest), str(src))
            restored += 1
    for d in {Path(e["to"]).parent for e in entries}:  # 비어 있으면 폴더 삭제
        if d.exists() and not any(d.iterdir()):
            d.rmdir()
    log.unlink()
    print(f"{restored}개 파일을 원래 위치로 되돌렸습니다.")


def main() -> None:
    p = argparse.ArgumentParser(description="폴더 파일 자동 정리")
    p.add_argument("folder", type=Path, help="정리할 폴더")
    p.add_argument("--by", choices=["type", "date"], default="type", help="분류 기준 (기본: type)")
    p.add_argument("--apply", action="store_true", help="실제로 이동 (없으면 미리보기)")
    p.add_argument("--undo", action="store_true", help="마지막 정리 되돌리기")
    args = p.parse_args()

    root = args.folder.expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"폴더를 찾을 수 없습니다: {root}")

    undo(root) if args.undo else organize(root, args.by, args.apply)


if __name__ == "__main__":
    main()