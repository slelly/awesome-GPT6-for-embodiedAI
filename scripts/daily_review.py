#!/usr/bin/env python3
"""Offline-first discovery and non-publishing human review packages.

Every network read is opt-in. State and packages are separate, adapter
watermarks advance independently, and a checkpoint makes package/state commit
recoverable after interruption or a failed state write.
"""
from __future__ import annotations

import argparse
import copy
import csv
import fcntl
import hashlib
import html
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from email.utils import parsedate_to_datetime
from urllib.parse import parse_qsl, quote, unquote, urlencode, urljoin, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
MANAGED_ROOT = (ROOT / "downloads").resolve()
VERSION = "0.6.0"
INTERRUPTED = False

FINAL_STATUSES = {"approved", "rejected", "superseded"}
AUTO_STATUSES = {"new", "needs_evidence", "needs_user_media", "possible_duplicate", "possible_update", "ready_for_review"}
CANDIDATE_KINDS = {"project", "post"}
SOURCE_KINDS = {"primary", "author_mirror", "secondary_index", "secondary"}
ACCESS_MODES = {"search_text", "page_text", "partial_index", "linked_only"}
RELEVANCE = {"direct", "supporting", "weak_lead", "out_of_scope"}
CONFIDENCE = {"low", "medium", "high"}
ENVIRONMENTS = {"real", "simulation", "real_and_sim", "visual_replay", "simulation_and_hardware_demo", "noninteractive", "mixed", "unknown"}
SECTIONS = {"core", "supporting", "watchlist", "rednote_leads"}
RELATIONS = {"explicit_primary", "explicit_partial", "explicit_author_mirror", "reported_secondary", "infrastructure", "not_established", "comparison_only", "discovery_only"}
EVENT_KINDS = {"exact_day", "month", "unknown"}
EVIDENCE_LEVELS = {"A", "B", "C", "D"}
FORMAL_FILES = (
    "data/projects.json", "data/sources.json", "data/media.json", "data/i18n.json",
    "data/publication_dates.json", "data/artifacts.json", "site/index.html",
    "data/projects.csv", "docs/CATALOG.md", "docs/SOURCES.md", "docs/HUGGING_FACE.md",
    "docs/MEDIA.md", "docs/PUBLICATION_DATES.md", "docs/TAGS.md",
)
SNAPSHOT_FIELDS = (
    "candidate_kind", "title", "title_zh_draft", "title_en_draft", "summary_zh_draft", "summary_en_draft",
    "primary_url", "paper_url", "code_url", "project_url", "post_url", "related_project_url", "authors",
    "proposed_section", "proposed_category", "proposed_environment", "proposed_scene_tags",
    "proposed_gpt6_relation", "proposed_evidence_level", "event_date", "event_date_kind",
    "event_date_basis", "license_status", "control_interface", "metrics", "limitations",
    "relation_facts", "relevance_tier", "media_hashes",
)
SENSITIVE_QUERY = re.compile(r"^(?:token|sig|signature|expires|x-amz-|x-goog-|auth|key|credential|policy)", re.I)
TRACKING_QUERY = re.compile(r"^(?:utm_|fbclid$|gclid$|ref$|source$)", re.I)
RUN_ID_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9._-]{0,78}[A-Za-z0-9_-])?")


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def formal_hashes(root: Path = ROOT) -> dict[str, str]:
    return {name: sha256_file(root / name) for name in FORMAL_FILES}


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def managed_path(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(MANAGED_ROOT)
    except ValueError as exc:
        raise ValueError(f"runtime paths must stay below {MANAGED_ROOT}") from exc
    return resolved


def validate_run_id(value: str) -> str:
    if not RUN_ID_RE.fullmatch(value) or ".." in value:
        raise ValueError("run ID must be 1-80 safe filename characters without '..'")
    return value


def sanitize_url(value: str, *, drop_tracking: bool = True) -> str:
    if not isinstance(value, str) or any(char.isspace() for char in value):
        raise ValueError("URL must be a whitespace-free string")
    parts = urlsplit(value.strip())
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
        raise ValueError("URL must be public HTTPS without credentials")
    try:
        port = parts.port
    except ValueError as exc:
        raise ValueError("URL has an invalid port") from exc
    host = parts.hostname.lower()
    netloc = host + (f":{port}" if port and port != 443 else "")
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    query = []
    for key, item in parse_qsl(parts.query, keep_blank_values=True):
        if SENSITIVE_QUERY.match(key) or (drop_tracking and TRACKING_QUERY.match(key)):
            continue
        query.append((key, item))
    return urlunsplit(("https", netloc, path, urlencode(query, doseq=True), ""))


def redacted_url(value: object) -> str | None:
    try:
        return sanitize_url(str(value))
    except (TypeError, ValueError):
        return None


def canonical_key(value: str) -> str:
    url = sanitize_url(value)
    parts = urlsplit(url)
    segments = [segment for segment in parts.path.split("/") if segment]
    host = parts.hostname or ""
    if host == "github.com" and len(segments) >= 2:
        return f"github:{segments[0].lower()}/{segments[1].removesuffix('.git').lower()}"
    if host in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"} and len(segments) >= 2 and segments[0].lower() in {"abs", "pdf"}:
        identifier = "/".join(segments[1:]).removesuffix(".pdf")
        identifier = re.sub(r"v\d+$", "", identifier, flags=re.I)
        if re.fullmatch(r"(?:\d{4}\.\d{4,5}|[A-Za-z-]+/\d{7})", identifier):
            return "arxiv:" + identifier.lower()
    if host in {"doi.org", "dx.doi.org"} and segments:
        return "doi:" + "/".join(segments).lower()
    if host in {"x.com", "www.x.com", "twitter.com", "www.twitter.com"}:
        match = re.fullmatch(r"/([A-Za-z0-9_]+)/status/(\d+)/?", parts.path)
        if match:
            return "social:x:" + match.group(2)
    if host in {"xiaohongshu.com", "www.xiaohongshu.com"}:
        match = re.fullmatch(r"/(?:explore|discovery/item)/([^/]+)/?", parts.path)
        if match:
            return "social:xiaohongshu:" + match.group(1).lower()
    return "url:" + url


def exact_post_url(value: str) -> bool:
    return canonical_key(value).startswith("social:")


def valid_date(value: object, kind: str) -> bool:
    if kind == "unknown":
        return value is None
    if not isinstance(value, str):
        return False
    try:
        if kind == "month":
            return bool(re.fullmatch(r"\d{4}-\d{2}", value)) and date.fromisoformat(value + "-01") is not None
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)) and date.fromisoformat(value) is not None
    except ValueError:
        return False


def host_allowed(url: str, policy: dict) -> bool:
    host = urlsplit(sanitize_url(url)).hostname or ""
    allow = {str(item).lower() for item in policy.get("allowlist", [])}
    deny = {str(item).lower() for item in policy.get("denylist", [])}
    matches = lambda domain: host == domain or host.endswith("." + domain)
    return not any(matches(domain) for domain in deny) and (not allow or any(matches(domain) for domain in allow))


def content_allowed(item: dict, policy: dict) -> bool:
    text = json.dumps(item, ensure_ascii=False).lower()
    if any(str(term).lower() in text for term in policy.get("deny_terms", [])):
        return False
    language = item.get("language")
    languages = policy.get("languages", [])
    return not language or not languages or language in languages


def load_config(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    for key in ("schedule", "discovery", "runtime", "persistence", "sources", "queries", "adapters"):
        if key not in value:
            raise ValueError(f"configuration missing {key}")
    if not value["queries"].get("model_terms") or not value["queries"].get("embodied_terms"):
        raise ValueError("both model_terms and embodied_terms are required")
    for query in value["sources"].get("arxiv_queries", []):
        if not isinstance(query, dict) or not query.get("name") or "{model_terms}" not in query.get("query_template", "") or "{embodied_terms}" not in query.get("query_template", ""):
            raise ValueError("each arxiv query needs name and both term placeholders")
        if int(query.get("page_size", 25)) < 1 or int(query.get("max_pages", 4)) < 1:
            raise ValueError("arxiv page_size and max_pages must be positive")
    names = [query["name"] for query in value["sources"].get("arxiv_queries", [])]
    if len(names) != len(set(names)):
        raise ValueError("arxiv query names must be unique")
    for group in ("github_searches", "feeds"):
        entries = value["sources"].get(group, [])
        if any(not isinstance(entry, dict) or not entry.get("name") for entry in entries):
            raise ValueError(f"each {group} entry needs a name")
        group_names = [entry["name"] for entry in entries]
        if len(group_names) != len(set(group_names)):
            raise ValueError(f"{group} names must be unique")
    return value


def default_state() -> dict:
    return {"version": 2, "revision": 0, "identities": {}, "aliases": {}, "adapters": {}, "decisions": [], "committed_runs": {}}


def load_state(path: Path) -> dict:
    if not path.exists():
        return default_state()
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("version") != 2:
        raise ValueError("unsupported state version; migrate or use a new state root")
    value.setdefault("revision", 0)
    value.setdefault("aliases", {})
    value.setdefault("committed_runs", {})
    return value


def unfinished_checkpoints(state_root: Path, ignored_run: str | None = None) -> list[tuple[str, str]]:
    result = []
    for path in sorted((state_root / "runs").glob("*.json")) if (state_root / "runs").exists() else []:
        data = json.loads(path.read_text(encoding="utf-8"))
        if path.stem != ignored_run and data.get("phase") in {"collecting", "restart_pending", "package_ready", "package_published"}:
            result.append((path.stem, str(data.get("phase"))))
    return result


def official_index(root: Path = ROOT) -> dict[str, str]:
    projects = json.loads((root / "data/projects.json").read_text(encoding="utf-8"))
    result: dict[str, str] = {}
    for project in projects:
        for url in [project.get("url"), project.get("code_url"), *project.get("links", {}).values()]:
            if isinstance(url, str) and url.startswith("https://"):
                try:
                    result[canonical_key(url)] = project["id"]
                except ValueError:
                    pass
    return result


def adapter_window(adapter_key: str, state: dict, upper: datetime, config: dict, explicit: str | None) -> dict:
    pending = state.get("adapters", {}).get(adapter_key, {}).get("pending_scan")
    config_hash = config.get("_hash")
    if pending and pending.get("config_hash") == config_hash:
        # Remote search rankings are not snapshots. An unfinished scan therefore
        # restarts at page zero inside the frozen time window.
        return {"lower_bound": pending["lower_bound"], "upper_bound": pending["upper_bound"], "cursor": 0}
    if explicit:
        lower = parse_time(explicit)
        return {"lower_bound": iso(lower), "upper_bound": iso(upper), "cursor": 0}
    record = state.get("adapters", {}).get(adapter_key, {})
    if record.get("last_successful_upper_bound"):
        lower = parse_time(record["last_successful_upper_bound"]) - timedelta(hours=config["discovery"]["overlap_hours"])
    else:
        lower = upper - timedelta(days=config["discovery"]["initial_lookback_days"])
    return {"lower_bound": iso(lower), "upper_bound": iso(upper), "cursor": 0}


def seed_specs(config: dict) -> list[dict]:
    result = []
    mappings = (
        ("project_pages", "project", "primary"),
        ("huggingface_seeds", "project", "primary"), ("social_post_seeds", "post", "author_mirror"),
        ("discovery_indexes", "project", "secondary_index"),
    )
    for group, kind, source_kind in mappings:
        for value in config["sources"].get(group, []):
            entry = value if isinstance(value, dict) else {"url": value}
            stable = sha256_bytes(str(entry.get("url", "")).encode())[:10]
            result.append({"adapter_key": f"seed:{group}:{stable}", "group": group, "candidate_kind": kind, "source_kind": source_kind, **entry})
    return result


def planned_adapters(config: dict, fixture: Path | None, selected: set[str] | None) -> list[dict]:
    plans = []
    if fixture and config["adapters"].get("fixture", {}).get("enabled", True) and (not selected or "fixture" in selected):
        plans.append({"adapter_key": "fixture", "type": "fixture", "path": fixture})
    if config["adapters"].get("seed", {}).get("enabled", True) and (not selected or "seed" in selected):
        plans.extend({**spec, "type": "seed"} for spec in seed_specs(config))
    if config["adapters"].get("arxiv", {}).get("enabled", True) and (not selected or "arxiv" in selected):
        plans.extend({"adapter_key": f"arxiv:{query['name']}", "type": "arxiv", "query": query} for query in config["sources"].get("arxiv_queries", []))
    if config["adapters"].get("github", {}).get("enabled", True) and (not selected or "github" in selected):
        plans.extend({"adapter_key": f"github-search:{query['name']}", "type": "github_search", "query": query} for query in config["sources"].get("github_searches", []))
        for repo in config["sources"].get("github_repositories", []):
            value = repo if isinstance(repo, dict) else {"repo": repo}
            plans.append({"adapter_key": "github-repo:" + value["repo"].lower(), "type": "github_repo", "repo": value})
    if config["adapters"].get("feed", {}).get("enabled", True) and (not selected or "feed" in selected):
        plans.extend({"adapter_key": f"feed:{feed['name']}", "type": "feed", "feed": feed} for feed in config["sources"].get("feeds", []))
    return plans


class RedirectBlocked(urllib.error.URLError):
    pass


class PolicyRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, policy: dict):
        super().__init__()
        self.policy = policy

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = sanitize_url(newurl, drop_tracking=False)
        if not host_allowed(target, self.policy):
            raise RedirectBlocked("redirect_target_not_allowed")
        return super().redirect_request(req, fp, code, msg, headers, target)


