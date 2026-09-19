#!/usr/bin/env python3
"""Offline schema, provenance, date, URL-syntax and local Markdown-link checks."""
from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {'core', 'supporting', 'watchlist', 'rednote_leads'}
ENVIRONMENTS = {'real', 'simulation', 'real_and_sim', 'visual_replay', 'simulation_and_hardware_demo', 'noninteractive', 'mixed', 'unknown'}
RELATIONS = {'explicit_primary', 'explicit_partial', 'explicit_author_mirror', 'reported_secondary', 'infrastructure', 'not_established', 'comparison_only', 'discovery_only'}
WINDOW = {'in_window', 'month_only', 'reported_in_window', 'date_unconfirmed', 'updated_in_window', 'outside_window'}
CATEGORIES = {'closed_loop', 'hybrid', 'evaluation', 'policy_improvement', 'real2sim', 'coding_evaluation', 'harness', 'understanding_benchmark', 'benchmark', 'discovery_collection', 'hierarchical_control', 'dexterous_sim', 'rl_engineering', 'paused_physics', 'generated_control', 'planned_replay', 'environment_engineering'}
ACCESS = {'search_text', 'page_text', 'partial_index', 'linked_only'}
KINDS = {'primary', 'author_mirror', 'secondary_index', 'secondary'}
PROJECT_KEYS = {'id','title','section','category','environment','scene_tags','gpt6_relation','evidence_level','summary','authors','event_date','event_date_basis','window_status','url','code_url','license_status','control_interface','metrics','limitations','source_ids','links','last_checked','independently_reproduced'}


def load(name: str):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)


def valid_url(value: str) -> bool:
    try:
        parts = urlsplit(value)
        return parts.scheme == 'https' and bool(parts.hostname) and not parts.username and not parts.password and not any(c.isspace() for c in value)
    except (ValueError, TypeError):
        return False


def valid_media_url(value: str) -> bool:
    """Permit verified web URLs or bundled, Pages-relative Social assets."""
    if valid_url(value):
        return True
    parsed = urlsplit(value or '')
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        return False
    # Bundled attachment names intentionally retain uploader spelling, including
    # spaces.  The data URI uses percent encoding; reject traversal and accept
    # only an existing file below the one Pages-published media directory.
    path = Path(unquote(parsed.path))
    if path.is_absolute() or path.parts[:2] not in {('assets', 'social'), ('assets', 'posters')} or len(path.parts) != 3 or '..' in path.parts:
        return False
    return (ROOT / 'site' / path).is_file()


def optional_lightweight_media(item: dict) -> bool:
    """The delivery ZIP omits only user-supplied Social originals.

    Their paths remain valid Pages-relative targets when a maintainer copies
    the listed originals in before a full-media deployment.  A lean public
    source checkout must still validate, build, and publish its static shell
    without mistaking these deliberate omissions for arbitrary missing assets.
    """
    return (
        isinstance(item, dict)
        and str(item.get('url', '')).startswith('assets/social/')
        and str(item.get('source_path', '')).startswith('User attachment')
    )


def valid_date(value: str, month_allowed: bool = False) -> bool:
    if not isinstance(value, str):
        return False
    if month_allowed and re.fullmatch(r'\d{4}-\d{2}', value):
        value += '-01'
    try:
        return bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', value)) and date.fromisoformat(value) is not None
    except ValueError:
        return False


def normalized_repository_url(value: str) -> str | None:
    """Return a GitHub repository identity, ignoring anchors and presentation URL form.

    This intentionally applies only to repository main URLs. Repeated author
    profile URLs (for distinct X demonstrations, for example) are not treated
    as duplicate projects.
    """
    parts = urlsplit(value)
    if parts.hostname is None or parts.hostname.lower() != 'github.com':
        return None
    segments = [segment for segment in parts.path.split('/') if segment]
    if len(segments) < 2:
        return None
    return f'https://github.com/{segments[0]}/{segments[1]}'.lower()


