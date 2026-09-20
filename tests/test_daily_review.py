"""Offline regression tests for discovery, state, and review transactions."""
from __future__ import annotations

import copy
import contextlib
import csv
import fcntl
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("daily_review", ROOT / "scripts/daily_review.py")
daily_review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(daily_review)
FIXTURE = ROOT / "tests/fixtures/daily_review_items.json"
RESPONSES = ROOT / "tests/fixtures/arxiv_responses.json"
DISCOVERY_RESPONSES = ROOT / "tests/fixtures/discovery_responses.json"
CONFIG = ROOT / "config/daily_review.json"


class DailyReviewTests(unittest.TestCase):
    def setUp(self):
        self.runtime = ROOT / "downloads" / ("test-daily-review-" + uuid.uuid4().hex)
        self.output = self.runtime / "review"
        self.state = self.runtime / "state"

    def tearDown(self):
        daily_review.INTERRUPTED = False
        if self.runtime.exists():
            shutil.rmtree(self.runtime)

    def run_collector(self, fixture: Path = FIXTURE, *, extra: list[str] | None = None, config: Path = CONFIG):
        command = [sys.executable, str(ROOT / "scripts/daily_review.py"), "--once", "--fixture", str(fixture),
                   "--config", str(config), "--output-root", str(self.output), "--state-root", str(self.state),
                   "--from", "2026-09-01T00:00:00Z", "--to", "2026-09-20T00:00:00Z"]
        command.extend(extra or [])
        return subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True)

    @staticmethod
    def rows(path: Path) -> list[dict]:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]

    def write_fixture(self, value: object, name: str = "input.json") -> Path:
        self.runtime.mkdir(parents=True, exist_ok=True)
        path = self.runtime / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def test_url_identity_and_input_contract(self):
        self.assertEqual(daily_review.canonical_key("https://arxiv.org/abs/2609.12345v1"), daily_review.canonical_key("https://arxiv.org/pdf/2609.12345v2.pdf"))
        self.assertEqual(daily_review.canonical_key("https://arxiv.org/abs/hep-th/9901001v1"), daily_review.canonical_key("https://arxiv.org/pdf/hep-th/9901001v3.pdf"))
        self.assertEqual(daily_review.canonical_key("https://x.com/name/status/123?ref=x"), "social:x:123")
        self.assertEqual(daily_review.sanitize_url("https://Example.com/Case/Path?view=1&utm_source=x#frag"), "https://example.com/Case/Path?view=1")
        self.assertNotIn("token", daily_review.sanitize_url("https://example.com/a?token=secret&view=1"))
        taxonomy = {"evaluation": ["evaluation"]}
        with self.assertRaisesRegex(ValueError, "specific"):
            daily_review.validate_candidate_input({"primary_url": "https://x.com/demo", "candidate_kind": "post"}, taxonomy)
        with self.assertRaisesRegex(ValueError, "invalid source_kind"):
            daily_review.validate_candidate_input({"primary_url": "https://example.com/a", "source_kind": "invented"}, taxonomy)
        with self.assertRaisesRegex(ValueError, "event_date"):
            daily_review.validate_candidate_input({"primary_url": "https://example.com/a", "event_date": "2026-02-30", "event_date_kind": "exact_day"}, taxonomy)

    def test_success_package_second_scan_does_not_requeue_and_ready_is_reported(self):
        before = daily_review.formal_hashes()
        first = self.run_collector()
        self.assertEqual(first.returncode, 0, first.stderr)
        first_package = Path(first.stdout.strip())
        self.assertEqual(len(self.rows(first_package / "candidates.jsonl")), 2)
        report = (first_package / "report.md").read_text(encoding="utf-8")
        self.assertIn("## Ready for review", report)
        self.assertIn("GPT-6 Robot Demo", report)
        second = self.run_collector()
        self.assertEqual(second.returncode, 0, second.stderr)
        second_package = Path(second.stdout.strip())
        self.assertEqual(self.rows(second_package / "candidates.jsonl"), [])
        self.assertEqual(len(self.rows(second_package / "evidence.jsonl")), 2)
        state = json.loads((self.state / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["adapters"]["fixture"]["last_successful_upper_bound"], "2026-09-20T00:00:00Z")
        self.assertEqual(daily_review.formal_hashes(), before)

    def test_failure_is_partial_and_does_not_advance_watermark(self):
        bad = self.write_fixture([{"primary_url": "http://example.com"}])
        result = self.run_collector(bad)
        self.assertEqual(result.returncode, 2, result.stderr)
        package = Path(result.stdout.strip())
        run = json.loads((package / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(run["status"], "partial_failure")
        self.assertEqual(run["adapter_runs"]["fixture"]["status"], "failed")
        state = json.loads((self.state / "state.json").read_text(encoding="utf-8"))
        self.assertNotIn("last_successful_upper_bound", state["adapters"]["fixture"])

    def test_same_batch_deduplicates(self):
        source = json.loads(FIXTURE.read_text(encoding="utf-8"))[0]
        fixture = self.write_fixture([source, copy.deepcopy(source)])
        result = self.run_collector(fixture)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.rows(Path(result.stdout.strip()) / "candidates.jsonl")), 1)

    def test_changed_version_references_old_decision_without_self_reference(self):
        source = json.loads(FIXTURE.read_text(encoding="utf-8"))[0]
        first_fixture = self.write_fixture([source], "v1.json")
        first = self.run_collector(first_fixture)
        old = self.rows(Path(first.stdout.strip()) / "candidates.jsonl")[0]
        decision = self.runtime / "decision.jsonl"
        decision.write_text(json.dumps({"candidate_id": old["candidate_id"], "decision": "rejected", "reviewer": "human", "decided_at": "2026-09-20T01:00:00Z", "reason": "insufficient evidence"}) + "\n", encoding="utf-8")
        changed = copy.deepcopy(source)
        changed["title_en_draft"] = "GPT-6 Robot Demo — revised evidence"
        second_fixture = self.write_fixture([changed], "v2.json")
        second = self.run_collector(second_fixture, extra=["--decisions", str(decision)])
        self.assertEqual(second.returncode, 0, second.stderr)
        new = self.rows(Path(second.stdout.strip()) / "candidates.jsonl")[0]
        self.assertNotEqual(new["candidate_id"], old["candidate_id"])
        self.assertEqual(new["update_of"], old["candidate_id"])
        self.assertNotEqual(new["candidate_id"], new["update_of"])
        self.assertEqual(new["related_decision"]["decision"], "rejected")
        self.assertEqual(new["changed_fields"], ["title_en_draft"])
        state = json.loads((self.state / "state.json").read_text(encoding="utf-8"))
        versions = state["identities"]["github:example-lab/gpt6-robot-demo"]["versions"]
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0]["decision"]["decision"], "rejected")

    def test_historical_a_b_a_reappearance_reuses_original_version_and_decision(self):
        source = json.loads(FIXTURE.read_text(encoding="utf-8"))[0]
        for decision_name in ("rejected", "approved"):
            with self.subTest(decision=decision_name):
                state = daily_review.default_state()
                first, observation = daily_review.normalize_item(source, "2026-09-20T00:00:00Z", {}, state, {"closed_loop": []})
                daily_review.apply_observation(state, observation)
                state["identities"][first["canonical_key"]]["versions"][0]["decision"] = {"decision": decision_name, "reason": "human decision"}
                changed = copy.deepcopy(source)
                changed["title_en_draft"] = "B"
                second, observation = daily_review.normalize_item(changed, "2026-09-20T01:00:00Z", {}, state, {"closed_loop": []})
                daily_review.apply_observation(state, observation)
                repeated, observation = daily_review.normalize_item(source, "2026-09-20T02:00:00Z", {}, state, {"closed_loop": []})
                daily_review.apply_observation(state, observation)
                identity = state["identities"][first["canonical_key"]]
                self.assertIsNone(repeated)
                self.assertNotEqual(first["candidate_id"], second["candidate_id"])
                self.assertEqual(len(identity["versions"]), 2)
                self.assertEqual(identity["versions"][0]["decision"]["decision"], decision_name)
                self.assertEqual(identity["reappearances"][0]["candidate_id"], first["candidate_id"])
                self.assertEqual(observation["evidence_candidate_id"], first["candidate_id"])

    def test_evidence_hash_a_b_c_b_reuses_b_and_preserves_decision(self):
        for decision_name in ("rejected", "approved"):
            with self.subTest(decision=decision_name):
                state = daily_review.default_state()
                base = {"primary_url": "https://example.org/project", "candidate_kind": "project", "title": "Unchanged title",
                        "event_date": None, "event_date_kind": "unknown", "source_kind": "primary", "access": "page_text"}
                candidates = []
                for index, content_hash in enumerate(("A", "B", "C")):
                    raw = copy.deepcopy(base)
                    raw["_discovery"] = {"source_url": "https://example.org/project", "content_hash": content_hash}
                    candidate, observation = daily_review.normalize_item(raw, f"2026-09-20T0{index}:00:00Z", {}, state, {})
                    daily_review.apply_observation(state, observation)
                    candidates.append(candidate)
                candidates[1]["reviewer_notes"] = "decision target"
                identity = state["identities"]["url:https://example.org/project"]
                identity["versions"][1]["decision"] = {"decision": decision_name, "reason": "human evidence review"}
                repeated = copy.deepcopy(base)
                repeated["_discovery"] = {"source_url": "https://example.org/project", "content_hash": "B"}
                candidate, observation = daily_review.normalize_item(repeated, "2026-09-20T04:00:00Z", {}, state, {})
                daily_review.apply_observation(state, observation)
                identity = state["identities"]["url:https://example.org/project"]
                ids = [row["candidate_id"] for row in identity["versions"]]
                self.assertIsNone(candidate)
                self.assertEqual(len(ids), 3)
                self.assertEqual(len(ids), len(set(ids)))
                self.assertEqual(observation["evidence_candidate_id"], candidates[1]["candidate_id"])
                self.assertEqual(identity["versions"][1]["decision"]["decision"], decision_name)
                self.assertEqual(identity["reappearances"][-1]["evidence_hash"], "B")

    def test_candidate_id_collision_is_rejected_before_append(self):
        state = daily_review.default_state()
        raw = {"primary_url": "https://example.org/collision", "candidate_kind": "project", "title": "A", "event_date": None, "event_date_kind": "unknown"}
        first, observation = daily_review.normalize_item(raw, "2026-09-20T00:00:00Z", {}, state, {})
        daily_review.apply_observation(state, observation)
        changed = copy.deepcopy(raw)
        changed["title"] = "B"
        original = daily_review.version_candidate_id
        daily_review.version_candidate_id = lambda *_args: first["candidate_id"]
        try:
            with self.assertRaisesRegex(ValueError, "candidate_id collision"):
                daily_review.normalize_item(changed, "2026-09-20T01:00:00Z", {}, state, {})
        finally:
            daily_review.version_candidate_id = original

    def test_new_post_can_be_update_of_existing_formal_project(self):
        post = json.loads(FIXTURE.read_text(encoding="utf-8"))[1]
        post["related_project_url"] = "https://github.com/cheng-haha/GPT-Policy"
        fixture = self.write_fixture([post])
        result = self.run_collector(fixture)
        candidate = self.rows(Path(result.stdout.strip()) / "candidates.jsonl")[0]
        self.assertEqual(candidate["status"], "possible_update")
        self.assertEqual(candidate["update_of"], "P01")

    def arxiv_config(self) -> Path:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        config["sources"]["arxiv_queries"] = [{"name": "embodied", "query_template": "{model_terms} AND {embodied_terms}", "page_size": 1, "max_pages": 3}]
        return self.write_fixture(config, "config.json")

    def test_arxiv_api_fixture_pagination_filtering_and_provenance(self):
        config = self.arxiv_config()
        result = self.run_collector(extra=["--adapter", "arxiv", "--response-fixture", str(RESPONSES)], config=config)
        self.assertEqual(result.returncode, 0, result.stderr)
        package = Path(result.stdout.strip())
        adapter = json.loads((package / "run.json").read_text(encoding="utf-8"))["adapter_runs"]["arxiv:embodied"]
        self.assertTrue(adapter["pages_complete"])
        self.assertEqual(adapter["pages_fetched"], 2)
        self.assertEqual(len(self.rows(package / "candidates.jsonl")), 2)
        evidence = self.rows(package / "evidence.jsonl")
        self.assertTrue(all(row["source_url"].startswith("https://export.arxiv.org/api/query?") for row in evidence))
        self.assertTrue(all(row["canonical_url"].startswith("https://arxiv.org/abs/") for row in evidence))

    def test_incomplete_pagination_restarts_frozen_window_and_never_silently_advances(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        config["sources"]["arxiv_queries"] = [{"name": "embodied", "query_template": "{model_terms} AND {embodied_terms}", "page_size": 1, "max_pages": 1}]
        config_path = self.write_fixture(config, "paged-config.json")
        first = self.run_collector(extra=["--adapter", "arxiv", "--response-fixture", str(RESPONSES)], config=config_path)
        self.assertEqual(first.returncode, 2, first.stderr)
        first_run = json.loads((Path(first.stdout.strip()) / "run.json").read_text(encoding="utf-8"))
        adapter = first_run["adapter_runs"]["arxiv:embodied"]
        self.assertEqual((first_run["status"], first_run["failure_count"]), ("partial_failure", 1))
        self.assertEqual((adapter["pages_complete"], adapter["next_cursor"], adapter["errors"]), (False, 0, ["pagination_incomplete_unstable_offset_restart_required"]))
        state = json.loads((self.state / "state.json").read_text(encoding="utf-8"))
        pending = state["adapters"]["arxiv:embodied"]["pending_scan"]
        self.assertEqual((pending["lower_bound"], pending["upper_bound"], pending["next_cursor"]), ("2026-09-01T00:00:00Z", "2026-09-20T00:00:00Z", 0))
        second = self.run_collector(extra=["--adapter", "arxiv", "--response-fixture", str(RESPONSES)], config=config_path)
        self.assertEqual(second.returncode, 2, second.stderr)
        second_run = json.loads((Path(second.stdout.strip()) / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(second_run["adapter_runs"]["arxiv:embodied"]["lower_bound"], "2026-09-01T00:00:00Z")
        state = json.loads((self.state / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["adapters"]["arxiv:embodied"]["pending_scan"]["next_cursor"], 0)
        self.assertNotIn("last_successful_upper_bound", state["adapters"]["arxiv:embodied"])

    def test_arxiv_old_first_submission_updated_inside_window_is_discovered(self):
        config = self.arxiv_config()
        result = self.run_collector(extra=["--adapter", "arxiv", "--response-fixture", str(RESPONSES)], config=config)
        self.assertEqual(result.returncode, 0, result.stderr)
        package = Path(result.stdout.strip())
        rows = self.rows(package / "candidates.jsonl")
        old = next(row for row in rows if "hep-th/9901001" in row["primary_url"])
        self.assertEqual(old["event_date"], "2026-09-18")
        evidence = self.rows(package / "evidence.jsonl")
        self.assertTrue(all("submittedDate" not in row["source_url"] for row in evidence))

    def test_github_search_repo_updates_and_feed_exact_post_from_real_format_fixtures(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        config["sources"]["github_searches"] = [{"name": "public", "query_template": "{model_terms} {embodied_terms}", "page_size": 30, "max_pages": 2}]
        config["sources"]["github_repositories"] = [{"repo": "example/gpt6-robot"}]
        config["sources"]["feeds"] = [{"name": "official", "url": "https://project.example/feed.atom", "source_kind": "primary", "language": "en"}]
        config["adapters"]["feed"]["allowlist"] = ["project.example"]
        path = self.write_fixture(config, "discovery-config.json")
        result = self.run_collector(extra=["--adapter", "github", "--adapter", "feed", "--response-fixture", str(DISCOVERY_RESPONSES)], config=path)
        self.assertEqual(result.returncode, 0, result.stderr)
        package = Path(result.stdout.strip())
        rows = self.rows(package / "candidates.jsonl")
        self.assertTrue(any(row["canonical_key"] == "github:example/gpt6-robot" for row in rows))
        post = next(row for row in rows if row["candidate_kind"] == "post")
        self.assertEqual(post["post_url"], "https://x.com/example/status/123456789")
        self.assertEqual(post["status"], "needs_user_media")
        repo = next(row for row in rows if row["canonical_key"] == "github:example/gpt6-robot")
        self.assertEqual((repo["relevance_tier"], repo["inference_confidence"]), ("weak_lead", "low"))
        run = json.loads((package / "run.json").read_text(encoding="utf-8"))
        self.assertTrue(all(value["status"] == "complete" for value in run["adapter_runs"].values()))

    def test_github_incomplete_cap_early_empty_and_invalid_entry_are_failures(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        plan = {"adapter_key": "github-search:negative", "query": {"name": "negative", "page_size": 30, "max_pages": 2}}
        lower, upper = daily_review.parse_time("2026-09-01T00:00:00Z"), daily_review.parse_time("2026-09-20T00:00:00Z")
        cases = [
            ({"total_count": 1, "incomplete_results": True, "items": []}, "github_incomplete_results"),
            ({"total_count": 1001, "incomplete_results": False, "items": []}, "github_search_result_cap_exceeded"),
            ({"total_count": 1, "incomplete_results": False, "items": []}, "github_search_early_empty_page"),
            ({"total_count": 1, "incomplete_results": False, "items": [{"full_name": "bad/missing-fields"}]}, "github_search_invalid_repository_entry"),
        ]
        for index, (payload, reason) in enumerate(cases):
            with self.subTest(reason=reason):
                body = self.write_fixture(payload, f"github-negative-{index}.json")
                responses = {"_base": str(self.runtime), plan["adapter_key"]: [{"body_file": body.name}]}
                result = daily_review.github_search_adapter(plan, config, lower, upper, False, responses)
                self.assertFalse(result["complete"])
                self.assertIn(reason, [row["reason"] for row in result["failures"]])

    def test_feed_login_invalid_root_and_unknown_date_contract(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        config["adapters"]["feed"]["allowlist"] = ["project.example"]
        plan = {"adapter_key": "feed:negative", "feed": {"name": "negative", "url": "https://project.example/feed.atom", "source_kind": "primary"}}
        lower, upper = daily_review.parse_time("2026-09-01T00:00:00Z"), daily_review.parse_time("2026-09-20T00:00:00Z")
        for name, body_text, reason in [
            ("login.xml", "<html><body>Sign in to see feed</body></html>", "login_wall"),
            ("invalid.xml", "<html><body>ordinary HTML</body></html>", "parse_error:invalid_feed_root"),
        ]:
            body = self.runtime / name
            self.runtime.mkdir(parents=True, exist_ok=True)
            body.write_text(body_text, encoding="utf-8")
            responses = {"_base": str(self.runtime), plan["adapter_key"]: {"body_file": body.name}}
            result = daily_review.feed_adapter(plan, config, lower, upper, False, responses)
            self.assertFalse(result["complete"])
            self.assertIn(reason, result["failures"][0]["reason"])
        unknown = self.runtime / "unknown-date.atom"
        unknown.write_text('<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry><id>https://project.example/item</id><title>Undated lead</title><link href="https://project.example/item"/></entry></feed>', encoding="utf-8")
        responses = {"_base": str(self.runtime), plan["adapter_key"]: {"body_file": unknown.name}}
        result = daily_review.feed_adapter(plan, config, lower, upper, False, responses)
        self.assertTrue(result["complete"])
        self.assertEqual((result["items"][0]["event_date"], result["items"][0]["event_date_kind"]), (None, "unknown"))
        self.assertIn("retained as unknown", result["items"][0]["unresolved_questions"][-1])

    def test_github_incomplete_and_feed_login_leave_evidence_without_watermark(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        config["sources"]["github_searches"] = [{"name": "negative", "query_template": "{model_terms} {embodied_terms}"}]
        config["sources"]["feeds"] = [{"name": "negative", "url": "https://project.example/feed.atom"}]
        config["adapters"]["feed"]["allowlist"] = ["project.example"]
        config_path = self.write_fixture(config, "negative-adapters-config.json")
        github_body = self.write_fixture({"total_count": 1, "incomplete_results": True, "items": []}, "incomplete-github.json")
        feed_body = self.runtime / "login-feed.xml"
        feed_body.write_text("<html><body>Sign in to see feed</body></html>", encoding="utf-8")
        manifest = self.write_fixture({
            "github-search:negative": [{"body_file": github_body.name}],
            "feed:negative": {"body_file": feed_body.name},
        }, "negative-responses.json")
        github = self.run_collector(extra=["--adapter", "github", "--response-fixture", str(manifest)], config=config_path)
        self.assertEqual(github.returncode, 2, github.stderr)
        self.assertEqual(self.rows(Path(github.stdout.strip()) / "evidence.jsonl")[0]["failure_reason"], "github_incomplete_results")
        feed = self.run_collector(extra=["--adapter", "feed", "--response-fixture", str(manifest)], config=config_path)
        self.assertEqual(feed.returncode, 2, feed.stderr)
        self.assertEqual(self.rows(Path(feed.stdout.strip()) / "evidence.jsonl")[0]["failure_reason"], "login_wall")
        state = json.loads((self.state / "state.json").read_text(encoding="utf-8"))
        self.assertNotIn("last_successful_upper_bound", state["adapters"]["github-search:negative"])
        self.assertNotIn("last_successful_upper_bound", state["adapters"]["feed:negative"])

    def test_discovery_index_extracts_specific_post_not_only_page_title(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        config["adapters"]["seed"]["allowlist"].append("index.example")
        plan = {"url": "https://index.example/posts", "group": "discovery_indexes", "candidate_kind": "project", "source_kind": "secondary_index"}
        original = daily_review.http_get
        body = (ROOT / "tests/fixtures/index_posts.html").read_bytes()
        daily_review.http_get = lambda *args, **kwargs: {"status": 200, "body": body, "final_url": plan["url"], "error": None}
        try:
            result = daily_review.seed_adapter(plan, config, True)
        finally:
            daily_review.http_get = original
        self.assertEqual(result["items"][0]["primary_url"], "https://x.com/example/status/987654321")
        self.assertEqual(result["items"][0]["candidate_kind"], "post")

    def test_mixed_adapter_failure_only_advances_successful_adapter(self):
        config = self.arxiv_config()
        result = self.run_collector(extra=["--adapter", "fixture", "--adapter", "arxiv"], config=config)
        self.assertEqual(result.returncode, 2, result.stderr)
        state = json.loads((self.state / "state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["adapters"]["fixture"]["last_successful_upper_bound"], "2026-09-20T00:00:00Z")
        self.assertNotIn("last_successful_upper_bound", state["adapters"]["arxiv:embodied"])

    def test_each_adapter_computes_its_own_window(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        config["sources"]["arxiv_queries"] = [{"name": "embodied", "query_template": "{model_terms} AND {embodied_terms}"}]
        config_path = self.write_fixture(config, "window-config.json")
        self.state.mkdir(parents=True)
        state = daily_review.default_state()
        state["adapters"] = {"fixture": {"last_successful_upper_bound": "2026-09-20T00:00:00Z"}, "arxiv:embodied": {"last_successful_upper_bound": "2026-09-10T00:00:00Z"}}
        (self.state / "state.json").write_text(json.dumps(state), encoding="utf-8")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/daily_review.py"), "--dry-run", "--fixture", str(FIXTURE), "--config", str(config_path), "--output-root", str(self.output), "--state-root", str(self.state), "--to", "2026-09-21T00:00:00Z"], cwd=ROOT, capture_output=True, text=True)
        windows = json.loads(result.stdout)["adapter_windows"]
        self.assertEqual(windows["fixture"]["lower_bound"], "2026-09-17T00:00:00Z")
        self.assertEqual(windows["arxiv:embodied"]["lower_bound"], "2026-09-07T00:00:00Z")

    def test_state_is_not_read_before_lock(self):
        self.state.mkdir(parents=True)
        (self.state / "state.json").write_text("not-json", encoding="utf-8")
        lock = (self.state / "collector.lock").open("a+")
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            result = self.run_collector()
        finally:
            lock.close()
        self.assertEqual(result.returncode, 75, result.stderr)
        self.assertIn("skipped_locked", result.stderr)

    def test_package_published_state_failure_is_resumable(self):
        temporary = self.runtime / "temp-package"
        final = self.runtime / "final-package"
        temporary.mkdir(parents=True)
        (temporary / "marker").write_text("ok", encoding="utf-8")
        checkpoint_path = self.runtime / "checkpoint.json"
        state_path = self.runtime / "state.json"
        pending = daily_review.default_state()
        pending["revision"] = 1
        pending["committed_runs"]["recover-run"] = {"revision": 1}
        daily_review.atomic_json(checkpoint_path, {"run_id": "recover-run", "phase": "package_ready", "temporary_dir": str(temporary), "final_dir": str(final), "pending_state": pending, "base_revision": 0, "exit_code": 0})
        failed = {"done": False}
        def flaky_writer(path, value):
            if path == state_path and not failed["done"]:
                failed["done"] = True
                raise OSError("simulated state persistence failure")
            daily_review.atomic_json(path, value)
        with self.assertRaises(OSError):
            daily_review.resume_commit(checkpoint_path, state_path, writer=flaky_writer)
        self.assertTrue(final.exists())
        self.assertEqual(json.loads(checkpoint_path.read_text(encoding="utf-8"))["phase"], "package_published")
        recovered, code = daily_review.resume_commit(checkpoint_path, state_path)
        self.assertEqual((recovered, code), (final, 0))
        self.assertEqual(json.loads(state_path.read_text(encoding="utf-8"))["version"], 2)

    def test_stale_old_transaction_cannot_overwrite_new_state_or_decision(self):
        final = self.runtime / "old-package"
        final.mkdir(parents=True)
        checkpoint_path = self.runtime / "old-checkpoint.json"
        old = daily_review.default_state()
        old["revision"] = 1
        old["adapters"]["arxiv:q"] = {"last_successful_upper_bound": "2026-09-19T00:00:00Z"}
        old["committed_runs"]["old-run"] = {"revision": 1}
        daily_review.atomic_json(checkpoint_path, {"run_id": "old-run", "phase": "package_published", "temporary_dir": str(self.runtime / "missing"), "final_dir": str(final), "pending_state": old, "base_revision": 0, "exit_code": 0})
        current = daily_review.default_state()
        current["revision"] = 2
        current["adapters"]["arxiv:q"] = {"last_successful_upper_bound": "2026-09-20T00:00:00Z"}
        current["decisions"] = [{"candidate_id": "C-NEW", "decision": "rejected", "decided_at": "2026-09-20T02:00:00Z"}]
        state_path = self.runtime / "state.json"
        daily_review.atomic_json(state_path, current)
        with self.assertRaisesRegex(RuntimeError, "stale transaction"):
            daily_review.resume_commit(checkpoint_path, state_path)
        persisted = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(persisted, current)
        self.assertEqual(json.loads(checkpoint_path.read_text(encoding="utf-8"))["phase"], "stale_conflict")

    def test_repeated_commit_is_recognized_without_overwrite(self):
        final = self.runtime / "package"
        final.mkdir(parents=True)
        checkpoint_path = self.runtime / "checkpoint.json"
        pending = daily_review.default_state()
        pending["revision"] = 1
        pending["committed_runs"]["same-run"] = {"revision": 1}
        daily_review.atomic_json(checkpoint_path, {"run_id": "same-run", "phase": "package_published", "temporary_dir": str(self.runtime / "missing"), "final_dir": str(final), "pending_state": pending, "base_revision": 0, "exit_code": 0})
        current = copy.deepcopy(pending)
        current["revision"] = 3
        current["decisions"] = [{"candidate_id": "C-LATER", "decision": "rejected"}]
        state_path = self.runtime / "state.json"
        daily_review.atomic_json(state_path, current)
        recovered, code = daily_review.resume_commit(checkpoint_path, state_path)
        self.assertEqual((recovered, code), (final, 0))
        self.assertEqual(json.loads(state_path.read_text(encoding="utf-8")), current)
        self.assertEqual(json.loads(checkpoint_path.read_text(encoding="utf-8"))["phase"], "state_committed")

    def test_new_run_refuses_unfinished_transaction(self):
        checkpoint = self.state / "runs/pending.json"
        daily_review.atomic_json(checkpoint, {"run_id": "pending", "phase": "package_published"})
        result = self.run_collector()
        self.assertEqual(result.returncode, 1)
        self.assertIn("unfinished transaction must be resumed first", result.stderr)

    def test_residual_ambiguous_directories_are_rejected(self):
        temporary = self.runtime / "temp"
        final = self.runtime / "final"
        temporary.mkdir(parents=True)
        final.mkdir(parents=True)
        checkpoint = self.runtime / "checkpoint.json"
        daily_review.atomic_json(checkpoint, {"run_id": "ambiguous", "phase": "package_ready", "temporary_dir": str(temporary), "final_dir": str(final), "pending_state": {}, "base_revision": 0, "exit_code": 0})
        with self.assertRaisesRegex(RuntimeError, "unique"):
            daily_review.resume_commit(checkpoint, self.runtime / "state.json")

    def test_collecting_checkpoint_restarts_with_same_run_id(self):
        run_id = "resume-collecting-01"
        temporary = self.output / "2026-09-20" / ("." + run_id + ".tmp")
        final = self.output / "2026-09-20" / run_id
        temporary.mkdir(parents=True)
        (temporary / "partial").write_text("incomplete", encoding="utf-8")
        checkpoint_path = self.state / "runs" / f"{run_id}.json"
        resume_args = ["--once", "--fixture", str(FIXTURE), "--config", str(CONFIG), "--output-root", str(self.output), "--state-root", str(self.state), "--from", "2026-09-01T00:00:00Z"]
        daily_review.atomic_json(checkpoint_path, {"run_id": run_id, "phase": "collecting", "temporary_dir": str(temporary), "final_dir": str(final), "started_at": "2026-09-20T00:00:00Z", "resume_args": resume_args,
            "upper_bound": "2026-09-20T00:00:00Z", "windows": {"fixture": {"lower_bound": "2026-09-01T00:00:00Z", "upper_bound": "2026-09-20T00:00:00Z", "cursor": 0}},
            "config_hash": daily_review.sha256_file(CONFIG), "base_revision": 0})
        result = subprocess.run([sys.executable, str(ROOT / "scripts/daily_review.py"), "--resume-run", run_id, "--output-root", str(self.output), "--state-root", str(self.state)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(result.stdout.strip()), final)
        self.assertTrue(final.is_dir())
        self.assertEqual(len(list((self.state / "abandoned").iterdir())), 1)
        self.assertEqual(json.loads(checkpoint_path.read_text(encoding="utf-8"))["phase"], "state_committed")

    def test_restart_pending_can_be_resumed_again(self):
        run_id = "restart-pending-01"
        final = self.output / "2026-09-20" / run_id
        checkpoint_path = self.state / "runs" / f"{run_id}.json"
        resume_args = ["--once", "--fixture", str(FIXTURE), "--config", str(CONFIG), "--output-root", str(self.output), "--state-root", str(self.state)]
        daily_review.atomic_json(checkpoint_path, {"run_id": run_id, "phase": "restart_pending", "temporary_dir": str(final.with_name("." + run_id + ".tmp")), "final_dir": str(final), "started_at": "2026-09-20T00:00:00Z", "resume_args": resume_args,
            "upper_bound": "2026-09-20T00:00:00Z", "windows": {"fixture": {"lower_bound": "2026-08-21T00:00:00Z", "upper_bound": "2026-09-20T00:00:00Z", "cursor": 0}},
            "config_hash": daily_review.sha256_file(CONFIG), "base_revision": 0})
        result = subprocess.run([sys.executable, str(ROOT / "scripts/daily_review.py"), "--resume-run", run_id, "--output-root", str(self.output), "--state-root", str(self.state)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        run = json.loads((final / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(run["adapter_runs"]["fixture"]["upper_bound"], "2026-09-20T00:00:00Z")

    def test_interruption_stops_new_items_and_does_not_advance(self):
        daily_review.INTERRUPTED = True
        with contextlib.redirect_stdout(io.StringIO()):
            code = daily_review.main(["--once", "--fixture", str(FIXTURE), "--config", str(CONFIG), "--output-root", str(self.output), "--state-root", str(self.state), "--from", "2026-09-01T00:00:00Z", "--to", "2026-09-20T00:00:00Z"])
        self.assertEqual(code, 130)
        state = json.loads((self.state / "state.json").read_text(encoding="utf-8"))
        self.assertNotIn("last_successful_upper_bound", state["adapters"]["fixture"])
        package = next(path for path in self.output.rglob("run.json")).parent
        self.assertEqual(self.rows(package / "candidates.jsonl"), [])

    def test_output_and_run_id_cannot_escape_managed_root(self):
        with self.assertRaises(ValueError):
            daily_review.managed_path(Path("/tmp/outside-review"))
        for value in ("../escape", "/absolute", "a" * 81):
            with self.assertRaises(ValueError):
                daily_review.validate_run_id(value)

    def test_seed_body_change_creates_evidence_update_and_second_source_is_retained(self):
        taxonomy = {"evaluation": ["evaluation"]}
        state = daily_review.default_state()
        raw = {"primary_url": "https://example.com/Project?view=1", "candidate_kind": "project", "title": "Stable title",
               "source_kind": "primary", "access": "page_text", "event_date": None, "event_date_kind": "unknown",
               "_discovery": {"source_url": "https://example.com/Project?view=1", "content_hash": "old", "aliases": ["https://example.com/Project?view=1"]}}
        first, observation = daily_review.normalize_item(raw, "2026-09-20T00:00:00Z", {}, state, taxonomy)
        daily_review.apply_observation(state, observation)
        changed = copy.deepcopy(raw)
        changed["_discovery"]["content_hash"] = "new"
        second, observation = daily_review.normalize_item(changed, "2026-09-20T01:00:00Z", {}, state, taxonomy)
        daily_review.apply_observation(state, observation)
        self.assertNotEqual(first["candidate_id"], second["candidate_id"])
        self.assertEqual(second["update_of"], first["candidate_id"])
        self.assertEqual(second["changed_fields"], ["evidence_content:url:https://example.com/Project?view=1"])
        other = copy.deepcopy(changed)
        other["_discovery"] = {"source_url": "https://evidence.example/paper", "content_hash": "other", "aliases": ["https://example.com/Project?view=1"]}
        candidate, observation = daily_review.normalize_item(other, "2026-09-20T02:00:00Z", {}, state, taxonomy)
        self.assertIsNone(candidate)
        self.assertEqual(observation["evidence_candidate_id"], second["candidate_id"])
        daily_review.apply_observation(state, observation)
        identity = state["identities"]["url:https://example.com/Project?view=1"]
        self.assertIn("url:https://evidence.example/paper", identity["evidence"])

    def test_redirect_aliases_deduplicate_identity(self):
        taxonomy = {}
        state = daily_review.default_state()
        first_raw = {"primary_url": "https://new.example/Project", "candidate_kind": "project", "event_date": None, "event_date_kind": "unknown",
                     "_discovery": {"source_url": "https://old.example/Project", "content_hash": "same", "aliases": ["https://old.example/Project", "https://new.example/Project"]}}
        first, observation = daily_review.normalize_item(first_raw, "2026-09-20T00:00:00Z", {}, state, taxonomy)
        daily_review.apply_observation(state, observation)
        second_raw = copy.deepcopy(first_raw)
        second_raw["primary_url"] = "https://old.example/Project"
        second, observation = daily_review.normalize_item(second_raw, "2026-09-20T01:00:00Z", {}, state, taxonomy)
        self.assertIsNone(second)
        self.assertEqual(observation["evidence_candidate_id"], first["candidate_id"])
        self.assertEqual(len(state["identities"]), 1)

    def test_approved_decision_produces_proposal_only_change_plan(self):
        first = self.run_collector()
        self.assertEqual(first.returncode, 0, first.stderr)
        candidate = next(row for row in self.rows(Path(first.stdout.strip()) / "candidates.jsonl") if row["candidate_kind"] == "project")
        decision = {"candidate_id": candidate["candidate_id"], "decision": "approved", "reviewer": "offline-reviewer",
                    "decided_at": "2026-09-20T12:00:00Z", "reason": "fixture acceptance test",
                    "accepted_fields": ["title_en_draft", "event_date", "event_date_basis"]}
        decisions = self.runtime / "decisions.jsonl"
        decisions.write_text(json.dumps(decision) + "\n", encoding="utf-8")
        before = daily_review.formal_hashes()
        second = self.run_collector(extra=["--decisions", str(decisions)])
        self.assertEqual(second.returncode, 0, second.stderr)
        package = Path(second.stdout.strip())
        plans = self.rows(package / "change-plans.jsonl")
        self.assertEqual(len(plans), 1)
        plan = plans[0]
        self.assertTrue(plan["proposal_only"])
        self.assertFalse(plan["formal_id_assigned"])
        current_window_end = json.loads((ROOT / "data/metadata.json").read_text(encoding="utf-8"))["window_end"]
        self.assertEqual(plan["date_window_proposal"]["proposed"]["window_end"], current_window_end)
        self.assertIn("data/metadata.json", plan["files_to_update_after_separate_human_authorization"])
        self.assertEqual(daily_review.formal_hashes(), before)

    def test_approved_empty_fields_respects_rejections_and_does_not_advance_date(self):
        first = self.run_collector()
        candidate = next(row for row in self.rows(Path(first.stdout.strip()) / "candidates.jsonl") if row["candidate_kind"] == "project")
        decision = {"candidate_id": candidate["candidate_id"], "decision": "approved", "reviewer": "offline-reviewer",
                    "decided_at": "2026-09-20T12:01:00Z", "reason": "only the candidate concept is approved",
                    "accepted_fields": [], "rejected_fields": ["event_date", "title_en_draft"]}
        decisions = self.runtime / "empty-fields.jsonl"
        decisions.write_text(json.dumps(decision) + "\n", encoding="utf-8")
        result = self.run_collector(extra=["--decisions", str(decisions)])
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = self.rows(Path(result.stdout.strip()) / "change-plans.jsonl")[0]
        self.assertEqual(plan["adopted_fields"], {})
        current_window_end = json.loads((ROOT / "data/metadata.json").read_text(encoding="utf-8"))["window_end"]
        self.assertEqual(plan["date_window_proposal"]["proposed"]["window_end"], current_window_end)
        self.assertEqual(plan["date_window_proposal"]["status"], "pending_unapproved_or_unverified_date")

    def test_decision_field_conflict_is_rejected(self):
        first = self.run_collector()
        candidate = self.rows(Path(first.stdout.strip()) / "candidates.jsonl")[0]
        decision = {"candidate_id": candidate["candidate_id"], "decision": "approved", "reviewer": "offline-reviewer",
                    "decided_at": "2026-09-20T12:02:00Z", "reason": "invalid conflict",
                    "accepted_fields": ["event_date"], "rejected_fields": ["event_date"]}
        decisions = self.runtime / "conflict.jsonl"
        decisions.write_text(json.dumps(decision) + "\n", encoding="utf-8")
        result = self.run_collector(extra=["--decisions", str(decisions)])
        self.assertEqual(result.returncode, 1)
        self.assertIn("accepted_fields and rejected_fields conflict", result.stderr)

    def test_user_media_preserves_original_name_hash_mapping_and_encoded_suggestion(self):
        first = self.run_collector()
        self.assertEqual(first.returncode, 0, first.stderr)
        candidate = next(row for row in self.rows(Path(first.stdout.strip()) / "candidates.jsonl") if row["candidate_kind"] == "post")
        media = self.runtime / "演示 原图 #1.png"
        media.write_bytes(b"offline-user-media")
        mapping = self.runtime / "media.csv"
        mapping.write_text("candidate_id,user_supplied_path,original_filename\n" +
                           f'{candidate["candidate_id"]},"{media}","{media.name}"\n', encoding="utf-8")
        second = self.run_collector(extra=["--user-media-map", str(mapping)])
        self.assertEqual(second.returncode, 0, second.stderr)
        package = Path(second.stdout.strip())
        with (package / "media-name-map.csv").open(encoding="utf-8", newline="") as handle:
            row = next(row for row in csv.DictReader(handle) if row["candidate_id"] == candidate["candidate_id"])
        copied = package / row["user_supplied_path"]
        self.assertEqual(copied.read_bytes(), media.read_bytes())
        self.assertEqual(row["sha256"], daily_review.sha256_file(media))
        self.assertEqual(row["mapping_status"], "verified")
        self.assertIn("%E6%BC%94%E7%A4%BA%20%E5%8E%9F%E5%9B%BE%20%231.png", row["suggested_site_path"])
        self.assertEqual(Path(row["suggested_site_path"]).parts[:2], ("assets", "social"))
        self.assertEqual(len(Path(row["suggested_site_path"]).parts), 3)
        self.assertTrue(media.exists())

    def test_media_same_names_multiple_files_duplicates_and_candidates_are_unambiguous(self):
        rows = json.loads(FIXTURE.read_text(encoding="utf-8"))
        second_post = copy.deepcopy(rows[1])
        second_post["primary_url"] = "https://x.com/example_robot/status/2100000000000000001"
        first = self.run_collector(self.write_fixture([rows[1], second_post], "two-posts.json"))
        candidates = self.rows(Path(first.stdout.strip()) / "candidates.jsonl")
        c1, c2 = candidates[0]["candidate_id"], candidates[1]["candidate_id"]
        media_specs = [("a", "demo.mp4", b"first"), ("b", "demo.mp4", b"second"),
                       ("c", "demo.mp4", b"first"), ("d", "cover.png", b"cover"), ("e", "demo.mp4", b"first"),
                       ("f", "X01.jpg", b"different-from-formal")]
        paths = []
        for folder, name, content in media_specs:
            path = self.runtime / folder / name
            path.parent.mkdir()
            path.write_bytes(content)
            paths.append(path)
        mapping = self.runtime / "many-media.csv"
        mapping.write_text("candidate_id,user_supplied_path,original_filename\n" + "".join(
            f'{candidate},"{path}","{path.name}"\n' for candidate, path in [(c1, paths[0]), (c1, paths[1]), (c1, paths[2]), (c1, paths[3]), (c2, paths[4]), (c2, paths[5])]), encoding="utf-8")
        second = self.run_collector(self.write_fixture([rows[1], second_post], "two-posts-again.json"), extra=["--user-media-map", str(mapping)])
        self.assertEqual(second.returncode, 0, second.stderr)
        package = Path(second.stdout.strip())
        with (package / "media-name-map.csv").open(encoding="utf-8", newline="") as handle:
            mapped = [row for row in csv.DictReader(handle) if row["mapping_status"] != "awaiting_user_file"]
        self.assertEqual(len(mapped), 6)
        for row in mapped:
            self.assertEqual(daily_review.sha256_file(package / row["user_supplied_path"]), row["sha256"])
        c1_demo = [row for row in mapped if row["candidate_id"] == c1 and row["original_filename"] == "demo.mp4"]
        self.assertEqual(len({row["user_supplied_path"] for row in c1_demo}), 2)
        self.assertEqual(c1_demo[0]["user_supplied_path"], c1_demo[2]["user_supplied_path"])
        self.assertTrue(all(row["mapping_status"] == "needs_manual_path_resolution" and not row["suggested_site_path"] for row in c1_demo))
        c2_demo = next(row for row in mapped if row["candidate_id"] == c2)
        self.assertEqual((c2_demo["mapping_status"], c2_demo["suggested_site_path"]), ("needs_manual_path_resolution", ""))
        cover = next(row for row in mapped if row["original_filename"] == "cover.png")
        self.assertEqual(Path(cover["suggested_site_path"]).parts, ("assets", "social", "cover.png"))
        formal_conflict = next(row for row in mapped if row["original_filename"] == "X01.jpg")
        self.assertEqual((formal_conflict["mapping_status"], formal_conflict["suggested_site_path"]), ("needs_manual_path_resolution", ""))

    def test_seed_http_status_login_redirect_and_policy(self):
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
        plan = {"url": "https://github.com/owner/repo", "candidate_kind": "project", "source_kind": "primary"}
        original = daily_review.http_get
        try:
            daily_review.http_get = lambda *args, **kwargs: {"status": 429, "body": b"", "final_url": plan["url"], "error": "http_429"}
            self.assertEqual(daily_review.seed_adapter(plan, config, True)["failures"][0]["http_status"], 429)
            daily_review.http_get = lambda *args, **kwargs: {"status": 200, "body": b'<form><input type="password"></form>', "final_url": "https://github.com/login", "error": None}
            self.assertEqual(daily_review.seed_adapter(plan, config, True)["failures"][0]["reason"], "login_wall")
            daily_review.http_get = lambda *args, **kwargs: {"status": 200, "body": b"<title>x</title>", "final_url": "https://evil.example/x", "error": None}
            self.assertEqual(daily_review.seed_adapter(plan, config, True)["failures"][0]["reason"], "redirect_target_not_allowed")
        finally:
            daily_review.http_get = original
        self.assertFalse(daily_review.content_allowed({"language": "fr", "title": "safe"}, {"languages": ["en"], "deny_terms": []}))
        self.assertFalse(daily_review.content_allowed({"language": "en", "title": "blocked topic"}, {"languages": ["en"], "deny_terms": ["blocked"]}))

    def test_http_client_enforces_request_interval_and_redirect_policy_before_follow(self):
        timeline = {"now": 0.0}
        sleeps = []
        client = daily_review.HttpClient(2.0, clock=lambda: timeline["now"], sleeper=lambda delay: (sleeps.append(delay), timeline.__setitem__("now", timeline["now"] + delay)))
        class Response:
            status = 200
            headers = {"Content-Type": "text/html"}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def geturl(self): return "https://github.com/owner/repo"
            def read(self, _limit): return b"<title>ok</title>"
        class Opener:
            def open(self, _request, timeout): return Response()
        original = daily_review.urllib.request.build_opener
        daily_review.urllib.request.build_opener = lambda *_handlers: Opener()
        try:
            policy = {"allowlist": ["github.com"], "denylist": []}
            client.get("https://github.com/owner/repo", 1, 0, "text/html", policy)
            client.get("https://github.com/owner/repo", 1, 0, "text/html", policy)
        finally:
            daily_review.urllib.request.build_opener = original
        self.assertEqual(sleeps, [2.0])
        handler = daily_review.PolicyRedirectHandler({"allowlist": ["github.com"], "denylist": []})
        with self.assertRaises(daily_review.RedirectBlocked):
            handler.redirect_request(None, None, 302, "found", {}, "https://evil.example/target")


if __name__ == "__main__":
    unittest.main()