class HttpClient:
    def __init__(self, minimum_interval: float, *, clock=time.monotonic, sleeper=time.sleep):
        self.minimum_interval = max(0.0, float(minimum_interval))
        self.clock = clock
        self.sleeper = sleeper
        self.last_started: float | None = None

    def get(self, url: str, timeout: float, retries: int, accept: str, policy: dict) -> dict:
        safe_url = sanitize_url(url, drop_tracking=False)
        if not host_allowed(safe_url, policy):
            return {"status": None, "body": b"", "final_url": safe_url, "error": "source_not_allowed"}
        last_error, last_status = None, None
        opener = urllib.request.build_opener(PolicyRedirectHandler(policy))
        for attempt in range(retries + 1):
            if INTERRUPTED:
                return {"status": None, "body": b"", "final_url": safe_url, "error": "interrupted"}
            now = self.clock()
            if self.last_started is not None:
                delay = self.minimum_interval - (now - self.last_started)
                if delay > 0:
                    self.sleeper(delay)
            self.last_started = self.clock()
            try:
                request = urllib.request.Request(safe_url, headers={"User-Agent": f"awesome-GPT6-review/{VERSION}", "Accept": accept})
                with opener.open(request, timeout=timeout) as response:
                    final_url = sanitize_url(response.geturl())
                    if not host_allowed(final_url, policy):
                        return {"status": response.status, "body": b"", "final_url": final_url, "error": "redirect_target_not_allowed"}
                    body = response.read(2 * 1024 * 1024)
                    return {"status": response.status, "body": body, "final_url": final_url, "content_type": response.headers.get("Content-Type", ""), "error": None}
            except urllib.error.HTTPError as exc:
                last_status, last_error = exc.code, f"http_{exc.code}"
                if exc.code < 500 and exc.code != 429:
                    break
            except RedirectBlocked:
                return {"status": None, "body": b"", "final_url": safe_url, "error": "redirect_target_not_allowed"}
            except (OSError, ValueError, urllib.error.URLError) as exc:
                last_error = f"{type(exc).__name__}:{str(exc)[:160]}"
        return {"status": last_status, "body": b"", "final_url": safe_url, "content_type": "", "error": last_error or "request_failed"}


def http_get(url: str, timeout: float, retries: int, accept: str, policy: dict | None = None, client: HttpClient | None = None) -> dict:
    return (client or HttpClient(0)).get(url, timeout, retries, accept, policy or {})


def looks_like_login(result: dict) -> bool:
    final_path = urlsplit(result.get("final_url") or "https://invalid.example/").path.lower()
    sample = result.get("body", b"")[:200000].decode("utf-8", errors="ignore").lower()
    return "/login" in final_path or ("<form" in sample and ("password" in sample or "sign in" in sample))


def fixture_adapter(plan: dict) -> dict:
    try:
        value = json.loads(Path(plan["path"]).read_text(encoding="utf-8"))
        if not isinstance(value, list):
            raise ValueError("fixture must be a JSON array")
        return {"items": value, "failures": [], "complete": True, "pages_complete": True}
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {"items": [], "failures": [{"reason": f"fixture_error:{exc}", "source_url": None}], "complete": False, "pages_complete": False}


def seed_adapter(plan: dict, config: dict, network: bool, client: HttpClient | None = None) -> dict:
    policy = config["adapters"]["seed"]
    source_url = redacted_url(plan.get("url"))
    if not source_url or not host_allowed(source_url, policy):
        return {"items": [], "failures": [{"reason": "source_not_allowed", "source_url": source_url}], "complete": False, "pages_complete": False}
    if not network:
        return {"items": [], "failures": [{"reason": "network_opt_in_required", "source_url": source_url}], "complete": False, "pages_complete": False}
    result = http_get(plan["url"], config["runtime"]["timeout_seconds"], config["runtime"]["retries"], "text/html,application/xhtml+xml", policy, client)
    final_url = redacted_url(result.get("final_url"))
    if result.get("error") or result.get("status") != 200 or looks_like_login(result):
        reason = "login_wall" if looks_like_login(result) else result.get("error") or f"http_{result.get('status')}"
        return {"items": [], "failures": [{"reason": reason, "source_url": source_url, "final_url": final_url, "http_status": result.get("status")}], "complete": False, "pages_complete": False}
    if not final_url or not host_allowed(final_url, policy):
        return {"items": [], "failures": [{"reason": "redirect_target_not_allowed", "source_url": source_url, "final_url": final_url, "http_status": result.get("status")}], "complete": False, "pages_complete": False}
    page = result["body"].decode("utf-8", errors="replace")
    match = re.search(r"<title[^>]*>(.*?)</title>", page, re.I | re.S)
    title = html.unescape(re.sub(r"\s+", " ", match.group(1)).strip()) if match else plan.get("title", final_url)
    item = {
        "primary_url": final_url, "candidate_kind": plan["candidate_kind"], "title": title,
        "title_zh_draft": plan.get("title_zh_draft", title), "title_en_draft": plan.get("title_en_draft", title),
        "summary_zh_draft": "机器草案：配置种子页面，关系待人工核验。", "summary_en_draft": "Machine draft: configured seed page; relation pending review.",
        "source_kind": plan["source_kind"], "access": "page_text", "relation_facts": [],
        "relevance_tier": "weak_lead", "inference_confidence": "low", "language": plan.get("language"),
        "unresolved_questions": ["页面是否提供 GPT-6/Astra 具身成果的一手证据？"],
        "_discovery": {"source_url": source_url, "final_url": final_url, "http_status": 200, "content_hash": sha256_bytes(result["body"]), "aliases": list(dict.fromkeys([source_url, final_url]))},
    }
    if not content_allowed(item, policy):
        return {"items": [], "failures": [], "complete": True, "pages_complete": True, "filtered_count": 1}
    items = [item]
    if plan.get("group") == "discovery_indexes":
        links = []
        for href in re.findall(r"href\s*=\s*['\"]([^'\"]+)['\"]", page, re.I):
            try:
                target = sanitize_url(urljoin(final_url, html.unescape(href)))
                if exact_post_url(target):
                    links.append(target)
            except ValueError:
                continue
        items = []
        for target in dict.fromkeys(links):
            items.append({
                "primary_url": target, "post_url": target, "candidate_kind": "post", "title": f"Post discovered from {title}",
                "title_zh_draft": f"从公开索引发现的帖子：{title}", "title_en_draft": f"Post discovered from public index: {title}",
                "summary_zh_draft": "机器草案：索引只提供帖子入口，内容和成果关系待人工核验。",
                "summary_en_draft": "Machine draft: the index exposes a post entry; content and project relation require review.",
                "source_kind": "secondary_index", "access": "linked_only", "relation_facts": ["A configured public index linked this exact post URL."],
                "relevance_tier": "weak_lead", "inference_confidence": "low", "language": plan.get("language"),
                "unresolved_questions": ["帖子正文是否提供与候选成果相关的一手证据？"],
                "_discovery": {"source_url": final_url, "final_url": final_url, "http_status": 200,
                               "content_hash": sha256_bytes(target.encode()), "aliases": [target]},
            })
        if not items:
            item["unresolved_questions"].append("索引中未发现可规范化的具体帖子入口。")
            items = [item]
    return {"items": items, "failures": [], "complete": True, "pages_complete": True}


def render_arxiv_query(query: dict, config: dict) -> str:
    quoted = lambda terms: "(" + " OR ".join(f'all:\"{term}\"' for term in terms) + ")"
    return query["query_template"].replace("{model_terms}", quoted(config["queries"]["model_terms"])).replace("{embodied_terms}", quoted(config["queries"]["embodied_terms"]))