def validate_data(projects, sources, artifacts, metadata) -> list[str]:
    errors = []
    def expect(ok, msg):
        if not ok:
            errors.append(msg)
    pids = [p.get('id') for p in projects]
    sids = [s.get('id') for s in sources]
    aids = [a.get('id') for a in artifacts]
    for label, ids in [('project', pids), ('source', sids), ('artifact', aids)]:
        expect(len(ids) == len(set(ids)), f'Duplicate {label} IDs')
    repositories: dict[str, list[str]] = {}
    for project in projects:
        repository = normalized_repository_url(project.get('url', ''))
        if repository:
            repositories.setdefault(repository, []).append(str(project.get('id')))
    for repository, ids in repositories.items():
        expect(len(ids) == 1, f'Duplicate normalized repository URL {repository}: {", ".join(ids)}')
    for s in sources:
        sid = s.get('id')
        expect(bool(re.fullmatch(r'S\d{3}', str(sid))), f'{sid}: invalid source ID')
        expect(valid_url(s.get('url')), f'{sid}: malformed URL')
        expect(s.get('kind') in KINDS, f'{sid}: invalid source kind')
        expect(s.get('access') in ACCESS, f'{sid}: invalid access mode')
        expect(valid_date(s.get('checked_at')), f'{sid}: invalid checked_at')
    for p in projects:
        pid = p.get('id')
        expect(PROJECT_KEYS.issubset(p), f'{pid}: missing fields {PROJECT_KEYS-set(p)}')
        if not PROJECT_KEYS.issubset(p):
            continue
        expect(bool(re.fullmatch(r'[PXR]\d{2}', str(pid))), f'{pid}: invalid project ID')
        for key, allowed in [('section',SECTIONS),('category',CATEGORIES),('environment',ENVIRONMENTS),('gpt6_relation',RELATIONS),('window_status',WINDOW),('evidence_level',set('ABCD'))]:
            expect(p[key] in allowed, f'{pid}: invalid {key}')
        expect(isinstance(p['scene_tags'],list) and p['scene_tags'] and set(p['scene_tags']).issubset({'sim','real'}) and len(p['scene_tags'])==len(set(p['scene_tags'])), f'{pid}: invalid scene_tags')
        for key in ['title','summary','authors','event_date_basis','license_status','control_interface']:
            expect(isinstance(p[key],str) and bool(p[key].strip()), f'{pid}: empty {key}')
        expect(valid_url(p['url']), f'{pid}: malformed main URL')
        expect(p['code_url'] is None or valid_url(p['code_url']), f'{pid}: malformed code URL')
        expect(isinstance(p['source_ids'],list) and bool(p['source_ids']), f'{pid}: missing provenance')
        for sid in p['source_ids']:
            expect(sid in sids, f'{pid}: unknown source {sid}')
        expect(isinstance(p['limitations'],list) and bool(p['limitations']), f'{pid}: missing limitations')
        expect(isinstance(p['independently_reproduced'],bool), f'{pid}: reproduction flag must be Boolean')
        expect(valid_date(p['last_checked']), f'{pid}: invalid last_checked')
        expect(p['event_date'] is None or valid_date(p['event_date'],True), f'{pid}: invalid event_date')
        if p['window_status'] in {'in_window','updated_in_window'}:
            expect(valid_date(p['event_date']),f'{pid}: exact date required')
            if valid_date(p['event_date']):
                expect(metadata['window_start'] <= p['event_date'] <= metadata['window_end'], f'{pid}: exact date outside window')
        if p['window_status']=='month_only':
            expect(isinstance(p['event_date'],str) and len(p['event_date'])==7, f'{pid}: month-only format required')
        if p['section']=='rednote_leads':
            expect(p['evidence_level']=='D', f'{pid}: upgrade requires moving out of Rednote unverified leads')
        if p['section'] in {'watchlist','rednote_leads'}:
            expect(not p['metrics'], f'{pid}: unverified leads cannot carry verified quantitative metrics')
        for key, value in p['links'].items():
            if key != 'search_terms':
                expect(valid_url(value), f'{pid}: malformed {key} link')
        for m in p['metrics']:
            expect({'name','value','unit','denominator','protocol'}.issubset(m),f'{pid}: incomplete metric')
            expect(isinstance(m.get('value'),(int,float)) and not isinstance(m.get('value'),bool),f'{pid}: non-numeric metric')
            expect(bool(m.get('denominator')) and bool(m.get('protocol')),f'{pid}: missing metric denominator/protocol')
            if m.get('unit')=='successes' and isinstance(m.get('denominator'),int):
                expect(0 <= m['value'] <= m['denominator'],f'{pid}: successes outside denominator')
    for a in artifacts:
        aid = a.get('id')
        expect(bool(re.fullmatch(r'HF\d{2}',str(aid))),f'{aid}: invalid artifact ID')
        expect(a.get('project_id') in pids,f'{aid}: invalid linked project')
        expect(valid_url(a.get('url')), f'{aid}: malformed URL')
        expect(valid_date(a.get('last_checked')),f'{aid}: invalid check date')
        expect(bool(a.get('license_status')),f'{aid}: missing license status')
        for sid in a.get('source_ids',[]):
            expect(sid in sids,f'{aid}: unknown source {sid}')
    for key in ['snapshot_date','window_start','window_end']:
        expect(valid_date(metadata.get(key)), f'metadata: invalid {key}')
    expect(metadata['window_start'] <= metadata['window_end'] <= metadata['snapshot_date'],'metadata: inconsistent window')
    return errors


