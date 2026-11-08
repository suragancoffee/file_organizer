# file-organizer

지저분한 폴더(다운로드, 바탕화면 등)를 **확장자별 / 월별**로 자동 정리하는 파이썬 CLI 도구입니다.
외부 라이브러리 없이 Python 표준 라이브러리만 사용합니다.

## 특징

- **안전한 기본값**: 기본은 미리보기이고, `--apply`를 붙여야 실제로 파일을 옮깁니다.
- **되돌리기**: `--undo`로 마지막 정리를 원래 위치로 복구합니다.
- **덮어쓰기 방지**: 같은 이름이 있으면 `name (1).ext`로 자동 회피합니다.
- **시스템 파일 보호**: 바로가기(`.lnk`), `desktop.ini`, 임시 파일(`~$`, `.tmp`), 숨김 파일, 하위 폴더는 건드리지 않습니다.
- **두 가지 분류 방식**: 확장자별(기본) 또는 수정 월별(`2026-11`).

## 요구 사항

- Python 3.8 이상

## 사용법

```bash
python organize.py <폴더>                       # 미리보기 (파일은 옮기지 않음)
python organize.py <폴더> --apply               # 확장자별로 실제 정리
python organize.py <폴더> --by date --apply     # 수정 월별로 정리
python organize.py <폴더> --undo                # 마지막 정리 되돌리기
```

Windows 예시:

```powershell
python organize.py C:\Users\<이름>\Downloads
python organize.py C:\Users\<이름>\Downloads --apply
```

> 처음에는 꼭 미리보기로 목록을 확인한 뒤 `--apply`를 붙이세요.

## 실행 화면

### 1. 미리보기

이동 대상이 `원래 이름 -> 분류 폴더\이름` 형태로 출력됩니다. 이 단계에서는 파일이 옮겨지지 않습니다.

<img width="881" height="558" alt="image" src="https://github.com/user-attachments/assets/f5d9a335-3158-4bb9-82ea-4307e3c5e2d0" />


### 2. 정리와 되돌리기

`--apply`로 9개 파일을 이동하고, `--undo`로 원래 위치에 복구한 모습입니다.

<img width="770" height="546" alt="image" src="https://github.com/user-attachments/assets/d799dbbc-7f82-4206-a8e4-187a5ed22e89" />


## 분류 규칙

| 폴더 | 확장자 예시 |
|------|-------------|
| Images | jpg, png, gif, webp, svg, heic |
| Documents | pdf, docx, txt, md, hwp, hwpx |
| Spreadsheets | xls, xlsx, csv |
| Presentations | ppt, pptx, key |
| Videos | mp4, mkv, mov, avi |
| Audio | mp3, wav, flac, m4a |
| Archives | zip, rar, 7z, tar, gz |
| Code | py, js, ts, html, css, json |
| Installers | exe, msi, dmg, pkg, apk |
| Others | 위에 없는 나머지 |

`organize.py` 상단의 `CATEGORIES` 딕셔너리를 수정하면 카테고리와 확장자를 바꿀 수 있습니다.
정리에서 제외할 확장자는 `SKIP_EXT`에서 관리합니다.

## 동작 방식

1. 대상 폴더 바로 아래의 파일만 검사합니다. 하위 폴더 안은 보지 않습니다.
2. 제외 대상(숨김, 시스템, 임시, 바로가기 파일)을 걸러냅니다.
3. 분류 기준에 따라 이동 목적지를 정하고, 이름이 겹치면 번호를 붙입니다.
4. `--apply`일 때만 이동하고, 이동 기록을 대상 폴더의 `.organize_log.json`에 저장합니다.
5. `--undo`는 이 기록을 거꾸로 읽어 복구하고, 비어 있는 분류 폴더를 삭제합니다.

## 주의

- `--undo`는 **가장 최근 정리 1회분**만 복구합니다. 다른 폴더를 정리하기 전에 사용하세요.
- 정리 후 파일을 직접 옮기거나 이름을 바꿨다면 해당 파일은 복구되지 않습니다.

## License

MIT