def parse_arxiv_page(body: bytes) -> tuple[list[dict], int]:
    root = ET.fromstring(body)
    atom = "{http://www.w3.org/2005/Atom}"
    open_search = "{http://a9.com/-/spec/opensearch/1.1/}"
    total_node = root.find(open_search + "totalResults")
    total = int(total_node.text) if total_node is not None and total_node.text else len(root.findall(atom + "entry"))
    entries = []
    for entry in root.findall(atom + "entry"):
        value = lambda tag: re.sub(r"\s+", " ", (entry.findtext(atom + tag) or "")).strip()
        entry_id = value("id")
        links = {node.attrib.get("rel", "alternate"): node.attrib.get("href") for node in entry.findall(atom + "link")}
        entries.append({"id": entry_id, "title": value("title"), "summary": value("summary"), "published": value("published"), "updated": value("updated"), "authors": [re.sub(r"\s+", " ", (author.findtext(atom + "name") or "")).strip() for author in entry.findall(atom + "author")], "primary_url": links.get("alternate") or entry_id})
    return entries, total


def load_response_fixture(path: Path | None) -> dict:
    if path is None:
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    value["_base"] = str(path.parent)
    return value


def fixture_response(responses: dict, spec: dict, request_url: str) -> dict:
    base = Path(responses["_base"]).resolve()
    file_path = (base / spec["body_file"]).resolve()
    file_path.relative_to(base)
    return {"status": spec.get("status", 200), "body": file_path.read_bytes(),
            "final_url": spec.get("final_url", request_url), "error": spec.get("error")}


def json_result(result: dict, source_url: str) -> tuple[object | None, dict | None]:
    status = result.get("status")
    if result.get("error") or status != 200 or looks_like_login(result):
        reason = "login_wall" if looks_like_login(result) else result.get("error") or f"http_{status}"
        return None, {"reason": reason, "source_url": source_url, "final_url": redacted_url(result.get("final_url")), "http_status": status}
    try:
        return json.loads(result["body"]), None
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, {"reason": f"parse_error:{exc}", "source_url": source_url, "http_status": status}


def github_search_adapter(plan: dict, config: dict, lower: datetime, upper: datetime, network: bool,
                          responses: dict, client: HttpClient | None = None) -> dict:
    policy = config["adapters"]["github"]
    spec = plan["query"]
    page_size, max_pages = int(spec.get("page_size", 30)), int(spec.get("max_pages", 4))
    model = " OR ".join(f'"{term}"' for term in config["queries"]["model_terms"])
    embodied = " OR ".join(f'"{term}"' for term in config["queries"]["embodied_terms"])
    query = spec.get("query_template", "({model_terms}) ({embodied_terms})").replace("{model_terms}", model).replace("{embodied_terms}", embodied)
    pages = responses.get(plan["adapter_key"])
    configured_repos = {(row.get("repo") if isinstance(row, dict) else row).lower() for row in config["sources"].get("github_repositories", [])}
    items, failures, total, received = [], [], None, 0
    for page in range(1, max_pages + 1):
        api_url = "https://api.github.com/search/repositories?" + urlencode({"q": query, "sort": "updated", "order": "desc", "per_page": page_size, "page": page})
        if pages is not None:
            if page > len(pages):
                failures.append({"reason": "fixture_missing_page", "source_url": api_url}); break
            result = fixture_response(responses, pages[page - 1], api_url)
        elif network:
            result = http_get(api_url, config["runtime"]["timeout_seconds"], config["runtime"]["retries"], "application/vnd.github+json", policy, client)
        else:
            failures.append({"reason": "network_opt_in_required", "source_url": api_url}); break
        payload, failure = json_result(result, api_url)
        if failure:
            failures.append(failure); break
        if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
            failures.append({"reason": "parse_error:invalid_github_search_shape", "source_url": api_url}); break
        if payload.get("incomplete_results") is not False:
            failures.append({"reason": "github_incomplete_results", "source_url": api_url}); break
        try:
            reported_total = int(payload.get("total_count", len(payload["items"])))
        except (TypeError, ValueError):
            failures.append({"reason": "parse_error:invalid_github_total_count", "source_url": api_url}); break
        if reported_total > 1000:
            failures.append({"reason": "github_search_result_cap_exceeded", "source_url": api_url}); break
        if total is not None and reported_total != total:
            failures.append({"reason": "github_search_total_changed_during_pagination", "source_url": api_url}); break
        total = reported_total
        page_rows = payload["items"]
        if not page_rows and received < total:
            failures.append({"reason": "github_search_early_empty_page", "source_url": api_url}); break
        received += len(page_rows)
        for repo in page_rows:
            if str(repo.get("full_name", "")).lower() in configured_repos:
                # The configured repository adapter will provide stronger,
                # original-entry evidence in this same batch.
                continue
            pushed = repo.get("pushed_at") or repo.get("updated_at")
            try:
                timestamp = parse_time(pushed)
                primary = sanitize_url(repo["html_url"])
            except (AttributeError, KeyError, TypeError, ValueError):
                failures.append({"reason": "github_search_invalid_repository_entry", "source_url": api_url})
                continue
            if not (lower <= timestamp <= upper):
                continue
            text = " ".join(str(repo.get(key, "")) for key in ("name", "full_name", "description")).lower()
            if not any(term.lower() in text for term in config["queries"]["model_terms"]) or not any(term.lower() in text for term in config["queries"]["embodied_terms"]):
                continue
            items.append({"primary_url": primary, "code_url": primary, "candidate_kind": "project", "title": repo.get("name") or repo.get("full_name"),
                "title_en_draft": repo.get("name") or repo.get("full_name"), "title_zh_draft": repo.get("name") or repo.get("full_name"),
                "summary_en_draft": "Machine draft: GitHub public search lead; repository facts require review.",
                "summary_zh_draft": "机器草案：GitHub 公开检索线索；仓库事实待人工核验。",
                "source_kind": "secondary_index", "access": "search_text", "language": "en", "relation_facts": ["GitHub public repository search matched configured terms."],
                "relevance_tier": "weak_lead", "inference_confidence": "low", "event_date": timestamp.date().isoformat(), "event_date_kind": "exact_day",
                "event_date_basis": "GitHub repository pushed_at/updated_at", "event_timezone": "UTC", "event_timestamp_raw": pushed,
                "proposed_section": "watchlist", "unresolved_questions": ["仓库 README、release 或 commit 是否明确证明模型与具身任务关系？"],
                "_discovery": {"source_url": api_url, "final_url": redacted_url(result.get("final_url")), "http_status": result.get("status"),
                               "content_hash": sha256_bytes(json.dumps(repo, sort_keys=True).encode()), "aliases": [primary]}})
        if received >= total:
            break
    pages_fetched = page if 'page' in locals() else 0
    complete = not failures and total is not None and received >= total
    if not complete and not failures:
        failures.append({"reason": "pagination_incomplete_unstable_ranking_restart_required", "source_url": api_url})
    return {"items": items, "failures": failures, "complete": complete, "pages_complete": complete,
            "pages_fetched": pages_fetched, "total_results": total, "next_cursor": None if complete else 0}


def github_repo_adapter(plan: dict, config: dict, lower: datetime, upper: datetime, network: bool,
                        responses: dict, client: HttpClient | None = None) -> dict:
    policy = config["adapters"]["github"]
    repo = plan["repo"]["repo"].strip("/")
    endpoints = {"repository": f"https://api.github.com/repos/{repo}",
                 "releases": f"https://api.github.com/repos/{repo}/releases?per_page=100",
                 "commits": f"https://api.github.com/repos/{repo}/commits?" + urlencode({"since": iso(lower), "until": iso(upper), "per_page": 100})}
    specs = responses.get(plan["adapter_key"])
    payloads, failures = {}, []
    for kind, url in endpoints.items():
        if specs is not None:
            result = fixture_response(responses, specs[kind], url)
        elif network:
            result = http_get(url, config["runtime"]["timeout_seconds"], config["runtime"]["retries"], "application/vnd.github+json", policy, client)
        else:
            failures.append({"reason": "network_opt_in_required", "source_url": url}); break
        payload, failure = json_result(result, url)
        if failure:
            failures.append(failure); break
        payloads[kind] = payload
    if failures:
        return {"items": [], "failures": failures, "complete": False, "pages_complete": False}
    repository = payloads.get("repository")
    if not isinstance(repository, dict) or not isinstance(payloads.get("releases"), list) or not isinstance(payloads.get("commits"), list):
        return {"items": [], "failures": [{"reason": "parse_error:invalid_github_repo_shape", "source_url": endpoints["repository"]}], "complete": False, "pages_complete": False}
    if len(payloads["releases"]) >= 100 or len(payloads["commits"]) >= 100:
        return {"items": [], "failures": [{"reason": "pagination_incomplete_github_repo_endpoint", "source_url": endpoints["commits"]}],
                "complete": False, "pages_complete": False, "pages_fetched": 3, "next_cursor": 0}
    try:
        primary = sanitize_url(repository["html_url"])
    except (KeyError, TypeError, ValueError):
        return {"items": [], "failures": [{"reason": "github_repo_invalid_repository_entry", "source_url": endpoints["repository"]}], "complete": False, "pages_complete": False}
    releases = [row for row in payloads["releases"] if row.get("published_at")]
    commits = payloads["commits"]
    invalid_commit = lambda row: (not isinstance(row, dict) or not isinstance(row.get("commit"), dict)
                                  or not isinstance(row["commit"].get("committer"), dict)
                                  or not row["commit"]["committer"].get("date"))
    if any(not isinstance(row, dict) for row in payloads["releases"]) or any(invalid_commit(row) for row in commits):
        return {"items": [], "failures": [{"reason": "github_repo_invalid_update_entry", "source_url": endpoints["commits"]}], "complete": False, "pages_complete": False}
    dates = [repository.get("pushed_at")] + [row.get("published_at") for row in releases] + [row.get("commit", {}).get("committer", {}).get("date") for row in commits]
    try:
        parsed = [parse_time(value) for value in dates if value]
    except (AttributeError, TypeError, ValueError):
        return {"items": [], "failures": [{"reason": "github_repo_invalid_timestamp", "source_url": endpoints["commits"]}], "complete": False, "pages_complete": False}
    in_window = [value for value in parsed if lower <= value <= upper]
    if not in_window:
        return {"items": [], "failures": [], "complete": True, "pages_complete": True, "pages_fetched": 3, "total_results": 0}
    latest = max(in_window)
    facts = ["Configured GitHub repository metadata was read from the public API."]
    if releases: facts.append(f"Public API returned {len(releases)} release record(s).")
    if commits: facts.append(f"Public API returned {len(commits)} commit record(s) in the frozen window.")
    item = {"primary_url": primary, "code_url": primary, "candidate_kind": "project", "title": repository.get("name") or repo,
        "title_en_draft": repository.get("name") or repo, "title_zh_draft": repository.get("name") or repo,
        "summary_en_draft": repository.get("description") or "Machine draft from public GitHub repository metadata.",
        "summary_zh_draft": "机器草案：来自 GitHub 公开仓库、release 与 commit 元数据。", "source_kind": "primary", "access": "page_text", "language": "en",
        "relation_facts": facts, "relevance_tier": "weak_lead", "inference_confidence": "low", "event_date": latest.date().isoformat(),
        "event_date_kind": "exact_day", "event_date_basis": "GitHub pushed_at/release published_at/commit committer date", "event_timezone": "UTC",
        "event_timestamp_raw": iso(latest), "proposed_section": "watchlist", "unresolved_questions": ["README 或 release 正文是否明确模型关系？"],
        "_discovery": {"source_url": endpoints["repository"], "final_url": endpoints["repository"], "http_status": 200,
                       "content_hash": sha256_bytes(json.dumps(payloads, sort_keys=True).encode()), "aliases": [primary]}}
    return {"items": [item], "failures": [], "complete": True, "pages_complete": True, "pages_fetched": 3, "total_results": 1}