def validate_presentation(projects, sources, i18n, media_data, publication_dates, tag_taxonomy) -> list[str]:
    """Validate complete English coverage and attributable gallery media."""
    errors=[]
    pids={p['id'] for p in projects}
    sids={s['id'] for s in sources}
    translations=i18n.get('en') if isinstance(i18n,dict) else None
    if not isinstance(translations,dict):
        return ['i18n: missing English translation map']
    if set(translations)!=pids:
        errors.append('i18n: English translation IDs must exactly match project IDs')
    for pid in pids:
        entry=translations.get(pid,{})
        for key in ('title','summary'):
            if not isinstance(entry.get(key),str) or not entry[key].strip():
                errors.append(f'i18n: {pid} missing English {key}')
    if not isinstance(tag_taxonomy, dict):
        errors.append('tag_taxonomy: missing taxonomy')
    else:
        labels = tag_taxonomy.get('labels')
        category_tags = tag_taxonomy.get('category_tags')
        if not isinstance(labels, dict) or not isinstance(category_tags, dict):
            errors.append('tag_taxonomy: requires labels and category_tags maps')
        else:
            if set(category_tags) != CATEGORIES:
                errors.append('tag_taxonomy: category_tags must exactly cover categories')
            for tag, label in labels.items():
                if not isinstance(tag, str) or not tag.strip() or not isinstance(label, dict) or not all(isinstance(label.get(lang), str) and label[lang].strip() for lang in ('en', 'zh')):
                    errors.append(f'tag_taxonomy: invalid bilingual label {tag}')
            for category, tags in category_tags.items():
                if not isinstance(tags, list) or not tags or len(tags) != len(set(tags)) or not set(tags).issubset(labels):
                    errors.append(f'tag_taxonomy: {category} invalid topic tags')
    if not isinstance(publication_dates, dict) or set(publication_dates) != pids:
        errors.append('publication_dates: IDs must exactly match projects')
    else:
        for pid, item in publication_dates.items():
            if not isinstance(item, dict):
                errors.append(f'publication_dates: {pid} must be an object')
                continue
            if not valid_date(item.get('date')):
                errors.append(f'publication_dates: {pid} invalid display date')
            if item.get('status') not in {'verified', 'estimated'}:
                errors.append(f'publication_dates: {pid} status must be verified or estimated')
            for field in ('basis', 'uncertainty'):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(f'publication_dates: {pid} missing {field}')
            if item.get('status') == 'estimated' and (not isinstance(item.get('rule'), str) or not item['rule'].strip()):
                errors.append(f'publication_dates: {pid} estimated date needs an explicit rule')
            if item.get('status') == 'verified' and item.get('rule') is not None:
                errors.append(f'publication_dates: {pid} verified date must not claim an estimation rule')
            if 'previous_display' in item:
                for field in ('previous_display', 'meaning'):
                    if not isinstance(item.get(field), str) or not item[field].strip():
                        errors.append(f'publication_dates: {pid} invalid {field}')
                if not valid_url(item.get('evidence_url')):
                    errors.append(f'publication_dates: {pid} invalid evidence_url')
                endpoints = item.get('checked_endpoints')
                if not isinstance(endpoints, list) or not endpoints or not all(valid_url(url) for url in endpoints):
                    errors.append(f'publication_dates: {pid} invalid checked_endpoints')
    declared=media_data.get('media') if isinstance(media_data,dict) else None
    policy=media_data.get('missing_policy') if isinstance(media_data,dict) else None
    if not isinstance(declared,dict):
        return errors+['media: missing media map']
    if set(declared) != pids:
        errors.append('media: every retained project must have an explicit media or checked-missing record')
    if not isinstance(policy,dict) or not all(isinstance(policy.get(lang),str) and policy[lang].strip() for lang in ('en','zh')):
        errors.append('media: missing bilingual fallback policy')
    by_id={p['id']:p for p in projects}
    for pid,item in declared.items():
        if pid not in pids:
            errors.append(f'media: unknown project {pid}')
            continue
        if not isinstance(item,dict) or item.get('kind') not in {'image','video','missing'}:
            errors.append(f'media: {pid} must be an image, video, or missing-media record')
            continue
        for key in (('source_url',) if item.get('kind') == 'missing' else ('url','source_url')):
            valid = valid_url(item.get(key,'')) if key == 'source_url' else valid_media_url(item.get(key,''))
            if key == 'url' and not valid and optional_lightweight_media(item):
                valid = True
            if not valid:
                errors.append(f'media: {pid} invalid {key}')
        if item.get('source_id') not in sids:
            errors.append(f'media: {pid} invalid source_id')
        if item.get('source_id') not in by_id[pid]['source_ids']:
            errors.append(f'media: {pid} source_id is not in the project provenance')
        if item.get('kind') == 'missing':
            reason=item.get('reason',{})
            if not isinstance(reason,dict) or not all(isinstance(reason.get(lang),str) and reason[lang].strip() for lang in ('en','zh')):
                errors.append(f'media: {pid} missing bilingual reason')
            checked=item.get('checked_pages')
            if not isinstance(checked,list) or not checked or not all(valid_url(url) for url in checked):
                errors.append(f'media: {pid} needs checked source pages')
            continue
        for field in ('alt','caption'):
            values=item.get(field,{})
            if not isinstance(values,dict) or not all(isinstance(values.get(lang),str) and values[lang].strip() for lang in ('en','zh')):
                errors.append(f'media: {pid} missing bilingual {field}')
        if 'source_page_url' in item and not valid_url(item['source_page_url']):
            errors.append(f'media: {pid} invalid source_page_url')
        if item.get('kind') == 'video':
            if not valid_media_url(item.get('poster', '')):
                errors.append(f'media: {pid} video needs a valid static poster')
            if 'first decoded frame at 00:00:00' not in item.get('source_path', ''):
                errors.append(f'media: {pid} video poster must record a 00:00:00 first-frame source')
        elif 'poster' in item and not valid_media_url(item['poster']):
            errors.append(f'media: {pid} invalid poster')
        for field in ('source_path','classification'):
            if field in item and (not isinstance(item[field],str) or not item[field].strip()):
                errors.append(f'media: {pid} invalid {field}')
    return errors


