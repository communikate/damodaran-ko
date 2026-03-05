#!/usr/bin/env python3
"""
jekyll-post-generator: 번역 JSON → Jekyll Markdown 포스팅 파일 생성
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[jekyll-post-generator] beautifulsoup4 필요: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


FRONT_MATTER_TEMPLATE = """\
---
layout: post
title: {title}
date: {date}
original_title: {original_title}
original_url: "{original_url}"
original_author: "Aswath Damodaran"
categories: [translation, finance]
comments: false
---
"""


def html_to_markdown(html: str) -> str:
    """HTML 본문 → Markdown. 이미지·링크는 원본 URL 그대로 유지."""
    soup = BeautifulSoup(html, "lxml")

    lines = []
    _process_node(soup.find("div") or soup, lines)
    text = "\n".join(lines)

    # 연속 빈 줄 3개 이상 → 2개로 압축
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _process_node(node, lines: list) -> None:
    from bs4 import NavigableString, Tag

    if isinstance(node, NavigableString):
        text = str(node)
        if text.strip():
            lines.append(text.rstrip())
        return

    tag = node.name.lower() if node.name else ""

    if tag in ("script", "style", "noscript"):
        return

    if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        level = int(tag[1])
        text = node.get_text(strip=True)
        if text:
            lines.append("")
            lines.append("#" * level + " " + text)
            lines.append("")

    elif tag == "p":
        parts = []
        for child in node.children:
            parts.append(_inline(child))
        text = "".join(parts).strip()
        if text:
            lines.append("")
            lines.append(text)
            lines.append("")

    elif tag == "blockquote":
        inner_lines = []
        _process_node_children(node, inner_lines)
        for line in inner_lines:
            lines.append("> " + line if line.strip() else ">")

    elif tag in ("ul", "ol"):
        for i, li in enumerate(node.find_all("li", recursive=False), 1):
            prefix = f"{i}. " if tag == "ol" else "- "
            text = li.get_text(separator=" ", strip=True)
            lines.append(prefix + text)
        lines.append("")

    elif tag == "img":
        src = node.get("src", "")
        alt = node.get("alt", "이미지")
        if src:
            lines.append("")
            lines.append(f"![{alt}]({src})")
            lines.append("")

    elif tag == "a":
        href = node.get("href", "")
        text = node.get_text(strip=True)
        if href and text:
            lines.append(f"[{text}]({href})")
        elif text:
            lines.append(text)
        else:
            # 텍스트 없음 — 자식 요소 처리 (예: <a><img/></a>)
            _process_node_children(node, lines)

    elif tag in ("table",):
        lines.append("")
        lines.append(_table_to_markdown(node))
        lines.append("")

    elif tag in ("br",):
        lines.append("  ")  # Markdown 줄바꿈

    elif tag in ("hr",):
        lines.append("\n---\n")

    elif tag in ("strong", "b"):
        text = node.get_text(strip=True)
        if text:
            lines.append(f"**{text}**")

    elif tag in ("em", "i"):
        text = node.get_text(strip=True)
        if text:
            lines.append(f"*{text}*")

    elif tag == "div":
        _process_node_children(node, lines)

    else:
        _process_node_children(node, lines)


def _process_node_children(node, lines: list) -> None:
    for child in node.children:
        _process_node(child, lines)


def _inline(node) -> str:
    from bs4 import NavigableString, Tag
    if isinstance(node, NavigableString):
        return str(node)
    tag = node.name.lower() if node.name else ""
    if tag == "img":
        src = node.get("src", "")
        alt = node.get("alt", "이미지")
        return f"![{alt}]({src})" if src else ""
    if tag == "a":
        href = node.get("href", "")
        text = node.get_text()
        return f"[{text}]({href})" if href else text
    if tag in ("strong", "b"):
        return f"**{node.get_text()}**"
    if tag in ("em", "i"):
        return f"*{node.get_text()}*"
    if tag == "br":
        return "  \n"
    return node.get_text()


def _table_to_markdown(table_node) -> str:
    rows = []
    for tr in table_node.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
        rows.append("| " + " | ".join(cells) + " |")
    if not rows:
        return ""
    # 헤더 구분선
    first_row_cells = table_node.find("tr")
    if first_row_cells:
        col_count = len(first_row_cells.find_all(["th", "td"]))
        separator = "| " + " | ".join(["---"] * col_count) + " |"
        rows.insert(1, separator)
    return "\n".join(rows)


def yaml_quote(value: str) -> str:
    """YAML 문자열 안전 처리: 특수문자 포함 시 따옴표."""
    if any(c in value for c in (':', '"', "'", '\n', '#', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`')):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return f'"{value}"'


def generate_markdown(data: dict) -> str:
    """번역 JSON → Jekyll Markdown 문자열."""
    translated_title = data.get("translated_title", data.get("title", ""))
    original_title   = data.get("original_title", data.get("title", ""))
    original_url     = data.get("original_url", "")
    published        = data.get("published", "")[:10]
    translated_content = data.get("translated_content", "")

    # HTML이면 Markdown으로 변환, 이미 Markdown이면 그대로
    if translated_content.strip().startswith("<"):
        body = html_to_markdown(translated_content)
    else:
        body = translated_content

    front_matter = FRONT_MATTER_TEMPLATE.format(
        title=yaml_quote(translated_title),
        date=published,
        original_title=yaml_quote(original_title),
        original_url=original_url,
    )

    attribution = (
        "\n\n---\n\n"
        f"*이 글은 Aswath Damodaran 교수의 원문을 번역·아카이빙한 것입니다.*  \n"
        f"*원문: [{original_title}]({original_url})*"
    )

    return front_matter + "\n" + body + attribution


def make_output_path(data: dict, output_dir: str) -> str:
    """blog/_posts/YYYY-MM-DD-slug.md 경로 생성."""
    published = data.get("published", "")[:10]
    slug = data.get("slug", "")
    if not slug:
        # slug가 없으면 제목에서 생성
        title = data.get("translated_title", "post")
        slug = re.sub(r"[^\w\s-]", "", title.lower())
        slug = re.sub(r"[\s_]+", "-", slug)[:60]
    filename = f"{published}-{slug}.md"
    return str(Path(output_dir) / filename)


def validate_front_matter(content: str) -> bool:
    """필수 front matter 필드 확인."""
    required = ["title:", "date:", "original_url:"]
    for field in required:
        if field not in content:
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description="번역 JSON → Jekyll Markdown 생성")
    parser.add_argument("--input",      required=True, help="translated_YYYYMMDD_slug.json 경로")
    parser.add_argument("--output",     default=None,  help="출력 .md 경로 (미지정 시 blog/_posts/ 자동 결정)")
    parser.add_argument("--posts-dir",  default="blog/_posts", help="_posts 디렉터리 경로")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[jekyll-post-generator] 입력 파일 없음: {args.input}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(input_path.read_text(encoding="utf-8"))

    markdown = generate_markdown(data)

    if not validate_front_matter(markdown):
        print("[jekyll-post-generator] front matter 검증 실패", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or make_output_path(data, args.posts_dir)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(markdown, encoding="utf-8")

    print(f"[jekyll-post-generator] 생성 완료: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
