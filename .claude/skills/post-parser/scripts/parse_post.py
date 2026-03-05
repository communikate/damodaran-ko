#!/usr/bin/env python3
"""
post-parser: Damodaran 블로그 개별 포스팅 HTML 파싱 → 구조화 JSON
댓글 섹션(.comments, #comments)은 파싱 단계에서 제거.
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

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("[post-parser] beautifulsoup4 필요: pip install beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)

MAX_RETRIES = 2
RETRY_DELAY = 3

# 제거할 댓글·공유 섹션 선택자
REMOVE_SELECTORS = [
    ".comments",
    "#comments",
    ".comment-form",
    ".blog-pager",
    ".share-buttons",
    ".post-share-buttons",
    "#comment-editor",
    ".comment-thread",
    ".feed-links",
]


def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DamodaranTranslator/1.0)",
        "Accept-Language": "en-US,en;q=0.9",
    }
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except URLError as e:
            print(f"[post-parser] 시도 {attempt} 실패: {e}", file=sys.stderr)
            if attempt <= MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    raise RuntimeError(f"포스팅 HTML 수집 실패: {url}")


def extract_post_data(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    # 댓글 등 불필요 섹션 제거
    for selector in REMOVE_SELECTORS:
        for el in soup.select(selector):
            el.decompose()

    # 제목
    title = ""
    h3 = soup.find("h3", class_="post-title")
    if h3:
        title = h3.get_text(strip=True)
    if not title:
        og_title = soup.find("meta", property="og:title")
        if og_title:
            title = og_title.get("content", "").strip()
    if not title:
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True).split("|")[0].strip()

    # 발행일
    published = ""
    date_meta = soup.find("meta", property="article:published_time")
    if date_meta:
        published = date_meta.get("content", "")[:10]
    if not published:
        abbr = soup.find("abbr", class_="published")
        if abbr:
            published = abbr.get("title", "")[:10]
    if not published:
        # URL에서 추출 (blogspot.com/YYYY/MM/...)
        m = re.search(r"/(\d{4})/(\d{2})/", url)
        if m:
            published = f"{m.group(1)}-{m.group(2)}-01"

    # 본문 HTML
    content_el = (
        soup.find("div", class_="post-body")
        or soup.find("div", class_="entry-content")
        or soup.find("div", itemprop="articleBody")
    )
    html_content = str(content_el) if content_el else ""

    # 이미지 URL 목록
    images = []
    if content_el:
        for img in content_el.find_all("img"):
            src = img.get("src", "").strip()
            if src and src.startswith("http"):
                images.append(src)

    # 외부 링크 목록
    links = []
    if content_el:
        for a in content_el.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http") and "blogspot.com" not in href:
                links.append({"text": a.get_text(strip=True), "href": href})

    # 단락 수 (검증용)
    plain_paragraphs = len(re.findall(r"<p[\s>]", html_content))

    if len(html_content) < 100:
        raise ValueError(f"본문 내용이 너무 짧음 (len={len(html_content)}): {url}")

    return {
        "title": title,
        "published": published,
        "original_url": url,
        "html_content": html_content,
        "images": images,
        "links": links,
        "paragraph_count": plain_paragraphs,
        "content_length": len(html_content),
        "parsed_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Damodaran 포스팅 HTML 파싱")
    parser.add_argument("--url", required=True, help="포스팅 URL")
    parser.add_argument("--output", required=True, help="출력 JSON 파일 경로")
    args = parser.parse_args()

    print(f"[post-parser] 파싱 시작: {args.url}")

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            html = fetch_html(args.url)
            data = extract_post_data(html, args.url)
            break
        except (ValueError, RuntimeError) as e:
            print(f"[post-parser] 시도 {attempt} 실패: {e}", file=sys.stderr)
            if attempt > MAX_RETRIES:
                print(f"[post-parser] 재시도 초과, 스킵: {args.url}", file=sys.stderr)
                sys.exit(2)
            time.sleep(RETRY_DELAY)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[post-parser] 완료: {args.output}")
    print(f"  - 제목: {data['title']}")
    print(f"  - 발행일: {data['published']}")
    print(f"  - 본문 길이: {data['content_length']}자")
    print(f"  - 단락 수: {data['paragraph_count']}")
    print(f"  - 이미지: {len(data['images'])}개")


if __name__ == "__main__":
    main()