def parse_feed(body: bytes, feed_url: str) -> list[dict]:
    root = ET.fromstring(body)
    atom = "{http://www.w3.org/2005/Atom}"
    rows = []
    if root.tag == atom + "feed":
        for entry in root.findall(atom + "entry"):
            links = [node.attrib.get("href") for node in entry.findall(atom + "link") if node.attrib.get("href")]
            rows.append({"title": entry.findtext(atom + "title") or "Untitled feed entry", "url": links[0] if links else entry.findtext(atom + "id"),
                         "date": entry.findtext(atom + "updated") or entry.findtext(atom + "published"),
                         "text": " ".join(filter(None, [entry.findtext(atom + "summary"), entry.findtext(atom + "content")]))})
    elif root.tag.lower().endswith("rss") and root.find("channel") is not None:
        for entry in root.findall("./channel/item"):
            rows.append({"title": entry.findtext("title") or "Untitled feed entry", "url": entry.findtext("link") or entry.findtext("guid"),
                         "date": entry.findtext("pubDate"), "text": entry.findtext("description") or ""})
    else:
        raise ValueError("invalid_feed_root")
    for row in rows:
        if row.get("url"): row["url"] = urljoin(feed_url, row["url"])
    return rows


def feed_adapter(plan: dict, config: dict, lower: datetime, upper: datetime, network: bool,
                 responses: dict, client: HttpClient | None = None) -> dict:
    policy, feed = config["adapters"]["feed"], plan["feed"]
    url = sanitize_url(feed["url"])
    spec = responses.get(plan["adapter_key"])
    if spec is not None:
        result = fixture_response(responses, spec, url)
    elif network:
        result = http_get(url, config["runtime"]["timeout_seconds"], config["runtime"]["retries"], "application/atom+xml,application/rss+xml", policy, client)
    else:
        return {"items": [], "failures": [{"reason": "network_opt_in_required", "source_url": url}], "complete": False, "pages_complete": False}
    body_text = result.get("body", b"")[:200000].decode("utf-8", errors="ignore").lower()
    feed_login = looks_like_login(result) or "sign in to see feed" in body_text or "login to see feed" in body_text
    if result.get("error") or result.get("status") != 200 or feed_login:
        reason = "login_wall" if feed_login else result.get("error") or f"http_{result.get('status')}"
        return {"items": [], "failures": [{"reason": reason, "source_url": url, "http_status": result.get("status")}], "complete": False, "pages_complete": False}
    try:
        entries = parse_feed(result["body"], url)
    except (ET.ParseError, ValueError) as exc:
        return {"items": [], "failures": [{"reason": f"parse_error:{exc}", "source_url": url}], "complete": False, "pages_complete": False}
    items = []
    failures = []
    for entry in entries:
        try:
            entry_url = sanitize_url(entry["url"])
        except (TypeError, ValueError):
            failures.append({"reason": "feed_entry_invalid_url", "source_url": url})
            continue
        timestamp = None
        if entry.get("date"):
            try:
                timestamp = parse_time(entry["date"]) if "T" in entry["date"] else parsedate_to_datetime(entry["date"]).astimezone(timezone.utc)
            except (TypeError, ValueError, OverflowError):
                timestamp = None
        if timestamp is not None and not lower <= timestamp <= upper: continue
        found = []
        for candidate_url in re.findall(r"https://[^\s<>\"']+", html.unescape(entry["text"] or "")):
            try:
                candidate_url = sanitize_url(candidate_url.rstrip(".,)"))
                if exact_post_url(candidate_url): found.append(candidate_url)
            except ValueError: pass
        primary = found[0] if found else entry_url
        kind = "post" if exact_post_url(primary) else "project"
        items.append({"primary_url": primary, "post_url": primary if kind == "post" else None, "candidate_kind": kind, "title": re.sub(r"\s+", " ", entry["title"]).strip(),
            "title_en_draft": entry["title"], "title_zh_draft": entry["title"],
            "summary_en_draft": "Machine draft: public feed lead; original evidence requires review.", "summary_zh_draft": "机器草案：公开 feed 线索；原始证据待核验。",
            "source_kind": "secondary_index" if found else feed.get("source_kind", "secondary_index"), "access": "linked_only", "language": feed.get("language"),
            "relation_facts": (["A public feed entry linked an exact post URL."] if found else ["A configured public feed published this lead."]),
            "relevance_tier": "weak_lead", "inference_confidence": "low", "event_date": timestamp.date().isoformat() if timestamp else None,
            "event_date_kind": "exact_day" if timestamp else "unknown", "event_date_basis": "Atom updated/published or RSS pubDate" if timestamp else None,
            "event_timezone": "UTC" if timestamp else None, "event_timestamp_raw": entry.get("date"),
            "proposed_section": "watchlist", "unresolved_questions": ["能否从 feed 入口追到与成果有关的原始证据？"] + (["Feed entry date missing or unparseable; retained as unknown."] if timestamp is None else []),
            "_discovery": {"source_url": url, "final_url": redacted_url(result.get("final_url")), "http_status": result.get("status"),
                           "content_hash": sha256_bytes(json.dumps(entry, sort_keys=True).encode()), "aliases": [primary]}})
    complete = not failures
    return {"items": items, "failures": failures, "complete": complete, "pages_complete": complete, "pages_fetched": 1, "total_results": len(entries)}


def arxiv_adapter(plan: dict, config: dict, lower: datetime, upper: datetime, network: bool, responses: dict,
                  cursor: int = 0, client: HttpClient | None = None) -> dict:
    policy = config["adapters"]["arxiv"]
    query = render_arxiv_query(plan["query"], config)
    page_size = int(plan["query"].get("page_size", 25))
    max_pages = int(plan["query"].get("max_pages", 4))
    fixture_pages = responses.get(plan["adapter_key"])
    # arXiv documents start/max_results offsets but does not promise a frozen
    # result set across calls. Always restart an unfinished scan at zero.
    items, failures, start, page_number, total = [], [], 0, 0, None
    while page_number < max_pages and (total is None or start < total):
        if INTERRUPTED:
            failures.append({"reason": "interrupted", "source_url": None})
            break
        api_url = "https://export.arxiv.org/api/query?" + urlencode({"search_query": query, "start": start, "max_results": page_size, "sortBy": "lastUpdatedDate", "sortOrder": "descending"})
        if fixture_pages is not None:
            fixture_index = start // page_size
            if fixture_index >= len(fixture_pages):
                failures.append({"reason": "fixture_missing_page", "source_url": api_url})
                break
            page_spec = fixture_pages[fixture_index]
            fixture_base = Path(responses["_base"]).resolve()
            fixture_file = (fixture_base / page_spec["body_file"]).resolve()
            fixture_file.relative_to(fixture_base)
            body = fixture_file.read_bytes()
            result = {"status": page_spec.get("status", 200), "body": body, "final_url": page_spec.get("final_url", api_url), "error": page_spec.get("error")}
        elif network:
            result = http_get(api_url, config["runtime"]["timeout_seconds"], config["runtime"]["retries"], "application/atom+xml", policy, client)
        else:
            failures.append({"reason": "network_opt_in_required", "source_url": api_url})
            break
        status = result.get("status")
        final_url = redacted_url(result.get("final_url"))
        if final_url and not host_allowed(final_url, policy):
            failures.append({"reason": "redirect_target_not_allowed", "source_url": api_url, "final_url": final_url, "http_status": status})
            break
        if result.get("error") or status != 200 or looks_like_login(result):
            failures.append({"reason": "login_wall" if looks_like_login(result) else result.get("error") or f"http_{status}", "source_url": api_url, "final_url": redacted_url(result.get("final_url")), "http_status": status})
            break
        try:
            entries, total = parse_arxiv_page(result["body"])
        except (ET.ParseError, ValueError) as exc:
            failures.append({"reason": f"parse_error:{exc}", "source_url": api_url, "http_status": status})
            break
        for entry in entries:
            text = (entry["title"] + " " + entry["summary"]).lower()
            if not any(term.lower() in text for term in config["queries"]["model_terms"]) or not any(term.lower() in text for term in config["queries"]["embodied_terms"]):
                continue
            timestamp_text = entry["updated"] or entry["published"]
            try:
                timestamp = parse_time(timestamp_text)
            except ValueError:
                failures.append({"reason": "invalid_entry_timestamp", "source_url": redacted_url(entry["primary_url"])})
                continue
            if timestamp < lower or timestamp > upper:
                continue
            primary = sanitize_url(entry["primary_url"])
            item = {
                "primary_url": primary, "paper_url": primary, "candidate_kind": "project", "title": entry["title"],
                "title_zh_draft": entry["title"], "title_en_draft": entry["title"],
                "summary_zh_draft": "机器草案：arXiv 查询命中；具体模型关系与实验结论待人工核验。",
                "summary_en_draft": "Machine draft: arXiv query match; model relation and experimental claims require human verification.",
                "authors": entry["authors"], "source_kind": "primary", "access": "page_text", "language": "en",
                "relation_facts": ["The arXiv title or abstract contains a configured model term and an embodied term."],
                "relevance_tier": "weak_lead", "relevance_inference": "可能是相关论文，不能仅凭查询命中晋级。", "inference_confidence": "low",
                "event_date": timestamp.date().isoformat(), "event_date_kind": "exact_day", "event_date_basis": "arXiv updated timestamp",
                "event_timezone": "UTC", "event_timestamp_raw": timestamp_text, "event_date_parse_method": "Atom ISO-8601 updated/published",
                "proposed_section": "watchlist", "proposed_environment": "unknown", "proposed_scene_tags": [],
                "proposed_gpt6_relation": "discovery_only", "proposed_evidence_level": "D", "license_status": "unknown",
                "control_interface": "unknown", "metrics": [], "limitations": ["Only title/abstract query relevance has been checked."],
                "unresolved_questions": ["全文是否明确说明 GPT-6/Astra 实际参与具身任务？"],
                "_discovery": {"source_url": api_url, "final_url": final_url, "http_status": status,
                               "content_hash": sha256_bytes(json.dumps(entry, ensure_ascii=False, sort_keys=True).encode()), "aliases": [primary]},
            }
            if host_allowed(primary, policy) and content_allowed(item, policy):
                items.append(item)
        start += len(entries)
        page_number += 1
        if not entries:
            break
    complete = not failures and total is not None and start >= total
    if not complete and not failures:
        failures.append({"reason": "pagination_incomplete_unstable_offset_restart_required", "source_url": api_url})
    return {"items": items, "failures": failures, "complete": complete, "pages_complete": complete,
            "pages_fetched": page_number, "total_results": total, "next_cursor": None if complete else 0}


