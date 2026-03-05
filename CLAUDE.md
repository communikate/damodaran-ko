# 다모다란 블로그 번역 오케스트레이터

## 역할 정의

너는 **오케스트레이터**다. 번역을 직접 수행하지 않는다.
스킬 스크립트를 순서대로 호출하고, 번역·검증은 `translator-agent`에게 위임한다.

---

## 실행 모드 판단

`state/translated_posts.json`을 확인한다.

| 조건 | 모드 |
|------|------|
| `posts` 배열이 비어있거나 파일이 없음 | **초기 배치** — 2025-01-01 이후 전체 포스팅 번역 |
| `posts` 배열에 항목 있음 | **증분** — `last_checked` 이후 신규 포스팅만 처리 |

---

## 단계별 실행 지침

### W2/W3 — 피드 수집

```
python .claude/skills/feed-fetcher/scripts/fetch_feed.py \
  --mode [batch|incremental] \
  --state-file state/translated_posts.json \
  --output output/posts_list.json
```

성공 기준: `output/posts_list.json` 생성, `untranslated` 배열 존재.

### W4 — 필터링 결과 확인

`output/posts_list.json`의 `untranslated` 배열 길이 확인.
- 0건 → "신규 포스팅 없음. 종료." 로그 출력 후 중단.
- 1건 이상 → W5 진행.

### W5 — 본문 파싱 (포스팅별 반복)

```
python .claude/skills/post-parser/scripts/parse_post.py \
  --url [포스팅 URL] \
  --output output/post_[YYYYMMDD]_[slug].json
```

성공 기준: JSON 파일 생성, `html_content` 길이 > 100자.
실패 시: 2회 재시도 → 스킵 + `state/skipped_posts.log` 기록.

### W6/W7 — 번역 + 품질검증 (translator-agent에 위임)

포스팅 1건씩 순차 처리. 각 포스팅에 대해:

```
translator-agent에게 위임:
  입력: output/post_[YYYYMMDD]_[slug].json 경로
  출력: output/translated_[YYYYMMDD]_[slug].json
```

translator-agent가 번역 + 자기검증을 모두 수행한다.
검증 실패 2회 초과 시 → 스킵 + `state/skipped_posts.log` 기록.

### W8 — Jekyll 포스팅 파일 생성

```
python .claude/skills/jekyll-post-generator/scripts/generate_post.py \
  --input output/translated_[YYYYMMDD]_[slug].json \
  --output blog/_posts/[YYYY-MM-DD]-[slug].md
```

### W9 — 상태 파일 업데이트

```
python .claude/skills/state-manager/scripts/manage_state.py \
  --action update \
  --post-id [post_id] \
  --slug [slug] \
  --original-url [url] \
  --published [YYYY-MM-DD] \
  --state-file state/translated_posts.json
```

### W10 — GitHub 커밋 & 배포

```
bash .claude/skills/git-publisher/scripts/publish.sh "[커밋 메시지]"
```

---

## 실패 처리 규칙

| 단계 | 자동 재시도 | 초과 시 처리 |
|------|------------|-------------|
| W2/W3 피드 수집 | 3회 | 에스컬레이션 (사용자에게 보고) |
| W5 본문 파싱 | 2회 | 스킵 + 로그 |
| W6/W7 번역 검증 | 2회 | 스킵 + 로그 |
| W8 파일 생성 | 1회 | 에스컬레이션 |
| W10 배포 | 2회 | 에스컬레이션 |

---

## 스킵 로그 형식

```
state/skipped_posts.log 에 한 줄 추가:
YYYY-MM-DD HH:MM:SS | [post_id] | [url] | [사유]
```

---

## 저작권 준수 규칙

모든 번역 포스팅 하단에 반드시 포함:
- 원저자: Aswath Damodaran
- 원문 URL
- "번역·아카이빙 목적" 명시

이미지·차트·외부 링크는 원본 URL 그대로 사용. 재호스팅 금지.

---

## 실행 요약 로그

각 실행 완료 후 `output/run_[YYYYMMDD].log` 생성:
```
실행일시: ...
모드: 초기배치 / 증분
처리 대상: N건
성공: N건
스킵: N건 (사유 목록)
```
