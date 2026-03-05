#!/usr/bin/env python3
"""
state-manager: 번역 상태 파일(translated_posts.json) 읽기/쓰기 및 필터링
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE_DEFAULT = "state/translated_posts.json"


def load_state(state_file: str) -> dict:
    p = Path(state_file)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[state-manager] 상태 파일 파싱 오류: {e}", file=sys.stderr)
    return {"last_checked": None, "posts": []}


def save_state(state: dict, state_file: str) -> None:
    p = Path(state_file)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_update(args) -> None:
    """번역 완료된 포스팅 1건을 상태 파일에 추가."""
    state = load_state(args.state_file)
    posts = state.get("posts", [])

    # 중복 체크
    existing_ids = {p["post_id"] for p in posts}
    if args.post_id in existing_ids:
        print(f"[state-manager] 이미 등록됨: {args.post_id}")
        return

    entry = {
        "post_id":      args.post_id,
        "slug":         args.slug,
        "original_url": args.original_url,
        "published":    args.published,
        "translated_at": datetime.now(timezone.utc).date().isoformat(),
        "status":       "done",
    }
    posts.append(entry)
    state["posts"] = posts
    save_state(state, args.state_file)
    print(f"[state-manager] 상태 업데이트 완료: {args.slug}")


def cmd_check(args) -> None:
    """post_id가 이미 번역됐는지 확인. exit code 0=번역됨, 1=미번역."""
    state = load_state(args.state_file)
    done_ids = {p["post_id"] for p in state.get("posts", [])}
    if args.post_id in done_ids:
        print("translated")
        sys.exit(0)
    else:
        print("untranslated")
        sys.exit(1)


def cmd_list_untranslated(args) -> None:
    """posts_list.json 기준으로 미번역 목록 출력."""
    posts_list_file = args.posts_list
    if not Path(posts_list_file).exists():
        print(f"[state-manager] posts_list 파일 없음: {posts_list_file}", file=sys.stderr)
        sys.exit(1)

    posts_data = json.loads(Path(posts_list_file).read_text(encoding="utf-8"))
    all_posts = posts_data.get("untranslated", [])

    state = load_state(args.state_file)
    done_ids = {p["post_id"] for p in state.get("posts", [])}

    untranslated = [p for p in all_posts if p["post_id"] not in done_ids]

    result = {
        "count": len(untranslated),
        "posts": untranslated,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_stats(args) -> None:
    """번역 통계 출력."""
    state = load_state(args.state_file)
    posts = state.get("posts", [])
    done = [p for p in posts if p.get("status") == "done"]
    print(json.dumps({
        "total_translated": len(done),
        "last_checked": state.get("last_checked"),
        "latest": done[-1] if done else None,
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="번역 상태 관리")
    parser.add_argument("--state-file", default=STATE_FILE_DEFAULT)
    sub = parser.add_subparsers(dest="action", required=True)

    # update
    p_update = sub.add_parser("update", help="번역 완료 포스팅 등록")
    p_update.add_argument("--post-id",      required=True)
    p_update.add_argument("--slug",         required=True)
    p_update.add_argument("--original-url", required=True)
    p_update.add_argument("--published",    required=True, help="YYYY-MM-DD")
    p_update.set_defaults(func=cmd_update)

    # check
    p_check = sub.add_parser("check", help="번역 여부 확인")
    p_check.add_argument("--post-id", required=True)
    p_check.set_defaults(func=cmd_check)

    # list-untranslated
    p_list = sub.add_parser("list-untranslated", help="미번역 목록 출력")
    p_list.add_argument("--posts-list", required=True, help="output/posts_list.json 경로")
    p_list.set_defaults(func=cmd_list_untranslated)

    # stats
    p_stats = sub.add_parser("stats", help="번역 통계")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
