#!/usr/bin/env bash
# git-publisher: 번역 완료 파일을 git add/commit/push
# 사용법: bash publish.sh "커밋 메시지"

set -euo pipefail

COMMIT_MSG="${1:-번역 업데이트: $(date +'%Y-%m-%d')}"
MAX_RETRIES=2

log() { echo "[git-publisher] $*"; }
error() { echo "[git-publisher] ERROR: $*" >&2; }

# 저장소 루트에서 실행되어야 함
if [ ! -d ".git" ]; then
  error ".git 디렉터리가 없습니다. 프로젝트 루트에서 실행하세요."
  exit 1
fi

# 스테이징할 파일이 있는지 확인
CHANGED=$(git status --porcelain blog/_posts/ state/translated_posts.json state/skipped_posts.log 2>/dev/null || true)

if [ -z "$CHANGED" ]; then
  log "커밋할 변경사항이 없습니다."
  exit 0
fi

log "변경 파일:"
echo "$CHANGED"

# git add
git add blog/_posts/ state/translated_posts.json state/skipped_posts.log
log "git add 완료"

# git commit
git commit -m "$COMMIT_MSG"
log "git commit 완료: $COMMIT_MSG"

# git push (재시도 포함)
for attempt in $(seq 1 $((MAX_RETRIES + 1))); do
  if git push; then
    log "git push 성공"
    exit 0
  fi
  if [ "$attempt" -le "$MAX_RETRIES" ]; then
    log "push 실패, ${attempt}회 재시도..."
    sleep 5
    git pull --rebase
  fi
done

error "git push 실패 (${MAX_RETRIES}회 재시도 초과)"
exit 1