def validate_candidate_input(raw: dict, taxonomy: dict) -> tuple[str, str, dict]:
    if not isinstance(raw, dict):
        raise ValueError("candidate must be an object")
    primary = sanitize_url(raw["primary_url"])
    key = canonical_key(primary)
    kind = raw.get("candidate_kind", "post" if key.startswith("social:") else "project")
    if kind not in CANDIDATE_KINDS:
        raise ValueError("invalid candidate_kind")
    if kind == "post" and not exact_post_url(primary):
        raise ValueError("post candidates require a specific X status or Xiaohongshu note URL")
    checks = (
        (raw.get("source_kind", "secondary") in SOURCE_KINDS, "invalid source_kind"),
        (raw.get("access", "linked_only") in ACCESS_MODES, "invalid access"),
        (raw.get("relevance_tier", "weak_lead") in RELEVANCE, "invalid relevance_tier"),
        (raw.get("inference_confidence", "low") in CONFIDENCE, "invalid inference_confidence"),
        (raw.get("proposed_environment", "unknown") in ENVIRONMENTS, "invalid proposed_environment"),
        (raw.get("proposed_section", "watchlist") in SECTIONS, "invalid proposed_section"),
        (raw.get("proposed_gpt6_relation", "discovery_only") in RELATIONS, "invalid proposed_gpt6_relation"),
        (raw.get("proposed_evidence_level", "D") in EVIDENCE_LEVELS, "invalid proposed_evidence_level"),
    )
    for ok, message in checks:
        if not ok:
            raise ValueError(message)
    scene_tags = raw.get("proposed_scene_tags", [])
    if not isinstance(scene_tags, list) or len(scene_tags) != len(set(scene_tags)) or not set(scene_tags).issubset({"sim", "real"}):
        raise ValueError("invalid proposed_scene_tags")
    event_kind = raw.get("event_date_kind", "unknown")
    if event_kind not in EVENT_KINDS or not valid_date(raw.get("event_date"), event_kind):
        raise ValueError("invalid event_date/event_date_kind")
    for field in ("paper_url", "code_url", "project_url", "post_url", "related_project_url"):
        if raw.get(field) is not None:
            raw[field] = sanitize_url(raw[field])
    if raw.get("post_url") and not exact_post_url(raw["post_url"]):
        raise ValueError("post_url must identify a specific post")
    category = raw.get("proposed_category")
    if category and category not in taxonomy and not raw.get("taxonomy_change_requested"):
        raise ValueError("unknown category requires taxonomy_change_requested=true")
    return primary, key, raw


def snapshot_for(raw: dict, primary: str, kind: str) -> dict:
    source = dict(raw, primary_url=primary, candidate_kind=kind)
    return {field: source.get(field) for field in SNAPSHOT_FIELDS}


