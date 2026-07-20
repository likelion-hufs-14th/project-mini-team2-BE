# INCINER - Backend

> 24시간 후 자동으로 소각(incinerate)되는 익명 피드 서비스 - BE 저장소

---

## 개요

- 게시글(Feed)은 작성 시각으로부터 24시간이 지나면 만료됩니다.
- 공감/비공감으로 반응을 표현합니다.
- 게시글에는 댓글(Comment)을 남길 수 있습니다.

---

## 기술 스택

- Python 3.13
- Django 4.2.8
- MySQL

---

## 프로젝트 구조

```
inciner/
├── inciner/          # 프로젝트 설정 (settings, urls, wsgi/asgi)
└── feed/             # 피드 앱 (models, views, admin, tests)
```

---

## 현재 진행 상황

- [x] Django 프로젝트 및 `feed` 앱 초기 설정
- [x] `Feeds` 모델: 닉네임, 내용, 생성/만료 시각(24시간 후 자동 만료), fan/wood 카운트
- [x] `Comments` 모델: 댓글 내용, 생성 시각
- [x] `nickname` 정책 수정 논의 필요 - 프론트에서 `localStorage` 활용할 예정
- [ ] Feed API 구현
- [ ] Comments API 구현
- [ ] Reaction API 구현
- [x] 피드 업로드 사용자 Count 로직

---

## 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/likelion-hufs-14th/project-mini-team2-BE.git
cd project-mini-team2-BE/inciner
```

### 2. 가상환경 설정 및 패키지 설치

```bash
python -m venv .venv
# Windows
source .venv/Scripts/activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. 환경 변수 설정

프로젝트 루트(`inciner/`)에 `.env` 파일을 생성하고 아래 값을 채워주세요.

```
SECRET_KEY=your-django-secret-key
```

### 4. DB 마이그레이션

```bash
python manage.py makemigration
python manage.py migrate
```

### 5. 개발 서버 실행

```bash
python manage.py runserver
```

---

## 협업 규칙

### 새 기능 추가 과정

`feat/function-name`으로 기능 단위 브랜치 파서 커밋
-> 리뷰 반영하여 같은 브랜치에 커밋
-> 최종 승인 받으면 PR로 main에 머지

### 커밋 메시지 컨벤션

| type       | 설명                                              |
| ---------- | ------------------------------------------------- |
| `feat`     | 새로운 기능 추가                                  |
| `fix`      | 버그 수정                                         |
| `docs`     | 문서 수정 (README 등)                             |
| `style`    | 코드 포맷팅, 세미콜론 누락 등 기능 변화 없는 수정 |
| `refactor` | 기능 변화 없는 코드 리팩토링                      |
| `test`     | 테스트 코드 추가/수정                             |
| `chore`    | 빌드, 패키지, 설정 등 기타 변경                   |

EX) `feat: Comments 모델에 nickname 필드 추가`

### 마이그레이션 파일 충돌 정책

- 모델을 수정했다면 `makemigrations`로 생성된 마이그레이션 파일을 반드시 같이 커밋
- PR을 올리기 전 `main`을 최신 상태로 pull 받아 마이그레이션 파일 번호 충돌 여부 확인하기
- 번호가 충돌하면 `rm <filename>`으로 자신의 마이그레이션 파일을 삭제 후 `makemigrations`로 재생성하거나 `makemigrations --merge`로 병합
- `migrations/` 폴더의 파일은 직접 수동으로 수정하지 않기

### PR 템플릿

```markdown
# 작업 개요

- 어떤 작업을 했는지 한 줄 제목으로 요약

## 변경 사항

- 변경한 내용을 목록으로 작성

## 리뷰 시 참고사항 (선택)

- 리뷰어가 특히 봐줬으면 하는 부분
```