def check_local_markdown(root: Path = ROOT) -> list[str]:
    errors=[]
    for path in root.rglob('*.md'):
        text=path.read_text(encoding='utf-8')
        for dest in re.findall(r'\]\(([^\s)]+)\)',text):
            parsed=urlsplit(dest)
            if parsed.scheme or parsed.netloc:
                continue
            target=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
            if not target.is_relative_to(root.resolve()):
                errors.append(f'{path.relative_to(root)}: local link escapes repository: {dest}')
                continue
            if not target.exists():
                errors.append(f'{path.relative_to(root)}: missing local target {dest}')
            elif parsed.fragment and target.suffix=='.md':
                # Catalogue/source links use explicit stable anchors rather than generated heading slugs.
                if re.fullmatch(r'[pxr]\d{2}|s\d{3}',parsed.fragment):
                    body=target.read_text(encoding='utf-8')
                    if f'id="{parsed.fragment}"' not in body:
                        errors.append(f'{path.relative_to(root)}: missing explicit anchor {dest}')
    return errors


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-only',action='store_true',help='Skip local Markdown links')
    args=parser.parse_args()
    try:
        projects,sources,artifacts,meta,i18n,media,publication_dates,tag_taxonomy=(load(n) for n in ['projects.json','sources.json','artifacts.json','metadata.json','i18n.json','media.json','publication_dates.json','tag_taxonomy.json'])
        errors=validate_data(projects,sources,artifacts,meta)
        errors.extend(validate_presentation(projects,sources,i18n,media,publication_dates,tag_taxonomy))
        if not args.data_only:
            errors.extend(check_local_markdown())
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(f'VALIDATION ERROR: {exc}',file=sys.stderr)
        return 1
    if errors:
        print('\n'.join('ERROR: '+e for e in errors),file=sys.stderr)
        return 1
    print(f'PASS: {len(projects)} entries, {len(sources)} sources, {len(artifacts)} HF resources; schema/provenance/dates/URL syntax/local links valid.')
    print('Offline only: remote HTTP availability and third-party experiments were NOT checked.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