def fingerprint(snapshot: dict) -> str:
    return sha256_bytes(json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def version_candidate_id(key: str, fp: str) -> str:
    return "C-" + sha256_bytes((key + "\0" + fp).encode())[:16].upper()


def observation_fingerprint(base_fp: str, evidence_key: str, evidence_hash: object) -> str:
    """Identify a version by facts plus stable source evidence when present."""
    if evidence_hash is None:
        return base_fp
    return sha256_bytes((base_fp + "\0" + evidence_key + "\0" + str(evidence_hash)).encode())


def changed_fields(old: dict, new: dict) -> list[str]:
    return [field for field in SNAPSHOT_FIELDS if old.get(field) != new.get(field)]


def normalize_item(raw: dict, now: str, official: dict[str, str], state: dict, taxonomy: dict) -> tuple[dict | None, dict]:
    primary, raw_key, raw = validate_candidate_input(copy.deepcopy(raw), taxonomy)
    discovery = raw.get("_discovery", {})
    alias_urls = [primary, *discovery.get("aliases", [])]
    alias_keys = []
    for value in alias_urls:
        try:
            alias_keys.append(canonical_key(value))
        except (TypeError, ValueError):
            continue
    resolved = {state.get("aliases", {}).get(alias) for alias in alias_keys if state.get("aliases", {}).get(alias)}
    if len(resolved) > 1:
        raise ValueError("redirect aliases resolve to conflicting identities")
    key = next(iter(resolved), raw_key)
    kind = raw.get("candidate_kind", "post" if raw_key.startswith("social:") else "project")
    snapshot = snapshot_for(raw, primary, kind)
    identity = copy.deepcopy(state.get("identities", {}).get(key, {"first_seen": now, "last_seen_at": now, "versions": [], "evidence": {}}))
    identity.setdefault("evidence", {})
    prior = identity["versions"][-1] if identity.get("versions") else None
    if prior and resolved:
        snapshot["primary_url"] = prior.get("snapshot", {}).get("primary_url", snapshot["primary_url"])
        primary = snapshot["primary_url"]
    base_fp = fingerprint(snapshot)
    evidence_source = discovery.get("source_url") or primary
    try:
        evidence_key = canonical_key(evidence_source)
    except (TypeError, ValueError):
        evidence_key = "source:" + sha256_bytes(str(evidence_source).encode())[:16]
    evidence_hash = discovery.get("content_hash")
    previous_evidence = identity["evidence"].get(evidence_key)
    evidence_changed = bool(previous_evidence and evidence_hash and previous_evidence.get("content_hash") != evidence_hash)
    facts_changed = bool(prior and fingerprint(prior.get("snapshot", {})) != base_fp)
    historical = prior if prior and not facts_changed and not evidence_changed else None
    fp = observation_fingerprint(base_fp, evidence_key, evidence_hash)
    if historical is None:
        historical = next((version for version in identity.get("versions", [])
                           if version.get("content_fingerprint") == fp
                           or (evidence_hash is not None and fingerprint(version.get("snapshot", {})) == base_fp
                               and version.get("evidence_key") == evidence_key and version.get("evidence_hash") == evidence_hash)), None)
    if historical is not None:
        identity["last_seen_at"] = now
        identity["last_seen_version_id"] = historical["candidate_id"]
        historical["last_seen_at"] = now
        identity["evidence"][evidence_key] = {"content_hash": evidence_hash, "last_seen_at": now, "candidate_id": historical["candidate_id"]}
        if prior is not historical:
            identity.setdefault("reappearances", []).append({"candidate_id": historical["candidate_id"], "observed_at": now,
                                                              "previous_latest_candidate_id": prior["candidate_id"] if prior else None,
                                                              "evidence_key": evidence_key, "evidence_hash": evidence_hash})
        return None, {"key": key, "identity": identity, "alias_keys": alias_keys,
                      "unchanged_candidate_id": historical["candidate_id"], "evidence_candidate_id": historical["candidate_id"]}
    cid = version_candidate_id(key, fp)
    duplicate_id = next((version for version in identity.get("versions", []) if version.get("candidate_id") == cid), None)
    if duplicate_id is not None:
        raise ValueError("candidate_id collision or duplicate historical version")
    duplicate_of = official.get(key) or next((official.get(alias) for alias in alias_keys if official.get(alias)), None)
    update_of = prior["candidate_id"] if prior else None
    related_decision = prior.get("decision") if prior else None
    related_project = raw.get("related_project_url")
    if related_project:
        related_key = canonical_key(related_project)
        related_identity = state.get("identities", {}).get(related_key)
        update_of = official.get(related_key) or (related_identity.get("versions", [])[-1]["candidate_id"] if related_identity and related_identity.get("versions") else None)
    status = "needs_user_media" if kind == "post" else "needs_evidence"
    if duplicate_of:
        status = "possible_duplicate"
    if update_of:
        status = "possible_update"
    elif raw.get("status") in AUTO_STATUSES:
        status = raw["status"]
    if not update_of and not duplicate_of and raw.get("ready_for_review") and raw.get("relation_facts") and raw.get("event_date_basis"):
        status = "ready_for_review"
    category = raw.get("proposed_category")
    changes = changed_fields(prior.get("snapshot", {}), snapshot) if prior else []
    if evidence_changed:
        changes.append(f"evidence_content:{evidence_key}")
    candidate = {
        "candidate_id": cid, "candidate_kind": kind, "canonical_key": key, "content_fingerprint": fp,
        "discovered_at": now, "last_seen_at": now, "status": status,
        "title_zh_draft": raw.get("title_zh_draft", raw.get("title", "待核实候选")),
        "title_en_draft": raw.get("title_en_draft", raw.get("title", "Candidate requiring verification")),
        "summary_zh_draft": raw.get("summary_zh_draft", "机器草案：待人工核验。"),
        "summary_en_draft": raw.get("summary_en_draft", "Machine draft: pending human verification."),
        "draft_notice": "machine_generated_not_source_text", "primary_url": primary,
        "paper_url": raw.get("paper_url"), "code_url": raw.get("code_url"), "project_url": raw.get("project_url"),
        "post_url": primary if kind == "post" else raw.get("post_url"), "authors": raw.get("authors", []),
        "proposed_section": raw.get("proposed_section", "watchlist"), "proposed_category": category,
        "proposed_environment": raw.get("proposed_environment", "unknown"), "proposed_scene_tags": raw.get("proposed_scene_tags", []),
        "derived_workflow_tags": taxonomy.get(category, []), "proposed_gpt6_relation": raw.get("proposed_gpt6_relation", "discovery_only"),
        "proposed_evidence_level": raw.get("proposed_evidence_level", "D"), "event_date": raw.get("event_date"),
        "event_date_kind": raw.get("event_date_kind", "unknown"), "event_date_basis": raw.get("event_date_basis"),
        "event_timezone": raw.get("event_timezone"), "event_timestamp_raw": raw.get("event_timestamp_raw"),
        "event_date_parse_method": raw.get("event_date_parse_method"), "license_status": raw.get("license_status", "unknown"),
        "control_interface": raw.get("control_interface", "unknown"), "metrics": raw.get("metrics", []),
        "limitations": raw.get("limitations", ["候选尚未经人工审核。"]), "relation_facts": raw.get("relation_facts", []),
        "relevance_tier": raw.get("relevance_tier", "weak_lead"), "relevance_inference": raw.get("relevance_inference", "可能相关，需原始证据确认。"),
        "inference_confidence": raw.get("inference_confidence", "low"), "unresolved_questions": raw.get("unresolved_questions", []),
        "evidence_ids": [], "media_candidate_ids": raw.get("media_candidate_ids", []), "duplicate_of": duplicate_of,
        "update_of": update_of, "related_decision": related_decision, "changed_fields": changes,
        "taxonomy_change_requested": bool(raw.get("taxonomy_change_requested")), "reviewer_notes": raw.get("reviewer_notes", ""),
    }
    version = {"candidate_id": cid, "content_fingerprint": fp, "snapshot": snapshot, "first_seen": now, "last_seen_at": now,
               "status": status, "decision": None, "evidence_key": evidence_key, "evidence_hash": evidence_hash}
    identity.setdefault("versions", []).append(version)
    identity["evidence"][evidence_key] = {"content_hash": evidence_hash, "last_seen_at": now, "candidate_id": cid}
    identity["last_seen_at"] = now
    identity["last_seen_version_id"] = cid
    identity["formal_id"] = duplicate_of or identity.get("formal_id")
    return candidate, {"key": key, "identity": identity, "alias_keys": alias_keys,
                       "unchanged_candidate_id": None, "evidence_candidate_id": cid}


def apply_observation(state: dict, observation: dict) -> None:
    state["identities"][observation["key"]] = observation["identity"]
    for alias in observation.get("alias_keys", []):
        state.setdefault("aliases", {})[alias] = observation["key"]


def load_decisions(paths: list[Path], state: dict, baseline: str) -> list[dict]:
    loaded = []
    versions = {}
    for key, identity in state.get("identities", {}).items():
        for version in identity.get("versions", []):
            versions[version["candidate_id"]] = (key, version)
    existing = {(row["candidate_id"], row["decided_at"], row["decision"]) for row in state.get("decisions", [])}
    for path in paths:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            missing = {"candidate_id", "decision", "reviewer", "decided_at", "reason"} - set(row)
            if missing or row.get("decision") not in FINAL_STATUSES or row.get("candidate_id") not in versions:
                raise ValueError(f"{path}:{line_number}: invalid human decision")
            parse_time(row["decided_at"])
            accepted, rejected = row.get("accepted_fields", []), row.get("rejected_fields", [])
            if not isinstance(accepted, list) or not isinstance(rejected, list) or any(not isinstance(field, str) for field in accepted + rejected):
                raise ValueError(f"{path}:{line_number}: accepted_fields/rejected_fields must be string arrays")
            if set(accepted) & set(rejected):
                raise ValueError(f"{path}:{line_number}: accepted_fields and rejected_fields conflict")
            if not set(accepted + rejected).issubset(SNAPSHOT_FIELDS):
                raise ValueError(f"{path}:{line_number}: decision references an unknown candidate field")
            normalized = {**row, "accepted_fields": accepted, "rejected_fields": rejected, "media_decision": row.get("media_decision"), "formal_id": row.get("formal_id"), "baseline_sha": row.get("baseline_sha", baseline)}
            event_key = (normalized["candidate_id"], normalized["decided_at"], normalized["decision"])
            if event_key in existing:
                continue
            key, version = versions[normalized["candidate_id"]]
            version["decision"] = normalized
            state["identities"][key]["last_decision"] = normalized
            state.setdefault("decisions", []).append(normalized)
            existing.add(event_key)
            loaded.append(normalized)
    return loaded


def evidence_failure(run_id: str, index: int, adapter_key: str, failure: dict, now: str) -> dict:
    return {"evidence_id": f"E-{run_id}-{index:04d}", "candidate_id": None, "adapter_key": adapter_key,
            "source_url": redacted_url(failure.get("source_url")), "canonical_url": None, "source_kind": "secondary",
            "access": "linked_only", "fetched_at": now, "http_status": failure.get("http_status"),
            "parse_status": "failed", "final_url": redacted_url(failure.get("final_url")), "aliases": [],
            "content_hash": None, "extractor_version": VERSION, "fact_summary": [], "date_evidence": None,
            "media_entries": [], "license_note": "unknown", "failure_reason": failure["reason"]}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    atomic_text(path, "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows))


def candidate_versions(state: dict) -> dict[str, dict]:
    result = {}
    for identity in state.get("identities", {}).values():
        for version in identity.get("versions", []):
            existing = result.get(version["candidate_id"])
            if existing is None or (not existing.get("decision") and version.get("decision")):
                result[version["candidate_id"]] = version
    return result


def build_change_plans(decisions: list[dict], state: dict) -> list[dict]:
    versions = candidate_versions(state)
    metadata = json.loads((ROOT / "data/metadata.json").read_text(encoding="utf-8"))
    projects = json.loads((ROOT / "data/projects.json").read_text(encoding="utf-8"))
    start, end = date.fromisoformat(metadata["window_start"]), date.fromisoformat(metadata["window_end"])
    plans = []
    for decision in decisions:
        if decision["decision"] != "approved":
            continue
        version = versions[decision["candidate_id"]]
        snapshot = version["snapshot"]
        accepted = decision.get("accepted_fields", [])
        rejected = decision.get("rejected_fields", [])
        if set(accepted) & set(rejected):
            raise ValueError("accepted_fields and rejected_fields conflict")
        adopted = {key: snapshot.get(key) for key in accepted if key in snapshot}
        gaps = [field for field in ("title_zh_draft", "title_en_draft", "summary_zh_draft", "summary_en_draft") if not snapshot.get(field)]
        evidence_keys = sorted(state_identity_evidence(state, decision["candidate_id"]))
        date_approved = {"event_date", "event_date_basis"}.issubset(accepted) and bool(snapshot.get("event_date_basis")) and bool(evidence_keys)
        event = snapshot.get("event_date") if date_approved else None
        event_day = date.fromisoformat(event) if date_approved and snapshot.get("event_date_kind") == "exact_day" and event else None
        proposed_end = max(end, event_day) if event_day else end
        proposed_start = proposed_end - (end - start)
        migration = []
        if (proposed_start, proposed_end) != (start, end):
            for project in projects:
                project_event = project.get("event_date")
                if project.get("window_status") in {"in_window", "updated_in_window"} and isinstance(project_event, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", project_event):
                    day = date.fromisoformat(project_event)
                    if not proposed_start <= day <= proposed_end:
                        migration.append({"formal_id": project["id"], "current_window_status": project["window_status"], "required_action": "re-evaluate; likely outside_window"})
        plans.append({"candidate_id": decision["candidate_id"], "decision": "approved", "proposal_only": True,
            "formal_id_assigned": False, "baseline_sha": decision.get("baseline_sha"), "adopted_fields": adopted,
            "evidence_review": {"required": True, "candidate_evidence_keys": evidence_keys},
            "bilingual_gaps": gaps, "date_window_proposal": {"current": {"window_start": str(start), "window_end": str(end), "snapshot_date": metadata["snapshot_date"]},
                "proposed": {"window_start": str(proposed_start), "window_end": str(proposed_end), "snapshot_date": str(max(date.fromisoformat(metadata["snapshot_date"]), event_day)) if event_day else metadata["snapshot_date"]},
                "window_status_migration_review": migration, "status": "proposed" if event_day else "pending_unapproved_or_unverified_date",
                "note": "Date migration requires explicitly accepted event_date and event_date_basis; keep the formal window length."},
            "files_to_update_after_separate_human_authorization": ["data/projects.json", "data/sources.json", "data/i18n.json", "data/media.json", "data/publication_dates.json", "data/metadata.json", "docs generated from data", "tests"],
            "not_applied": ["No formal data was changed", "No formal ID was allocated", "No commit, push, deployment, or publication occurred"]})
    return plans


def state_identity_evidence(state: dict, candidate_id: str) -> list[str]:
    for key, identity in state.get("identities", {}).items():
        if any(row["candidate_id"] == candidate_id for row in identity.get("versions", [])):
            return list(identity.get("evidence", {}).keys())
    return []


def existing_formal_social_assets() -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    media = json.loads((ROOT / "data/media.json").read_text(encoding="utf-8"))
    def visit(value: object) -> None:
        if isinstance(value, dict):
            for child in value.values(): visit(child)
        elif isinstance(value, list):
            for child in value: visit(child)
        elif isinstance(value, str) and value.startswith("assets/social/"):
            path = ROOT / "site" / unquote(value)
            result[value] = sha256_file(path) if path.is_file() else None
    visit(media)
    social = ROOT / "site/assets/social"
    if social.exists():
        for path in social.iterdir():
            if path.is_file():
                result.setdefault("assets/social/" + quote(path.name, safe=""), sha256_file(path))
    return result


def load_user_media(paths: list[Path], state: dict) -> list[dict]:
    known = candidate_versions(state)
    records = []
    for mapping in paths:
        with mapping.open(encoding="utf-8", newline="") as handle:
            for line, row in enumerate(csv.DictReader(handle), 2):
                candidate_id = row.get("candidate_id", "")
                source = Path(row.get("user_supplied_path", ""))
                if candidate_id not in known or not source.is_file():
                    raise ValueError(f"{mapping}:{line}: unknown candidate or missing media file")
                original = row.get("original_filename") or source.name
                if original != source.name or original in {"", ".", ".."} or Path(original).name != original or any(ord(char) < 32 for char in original):
                    raise ValueError(f"{mapping}:{line}: original_filename must exactly match the supplied basename")
                if known[candidate_id]["snapshot"].get("candidate_kind") != "post":
                    raise ValueError(f"{mapping}:{line}: media may only map to a post candidate")
                digest = sha256_file(source)
                relative = f"media-staging/{candidate_id}/{digest[:12]}/{original}"
                proposed = "assets/social/" + quote(original, safe="")
                records.append({"candidate_id": candidate_id, "post_url": known[candidate_id]["snapshot"].get("post_url") or known[candidate_id]["snapshot"].get("primary_url"),
                    "source": source.resolve(), "original_filename": original, "sha256": digest, "package_relative_path": relative,
                    "suggested_site_path": proposed, "mapping_status": "verified", "notes": "original filename is compatible with the formal single-file path contract"})
    by_suggestion: dict[str, list[dict]] = {}
    for record in records:
        by_suggestion.setdefault(record["suggested_site_path"], []).append(record)
    formal = existing_formal_social_assets()
    for suggestion, grouped in by_suggestion.items():
        hashes = {record["sha256"] for record in grouped}
        formal_hash = formal.get(suggestion)
        conflict = len(hashes) > 1 or (suggestion in formal and formal_hash not in hashes)
        for record in grouped:
            if conflict:
                record["suggested_site_path"] = ""
                record["mapping_status"] = "needs_manual_path_resolution"
                record["notes"] = "original preserved; formal assets/social filename conflicts and requires a human decision"
            elif suggestion in formal:
                record["mapping_status"] = "verified_existing_same_content"
                record["notes"] = "original preserved; identical content already exists at the formal single-file path"
    return records


def write_review_files(directory: Path, candidates: list[dict], evidence: list[dict], decisions: list[dict], run: dict,
                       state: dict, media_records: list[dict]) -> None:
    write_jsonl(directory / "candidates.jsonl", candidates)
    write_jsonl(directory / "evidence.jsonl", evidence)
    write_jsonl(directory / "decisions.jsonl", decisions)
    posts = [candidate for candidate in candidates if candidate["candidate_kind"] == "post"]
    lines = ["# Post download list", "", "> User action only. The collector did not download post media.", ""]
    for candidate in posts:
        lines.extend([f"## {candidate['candidate_id']} — {candidate['title_en_draft']}", "", f"- Platform/post: {candidate['post_url']}", "- Media: unknown until manually inspected", "- Download status: not_downloaded", "- Note: retain the user-supplied original filename", ""])
    atomic_text(directory / "post-download-list.md", "\n".join(lines) + "\n")
    csv_path = directory / "media-name-map.csv"
    temporary = csv_path.with_name(f".{csv_path.name}.{uuid.uuid4().hex}.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "post_url", "suggested_role", "original_filename", "user_supplied_path", "sha256", "suggested_site_path", "mapping_status", "notes"])
        writer.writeheader()
        for candidate in posts:
            records = [row for row in media_records if row["candidate_id"] == candidate["candidate_id"]]
            if not records:
                writer.writerow({"candidate_id": candidate["candidate_id"], "post_url": candidate["post_url"], "suggested_role": "review_media",
                    "mapping_status": "awaiting_user_file", "notes": "keep original filename"})
            for record in records:
                writer.writerow({"candidate_id": candidate["candidate_id"], "post_url": candidate["post_url"], "suggested_role": "review_media",
                    "original_filename": record["original_filename"], "user_supplied_path": record["package_relative_path"],
                    "sha256": record["sha256"], "suggested_site_path": record["suggested_site_path"],
                    "mapping_status": record["mapping_status"], "notes": record["notes"]})
        for record in media_records:
            if not any(candidate["candidate_id"] == record["candidate_id"] for candidate in posts):
                writer.writerow({"candidate_id": record["candidate_id"], "post_url": record["post_url"], "suggested_role": "review_media",
                    "original_filename": record["original_filename"], "user_supplied_path": record["package_relative_path"], "sha256": record["sha256"],
                    "suggested_site_path": record["suggested_site_path"], "mapping_status": record["mapping_status"], "notes": record["notes"]})
    os.replace(temporary, csv_path)
    (directory / "media-staging").mkdir(exist_ok=True)
    atomic_text(directory / "media-staging/.keep", "User-supplied originals are staged here; do not rename them.\n")
    for record in media_records:
        target = directory / record["package_relative_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and sha256_file(target) != record["sha256"]:
            raise RuntimeError("media package path collision with different content")
        if not target.exists():
            shutil.copy2(record["source"], target)
        if sha256_file(target) != record["sha256"]:
            raise RuntimeError("media hash mismatch after package copy")
    change_plans = build_change_plans(decisions, state)
    write_jsonl(directory / "change-plans.jsonl", change_plans)
    plan_lines = ["# Approved candidate change plans", "", "> Proposal only: no formal file change, ID allocation, commit, deployment, or publication.", ""]
    for plan in change_plans:
        plan_lines.extend([f"## {plan['candidate_id']}", "", f"- Adopted fields: {', '.join(plan['adopted_fields']) or 'none'}", f"- Bilingual gaps: {', '.join(plan['bilingual_gaps']) or 'none'}",
            f"- Proposed formal window: {plan['date_window_proposal']['proposed']['window_start']} → {plan['date_window_proposal']['proposed']['window_end']}",
            f"- Existing window_status records needing migration review: {len(plan['date_window_proposal']['window_status_migration_review'])}",
            f"- Files/tests to update: {', '.join(plan['files_to_update_after_separate_human_authorization'])}", ""])
    if not change_plans: plan_lines.append("- No newly supplied approved decision.\n")
    atomic_text(directory / "change-plan.md", "\n".join(plan_lines) + "\n")
    sections = [("New", "new"), ("Ready for review", "ready_for_review"), ("Possible updates", "possible_update"), ("Possible duplicates", "possible_duplicate"), ("Needs evidence", "needs_evidence"), ("Needs user media", "needs_user_media")]
    report = ["# Daily discovery review", "", f"Run: `{run['run_id']}`  ", f"Baseline: `{run['baseline_sha']}`", "", "Local review output only; not deployed or published.", ""]
    for heading, status in sections:
        report.extend([f"## {heading}", ""])
        chosen = [candidate for candidate in candidates if candidate["status"] == status]
        report.extend([f"- [{item['candidate_id']}]({item['primary_url']}) — {item['title_en_draft']} ({', '.join(item['changed_fields']) or 'initial version'})" for item in chosen] or ["- None"])
        report.append("")
    report.extend(["## Adapter results", ""])
    for key, item in run["adapter_runs"].items():
        report.append(f"- `{key}`: {item['status']}; window `{item['lower_bound']}` → `{item['upper_bound']}`; failures={item['failure_count']}")
    report.extend(["", "## Collection failures", ""])
    failures = [item for item in evidence if item.get("failure_reason")]
    report.extend([f"- `{item['adapter_key']}` / `{item['evidence_id']}`: {item['failure_reason']}" for item in failures] or ["- None"])
    atomic_text(directory / "report.md", "\n".join(report) + "\n")


def build_manifest(directory: Path) -> None:
    rows = [f"{sha256_file(path)}  {path.relative_to(directory).as_posix()}" for path in sorted(directory.rglob("*")) if path.is_file() and path.name != "SHA256SUMS"]
    atomic_text(directory / "SHA256SUMS", "\n".join(rows) + "\n")


def resume_commit(checkpoint_path: Path, state_path: Path, writer=atomic_json) -> tuple[Path, int]:
    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    phase = checkpoint["phase"]
    temporary = Path(checkpoint["temporary_dir"])
    final = Path(checkpoint["final_dir"])
    if phase == "package_ready":
        if final.exists() and not temporary.exists():
            pass
        elif temporary.exists() and not final.exists():
            final.parent.mkdir(parents=True, exist_ok=True)
            os.replace(temporary, final)
        else:
            raise RuntimeError("recovery cannot determine a unique package directory")
        checkpoint["phase"] = "package_published"
        writer(checkpoint_path, checkpoint)
    if checkpoint["phase"] == "package_published":
        current = load_state(state_path)
        run_id = checkpoint["run_id"]
        if run_id in current.get("committed_runs", {}):
            checkpoint["phase"] = "state_committed"
            checkpoint["committed_revision"] = current["committed_runs"][run_id]["revision"]
            writer(checkpoint_path, checkpoint)
            return final, int(checkpoint.get("exit_code", 0))
        base_revision = int(checkpoint["base_revision"])
        if current.get("revision", 0) != base_revision:
            checkpoint["phase"] = "stale_conflict"
            checkpoint["conflict_revision"] = current.get("revision", 0)
            writer(checkpoint_path, checkpoint)
            raise RuntimeError(f"stale transaction base revision {base_revision}; current revision is {current.get('revision', 0)}")
        pending = checkpoint["pending_state"]
        if pending.get("revision") != base_revision + 1:
            raise RuntimeError("pending state revision is inconsistent")
        writer(state_path, pending)
        checkpoint["phase"] = "state_committed"
        checkpoint["committed_revision"] = pending["revision"]
        writer(checkpoint_path, checkpoint)
    if checkpoint["phase"] != "state_committed":
        raise RuntimeError(f"run is not commit-ready (phase={checkpoint['phase']})")
    return final, int(checkpoint.get("exit_code", 0))


def _interrupt(_signum: int, _frame: object) -> None:
    global INTERRUPTED
    INTERRUPTED = True


def close_return(handle, code: int) -> int:
    handle.close()
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--network", action="store_true")
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--response-fixture", type=Path, help="offline public API response manifest")
    parser.add_argument("--config", type=Path, default=ROOT / "config/daily_review.json")
    parser.add_argument("--output-root", type=Path, default=ROOT / "downloads/daily-review")
    parser.add_argument("--state-root", type=Path, default=ROOT / "downloads/daily-review-state")
    parser.add_argument("--from", dest="lower")
    parser.add_argument("--to", dest="upper")
    parser.add_argument("--resume-run")
    parser.add_argument("--forced-run-id", help=argparse.SUPPRESS)
    parser.add_argument("--adapter", action="append", choices=("fixture", "seed", "arxiv", "github", "feed"))
    parser.add_argument("--decisions", action="append", type=Path, default=[])
    parser.add_argument("--user-media-map", action="append", type=Path, default=[], help="CSV mapping candidate_id to a user-supplied original file")
    args = parser.parse_args(argv)
    if not (args.once or args.dry_run or args.resume_run):
        parser.error("choose --once, --dry-run, or --resume-run")
    try:
        output_root, state_root = managed_path(args.output_root), managed_path(args.state_root)
        if args.resume_run:
            validate_run_id(args.resume_run)
    except ValueError as exc:
        parser.error(str(exc))
    output_root.mkdir(parents=True, exist_ok=True)
    state_root.mkdir(parents=True, exist_ok=True)
    lock_handle = (state_root / "collector.lock").open("a+")
    try:
        fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("skipped_locked", file=sys.stderr)
        return close_return(lock_handle, 75)
    state_path = state_root / "state.json"
    if args.resume_run:
        checkpoint_path = state_root / "runs" / f"{args.resume_run}.json"
        try:
            checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
            if checkpoint.get("phase") in {"collecting", "restart_pending"}:
                resume_args = checkpoint.get("resume_args")
                if not isinstance(resume_args, list):
                    raise RuntimeError("collecting checkpoint lacks restart arguments")
                temporary = Path(checkpoint["temporary_dir"])
                temporary.resolve().relative_to(output_root)
                Path(checkpoint["final_dir"]).resolve().relative_to(output_root)
                if temporary.exists():
                    abandoned = state_root / "abandoned" / f"{args.resume_run}-{uuid.uuid4().hex[:8]}"
                    abandoned.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(temporary, abandoned)
                    checkpoint["abandoned_partial"] = str(abandoned)
                checkpoint["phase"] = "restart_pending"
                atomic_json(checkpoint_path, checkpoint)
                lock_handle.close()
                return main([*resume_args, "--forced-run-id", args.resume_run])
            Path(checkpoint["temporary_dir"]).resolve().relative_to(output_root)
            Path(checkpoint["final_dir"]).resolve().relative_to(output_root)
            final, exit_code = resume_commit(checkpoint_path, state_path)
        except Exception as exc:
            print(f"resume_failed:{exc}", file=sys.stderr)
            return close_return(lock_handle, 74)
        print(final)
        return close_return(lock_handle, exit_code)
    try:
        config = load_config(args.config)
        config_hash = sha256_file(args.config)
        config["_hash"] = config_hash
        state = load_state(state_path)
        plans = planned_adapters(config, args.fixture, set(args.adapter) if args.adapter else None)
        if not plans and not args.dry_run:
            raise ValueError("no configured adapter/query to run")
        prior_checkpoint_path = state_root / "runs" / f"{args.forced_run_id}.json" if args.forced_run_id else None
        prior_checkpoint = json.loads(prior_checkpoint_path.read_text(encoding="utf-8")) if prior_checkpoint_path and prior_checkpoint_path.exists() else None
        if args.forced_run_id:
            if not prior_checkpoint or prior_checkpoint.get("phase") != "restart_pending":
                raise RuntimeError("forced restart requires a restart_pending checkpoint")
            if prior_checkpoint.get("config_hash") != config_hash:
                raise RuntimeError("configuration changed since the interrupted run")
            upper = parse_time(prior_checkpoint["upper_bound"])
            windows = prior_checkpoint["windows"]
        else:
            unfinished = unfinished_checkpoints(state_root)
            if unfinished:
                details = ", ".join(f"{run}:{phase}" for run, phase in unfinished)
                raise RuntimeError(f"unfinished transaction must be resumed first: {details}")
            upper = parse_time(args.upper) if args.upper else utc_now()
            windows = {plan["adapter_key"]: adapter_window(plan["adapter_key"], state, upper, config, args.lower) for plan in plans}
        if any(parse_time(item["lower_bound"]) > parse_time(item["upper_bound"]) for item in windows.values()):
            raise ValueError("--from must not be after --to")
        if args.dry_run:
            print(json.dumps({"configured": config["persistence"]["configured"], "network": args.network, "adapter_windows": windows}, indent=2))
            return close_return(lock_handle, 0)
        before = formal_hashes()
        baseline = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], check=False, capture_output=True, text=True).stdout.strip() or "unknown"
        decisions = load_decisions(args.decisions, state, baseline)
        started = utc_now()
        run_id = validate_run_id(args.forced_run_id or (started.strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]))
        final_dir = Path(prior_checkpoint["final_dir"]) if prior_checkpoint else output_root / started.date().isoformat() / run_id
        temporary = Path(prior_checkpoint["temporary_dir"]) if prior_checkpoint else final_dir.with_name("." + run_id + ".tmp")
        if temporary.exists() or final_dir.exists():
            raise RuntimeError("run directory collision")
        temporary.mkdir(parents=True)
        checkpoint_path = state_root / "runs" / f"{run_id}.json"
        resume_args = ["--once", "--config", str(args.config), "--output-root", str(output_root), "--state-root", str(state_root)]
        for flag, value in (("--fixture", args.fixture), ("--response-fixture", args.response_fixture), ("--from", args.lower)):
            if value is not None:
                resume_args.extend([flag, str(value)])
        resume_args.extend(["--to", iso(upper)])
        if args.network:
            resume_args.append("--network")
        for adapter in args.adapter or []:
            resume_args.extend(["--adapter", adapter])
        for decision in args.decisions:
            resume_args.extend(["--decisions", str(decision)])
        for mapping in args.user_media_map:
            resume_args.extend(["--user-media-map", str(mapping)])
        checkpoint = {"run_id": run_id, "phase": "collecting", "temporary_dir": str(temporary), "final_dir": str(final_dir),
                      "started_at": prior_checkpoint.get("started_at", iso(started)) if prior_checkpoint else iso(started),
                      "resume_args": resume_args, "upper_bound": iso(upper), "windows": windows,
                      "config_hash": config_hash, "base_revision": state.get("revision", 0)}
        atomic_json(checkpoint_path, checkpoint)
        responses = load_response_fixture(args.response_fixture)
        working_state = copy.deepcopy(state)
        taxonomy = json.loads((ROOT / "data/tag_taxonomy.json").read_text(encoding="utf-8"))["category_tags"]
        official = official_index()
        candidates, evidence, adapter_runs = [], [], {}
        http_client = HttpClient(config["runtime"]["minimum_request_interval_seconds"])
        evidence_index = 0
        now = iso(started)
        for plan in plans:
            key = plan["adapter_key"]
            lower = parse_time(windows[key]["lower_bound"])
            adapter_upper = parse_time(windows[key]["upper_bound"])
            if INTERRUPTED:
                result = {"items": [], "failures": [{"reason": "interrupted", "source_url": None}], "complete": False, "pages_complete": False}
            elif plan["type"] == "fixture":
                result = fixture_adapter(plan)
            elif plan["type"] == "seed":
                result = seed_adapter(plan, config, args.network, http_client)
            elif plan["type"] == "arxiv":
                result = arxiv_adapter(plan, config, lower, adapter_upper, args.network, responses,
                                       int(windows[key].get("cursor", 0)), http_client)
            elif plan["type"] == "github_search":
                result = github_search_adapter(plan, config, lower, adapter_upper, args.network, responses, http_client)
            elif plan["type"] == "github_repo":
                result = github_repo_adapter(plan, config, lower, adapter_upper, args.network, responses, http_client)
            else:
                result = feed_adapter(plan, config, lower, adapter_upper, args.network, responses, http_client)
            validation_failures = 0
            validation_errors = []
            for failure in result.get("failures", []):
                evidence_index += 1
                evidence.append(evidence_failure(run_id, evidence_index, key, failure, now))
            for raw in result.get("items", []):
                if INTERRUPTED:
                    validation_failures += 1
                    evidence_index += 1
                    evidence.append(evidence_failure(run_id, evidence_index, key, {"reason": "interrupted", "source_url": raw.get("primary_url")}, now))
                    break
                try:
                    candidate, observation = normalize_item(raw, now, official, working_state, taxonomy)
                except (KeyError, TypeError, ValueError) as exc:
                    validation_failures += 1
                    validation_errors.append(f"candidate_validation:{exc}")
                    evidence_index += 1
                    evidence.append(evidence_failure(run_id, evidence_index, key, {"reason": f"candidate_validation:{exc}", "source_url": raw.get("primary_url") if isinstance(raw, dict) else None}, now))
                    continue
                apply_observation(working_state, observation)
                evidence_index += 1
                eid = f"E-{run_id}-{evidence_index:04d}"
                discovery = raw.get("_discovery", {})
                evidence.append({"evidence_id": eid, "candidate_id": observation["evidence_candidate_id"], "adapter_key": key,
                    "source_url": redacted_url(discovery.get("source_url") or raw.get("primary_url")), "canonical_url": sanitize_url(raw["primary_url"]),
                    "source_kind": raw.get("source_kind", "secondary"), "access": raw.get("access", "linked_only"), "fetched_at": now,
                    "http_status": discovery.get("http_status"), "parse_status": "parsed", "final_url": redacted_url(discovery.get("final_url")),
                    "aliases": [url for url in (redacted_url(value) for value in discovery.get("aliases", [])) if url],
                    "content_hash": discovery.get("content_hash"), "extractor_version": VERSION, "fact_summary": raw.get("relation_facts", []),
                    "date_evidence": raw.get("event_date_basis"), "media_entries": raw.get("media_entries", []),
                    "license_note": raw.get("license_status", "unknown"), "failure_reason": None})
                if candidate is not None:
                    candidate["evidence_ids"] = [eid]
                    candidates.append(candidate)
            failures = len(result.get("failures", [])) + validation_failures
            complete = bool(result.get("complete")) and failures == 0 and not INTERRUPTED
            adapter_runs[key] = {**windows[key], "status": "complete" if complete else ("interrupted" if INTERRUPTED else "failed"),
                                 "failure_count": failures, "pages_complete": bool(result.get("pages_complete")),
                                 "pages_fetched": result.get("pages_fetched"), "total_results": result.get("total_results"),
                                 "next_cursor": result.get("next_cursor"),
                                 "errors": [item.get("reason") for item in result.get("failures", [])] + validation_errors}
            working_state["adapters"][key] = {**working_state["adapters"].get(key, {}), "last_run": run_id,
                "last_status": adapter_runs[key]["status"], "error": adapter_runs[key]["errors"] or None,
                "cursor": result.get("next_cursor"),
                "config_hash": config_hash}
            if complete:
                working_state["adapters"][key].pop("pending_scan", None)
                old_bound = working_state["adapters"][key].get("last_successful_upper_bound")
                if not old_bound or parse_time(old_bound) < adapter_upper:
                    working_state["adapters"][key]["last_successful_upper_bound"] = iso(adapter_upper)
                    working_state["adapters"][key]["last_successful_run"] = run_id
            elif result.get("next_cursor") is not None:
                working_state["adapters"][key]["pending_scan"] = {"lower_bound": windows[key]["lower_bound"],
                    "upper_bound": windows[key]["upper_bound"], "next_cursor": result["next_cursor"], "config_hash": config_hash}
        failures = sum(item["failure_count"] for item in adapter_runs.values())
        incomplete = sum(item["status"] != "complete" for item in adapter_runs.values())
        status = "interrupted" if INTERRUPTED else ("partial_failure" if failures or incomplete else "complete")
        exit_code = 130 if INTERRUPTED else (2 if failures or incomplete else 0)
        run = {"run_id": run_id, "started_at": iso(started), "finished_at": iso(utc_now()), "baseline_sha": baseline,
               "collector_version": VERSION, "adapter_runs": adapter_runs, "config_hash": config_hash,
               "network_enabled": args.network, "configured": bool(config["persistence"]["configured"]), "persistence": config["persistence"],
               "candidate_count": len(candidates), "failure_count": failures, "status": status, "formal_hashes_before": before}
        media_records = load_user_media(args.user_media_map, working_state)
        write_review_files(temporary, candidates, evidence, decisions, run, working_state, media_records)
        after = formal_hashes()
        if before != after:
            raise RuntimeError("formal files changed during collection")
        run["formal_hashes_after"] = after
        run["formal_files_unchanged"] = True
        atomic_json(temporary / "run.json", run)
        build_manifest(temporary)
        working_state["revision"] = state.get("revision", 0) + 1
        working_state.setdefault("committed_runs", {})[run_id] = {"revision": working_state["revision"], "status": status,
            "package": str(final_dir), "committed_at": iso(utc_now())}
        checkpoint.update({"phase": "package_ready", "pending_state": working_state, "exit_code": exit_code, "run_status": status})
        atomic_json(checkpoint_path, checkpoint)
        try:
            final, committed_exit = resume_commit(checkpoint_path, state_path)
        except Exception as exc:
            print(f"commit_failed:{exc}; resume with --resume-run {run_id}", file=sys.stderr)
            return close_return(lock_handle, 74)
        print(final)
        return close_return(lock_handle, committed_exit)
    except Exception as exc:
        print(f"daily_review_failed:{type(exc).__name__}:{exc}", file=sys.stderr)
        return close_return(lock_handle, 1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, _interrupt)
    signal.signal(signal.SIGTERM, _interrupt)
    raise SystemExit(main())
