#!/usr/bin/env python3
"""
feed-fetcher: Damodaran 블로그 Atom 피드 수집 및 포스팅 목록 파싱
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
import xml.etree.ElementTree as ET

FEED_URL = "https://aswathdamodaran.blogspot.com/feeds/posts/default"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "gd":   "http://schemas.google.com/g/2005",
}
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def fetch_feed_xml(url: str, max_results: int = 500) -> str:
    """Atom 피드 XML 다운로드. 페이지네이션 처리."""
    full_url = f"{url}?max-results={max_results}&orderby=published"
    headers = {"User-Agent": "DamodaranTranslator/1.0"}
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = Request(full_url, headers=headers)
            with urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8")
        except URLError as e:
            print(f"[feed-fetcher] 시도 {attempt}/{MAX_RETRIES} 실패: {e}", file=sys.stderr)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    raise RuntimeError(f"피드 수집 실패 (3회 재시도 초과): {url}")


def parse_entries(xml_text: str) -> list[dict]:
    """Atom XML → 포스팅 메타데이터 리스트."""
    root = ET.fromstring(xml_text)
    entries = []
    for entry in root.findall("atom:entry", NS):
        # post_id: tag:blogger.com,1999:blog-XXXXXX.post-YYYYYY
        raw_id = entry.findtext("atom:id", "", NS)
        post_id = raw_id.split(".")[-1] if "." in raw_id else raw_id

        title = entry.findtext("atom:title", "", NS).strip()
        published = entry.findtext("atom:published", "", NS)[:10]  # YYYY-MM-DD

        # 원본 URL (rel="alternate")
        url = ""
        for link in entry.findall("atom:link", NS):
            if link.get("rel") == "alternate":
                url = link.get("href", "")
                break

        if not url or not post_id:
            continue

        # slug: URL의 마지막 경로 세그먼트 (blogspot 형식: YYYY/MM/title-slug.html)
        slug = _url_to_slug(url, published)

        entries.append({
            "post_id": post_id,
            "title":   title,
            "published": published,
            "url":     url,
            "slug":    slug,
        })
    return entries


def _url_to_slug(url: str, published: str) -> str:
    """https://aswathdamodaran.blogspot.com/2025/01/title-slug.html → 2025-01-title-slug"""
    match = re.search(r"/(\d{4})/(\d{2})/(.+?)(?:\.html)?$", url)
    if match:
        year, month, title_part = match.groups()
        return f"{year}-{month}-{title_part}"
    # 폴백: published date + post_id 일부
    return f"{published}-post"


def load_state(state_file: str) -> dict:
    p = Path(state_file)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"last_checked": None, "posts": []}


def filter_untranslated(all_posts: list[dict], state: dict, since_date: str | None) -> list[dict]:
    """상태 파일과 대조하여 미번역 포스팅 반환."""
    done_ids = {p["post_id"] for p in state.get("posts", [])}
    result = []
    for post in all_posts:
        if post["post_id"] in done_ids:
            continue
        if since_date and post["published"] < since_date:
            continue
        result.append(post)
    # 오래된 것부터 번역 (오름차순)
    return sorted(result, key=lambda x: x["published"])


def main():
    parser = argparse.ArgumentParser(description="Damodaran 블로그 피드 수집")
    parser.add_argument("--mode", choices=["batch", "incremental"], required=True)
    parser.add_argument("--state-file", default="state/translated_posts.json")
    parser.add_argument("--output", default="output/posts_list.json")
    parser.add_argument("--since", default=None, help="YYYY-MM-DD 이후 포스팅만 (batch 기본값: 2025-01-01)")
    args = parser.parse_args()

    # 출력 디렉터리 생성
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    state = load_state(args.state_file)

    # 날짜 필터 결정
    if args.mode == "batch":
        since_date = args.since or "2025-01-01"
    else:
        # 증분: 마지막 체크 날짜 이후
        since_date = state.get("last_checked", "2025-01-01")
        if since_date:
            since_date = since_date[:10]  # YYYY-MM-DD

    print(f"[feed-fetcher] 피드 수집 시작 (mode={args.mode}, since={since_date})")
    xml_text = fetch_feed_xml(FEED_URL)
    all_posts = parse_entries(xml_text)
    print(f"[feed-fetcher] 전체 파싱된 포스팅: {len(all_posts)}건")

    untranslated = filter_untranslated(all_posts, state, since_date)
    print(f"[feed-fetcher] 번역 대상: {len(untranslated)}건")

    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "since_date": since_date,
        "total_fetched": len(all_posts),
        "untranslated": untranslated,
    }

    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[feed-fetcher] 결과 저장: {args.output}")

    # 상태 파일의 last_checked 갱신
    state["last_checked"] = datetime.now(timezone.utc).isoformat()
    Path(args.state_file).parent.mkdir(parents=True, exist_ok=True)
    Path(args.state_file).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
