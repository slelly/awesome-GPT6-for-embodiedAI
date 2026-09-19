#!/usr/bin/env python3
"""Build deterministic Markdown, CSV and an offline HTML catalogue; no network calls."""
from __future__ import annotations
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {'core': '核心项目与评测', 'supporting': '配套资源与对照', 'watchlist': 'X / Twitter 演示线索', 'rednote_leads': '小红书待核实线索'}
ENV = {'real': '真机', 'simulation': '仿真', 'real_and_sim': '真机 + 仿真', 'visual_replay': '视觉动画重放', 'simulation_and_hardware_demo': '仿真 / 硬件演示', 'noninteractive': '非交互评测', 'mixed': '混合资源', 'unknown': '未确认'}
REL = {'explicit_primary': '一手资料明确涉及 GPT-6', 'explicit_partial': 'GPT-6 明确，但正文证据不完整', 'explicit_author_mirror': '作者声明，经镜像获取', 'reported_secondary': '二手来源提及', 'infrastructure': '基础设施，不是单独的 GPT-6 成果', 'not_established': '未确认 GPT-6 专项结果', 'comparison_only': 'GPT-6 仅作对照', 'discovery_only': '发现线索的索引'}
DATE = {'in_window': '窗口内', 'month_only': '仅确认到月份', 'reported_in_window': '二手/作者报告时间', 'date_unconfirmed': '首发/更新时间未确认', 'updated_in_window': '本月更新，基础项目更早', 'outside_window': '窗口外背景'}

def load(name: str):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + '\n', encoding='utf-8')

def cell(value) -> str:
    return str(value).replace('|', '\\|').replace('\n', ' ')

def catalogue_entry(p: dict) -> str:
    """Avoid presenting an account/search page as an original social post."""
    if p['section'] == 'watchlist' and '/status/' not in p['url']:
        return '**入口：** 原帖未找到；不以作者主页或搜索页替代  '
    return f"**入口：** [{p['url']}]({p['url']})  "

def media_reference(url: str) -> str:
    """Avoid broken docs/ links for media bundled below site/ for Pages."""
    if url.startswith(('http://', 'https://')):
        return f'[{url}]({url})'
    return f'`site/{url}` (Pages-relative)'

def build() -> None:
    projects, sources, artifacts, meta, i18n, media_data, publication_dates, tag_taxonomy = (load(n) for n in ['projects.json', 'sources.json', 'artifacts.json', 'metadata.json', 'i18n.json', 'media.json', 'publication_dates.json', 'tag_taxonomy.json'])
    topic_tags = {p['id']: tag_taxonomy['category_tags'][p['category']] for p in projects}
    smap = {s['id']: s for s in sources}
    media = {}
    for p in projects:
        media[p['id']] = media_data['media'].get(p['id'], {
            'kind': 'missing',
            'source_url': p['url'],
            'source_id': p['source_ids'][0],
            'reason': media_data['missing_policy'],
        })
    lines = ['# 完整目录 / Full catalogue', '', f"证据快照：{meta['snapshot_date']}。本文件由 `scripts/build.py` 生成；请编辑 `data/projects.json`。", '',
             '**A/B/C/D 是来源证据等级，不是模型能力、代码质量或独立复现等级。所有条目均未由本仓库独立运行机器人实验。**', '',
             'A：一手正文可读；B：一手入口存在但关键实施/模型关系不完整；C：作者演示的可读镜像；D：二手索引。A 也可能没有公开代码。', '',
             '“核心”仅代表与主题直接相关；不等于证据全部完整，也不保证日期均精确落在窗口内。', '']
    for sec, label in SECTIONS.items():
        subset = [p for p in projects if p['section'] == sec]
        if not subset:
            continue
        lines += [f'## {label} · {len(subset)}', '']
        for p in subset:
            lines += [f"<a id=\"{p['id'].lower()}\"></a>", f"### {p['id']} · {p['title']}", '', p['summary'], '',
                      f"**来源等级：{p['evidence_level']}** · {ENV[p['environment']]} · {REL[p['gpt6_relation']]}", '',
                      f"**作者 / 团队：** {p['authors']}  ",
                      f"**事件日期：** {p['event_date'] or '未确认'}（{DATE[p['window_status']]}）  ",
                      f"**日期依据：** {p['event_date_basis']}  ",
                      catalogue_entry(p),
                      f"**代码入口：** {'[' + p['code_url'] + '](' + p['code_url'] + ')' if p['code_url'] else '未定位公开代码；不等于确认代码不存在'}  ",
                      f"**许可状态：** {p['license_status']}  ",
                      f"**控制接口 / 作用：** {p['control_interface']}", '']
            if p['metrics']:
                lines += ['| 指标 | 结果 | 分母 | 协议 / 注意事项 |', '| --- | --- | --- | --- |']
                for m in p['metrics']:
                    lines.append('| ' + ' | '.join(cell(t) for t in [m['name'], f"{m['value']} {m['unit']}", m['denominator'], m['protocol']]) + ' |')
                lines += ['']
            lines += ['**限制与未决项：** ' + ' '.join(p['limitations']), '']
            for key, url in p['links'].items():
                lines += [f"{key}：" + (f'[{url}]({url})' if url.startswith('https://') else f'`{url}`') + '  ']
            lines += ['', '**来源：** ' + ' · '.join(f"[{sid} · {smap[sid]['title']}](SOURCES.md#{sid.lower()})" for sid in p['source_ids']), '', '---', '']
    write('docs/CATALOG.md', '\n'.join(lines))

    lines = ['# Publication-date ledger', '', 'The Gallery shows verified dates as `YYYY-MMDD` and explicit estimates as `≈ YYYY-MMDD`. An estimate never changes the original `event_date` field into a claimed publication date. Month-only records use the 15th of that month as a midpoint; entries without a recoverable date use the retained first-observation snapshot date. Each row states its basis, rule, and uncertainty.', '', '| ID | Gallery display | Status | Original record | Basis | Estimation rule | Uncertainty | Sources |', '| --- | --- | --- | --- | --- | --- | --- | --- |']
    for p in projects:
        item = publication_dates[p['id']]
        recorded = p['event_date'] or 'pending confirmation'
        display = item['date'][:7] + item['date'][8:]
        if item['status'] == 'estimated':
            display = '≈ ' + display
        sources_text = ' · '.join(f'[{sid}](SOURCES.md#{sid.lower()})' for sid in p['source_ids'])
        lines.append(f"| {p['id']} | {display} | {item['status']} | {recorded} | {cell(item['basis'])} | {cell(item['rule'] or '—')} | {cell(item['uncertainty'])} | {sources_text} |")
    refreshed = [(p, publication_dates[p['id']]) for p in projects if 'previous_display' in publication_dates[p['id']]]
    lines += ['', '## Date-research replacement audit', '', 'These rows record the exact meaning of the replacement date. Repository creation, a version release, a paper submission, and an X-post timestamp are intentionally not presented as interchangeable events. The one remaining estimate documents the absence of a recoverable dated entry point.', '', '| ID | Previous display | Current display | What this date represents | Direct evidence | Checked entry points |', '| --- | --- | --- | --- | --- | --- |']
    for p, item in refreshed:
        display = item['date'][:7] + item['date'][8:]
        if item['status'] == 'estimated':
            display = '≈ ' + display
        checked = ' · '.join(f'[{url}]({url})' for url in item['checked_endpoints'])
        lines.append(f"| {p['id']} | {cell(item['previous_display'])} | {display} | {cell(item['meaning'])} | [{item['evidence_url']}]({item['evidence_url']}) | {checked} |")
    write('docs/PUBLICATION_DATES.md', '\n'.join(lines))

    lines = ['# Gallery tags', '', 'Cards combine one or two factual scene tags (`simulation` / `real world`) with one or more workflow tags. Tags are additive: they help visitors search and compare work; they do not claim a shared benchmark, deployment result, or model capability.', '', '| Tag | English | 中文 | Applied from category |', '| --- | --- | --- | --- |']
    for tag, label in tag_taxonomy['labels'].items():
        categories = ', '.join(category for category, tags in tag_taxonomy['category_tags'].items() if tag in tags)
        lines.append(f"| `{tag}` | {label['en']} | {label['zh']} | {categories or 'scene tag'} |")
    lines += ['', '## Project mapping', '', '| ID | Scene tags | Workflow tags |', '| --- | --- | --- |']
    for p in projects:
        lines.append(f"| {p['id']} | {', '.join(p['scene_tags'])} | {', '.join(topic_tags[p['id']])} |")
    write('docs/TAGS.md', '\n'.join(lines))

    lines = ['# 来源台账 / Source ledger', '', '本文件由 `data/sources.json` 生成。外链状态是 2026-09-18 的读取方式，不代表当前仍可访问。', '',
             '`search_text`：读取搜索返回的正文/索引；`page_text`：直接读取页面正文；`partial_index`：只有局部索引；`linked_only`：只取得链接，未读全文。', '',
             '镜像用于发现作者声明，不等同于原始 X 帖文已独立核验。这里只保存链接与原创核验备注，不转载第三方全文或视频。', '']
    for s in sources:
        lines += [f"<a id=\"{s['id'].lower()}\"></a>", f"## {s['id']} · {s['title']}", '', f"[{s['url']}]({s['url']})", '',
                  f"类型：`{s['kind']}` · 读取：`{s['access']}` · 检查日期：{s['checked_at']}", '', s['notes'], '']
    write('docs/SOURCES.md', '\n'.join(lines))

    lines = ['# Hugging Face 资源地图', '', '这 8 个资源与主目录交叉关联，**不是另外 8 个独立 GPT-6 实验，也不包含 GPT-6 的开放权重**。', '',
             '模型适配器、演示数据、评测轨迹、基准资产必须分开；旧版快照不能与新版相加。许可按对应版本的文件核对。', '',
             '| ID | 资源 | 类型 | 对应项目 | 核验范围 |', '| --- | --- | --- | --- |']
    for a in artifacts:
        lines.append(f"| {a['id']} | [{cell(a['title'])}]({a['url']}) | {a['kind']} | [{a['project_id']}](CATALOG.md#{a['project_id'].lower()}) | {a['verification']} |")
    for a in artifacts:
        lines += ['', f"## {a['id']} · {a['title']}", '', a['description'], '', f"许可：{a['license_status']}", '',
                  '来源：' + ' · '.join(f'[{s}](SOURCES.md#{s.lower()})' for s in a['source_ids'])]
    lines += ['', '## 下载之前', '',
              '先看文件树、许可证、版本和容量，再下载所需清单或单个案例。评测数据与真实机器人轨迹可能包含人的语音、图像或现场信息，不应默认允许再发布。', '',
              'YuMoool 的完整回放包约 135 GB；只读结果不需要模拟器。AGP 的 canonical 卡与旧 YAM 卡采用不同统计口径；不把 reset/auxiliary sessions 计作 evaluated trials。来源：[S045](SOURCES.md#s045)、[S006](SOURCES.md#s006)、[S008](SOURCES.md#s008)。', '',
              '本仓库没有下载这些大文件、替用户接受访问协议或执行远程数据中的脚本。访问错误、revision 和依赖版本应在实际使用时重新确认。']
    write('docs/HUGGING_FACE.md', '\n'.join(lines))

    lines = ['# Gallery media ledger', '', 'This ledger is generated from `data/media.json` and `data/projects.json`. Project-hosted videos stay on their original host, while every retained video uses a local static poster extracted from its first decoded frame at 00:00:00. Thirteen user-supplied Social videos, one supplied Social image, and all poster frames are published under `site/assets/` for Pages; each keeps its matched source record. P09 instead uses a clearly labelled site-made text cover because no hostable project demo asset was retained; it is not presented as project media. Gallery cards disclose a fallback when no retained media is available. The lightweight delivery package deliberately excludes the 14 large uploaded originals; see [the Chinese placement guide](SOCIAL_MEDIA_PLACEMENT.zh-CN.md).', '', '## Verified, directly linkable media', '']
    verified = [(p, media[p['id']]) for p in projects if media[p['id']]['kind'] != 'missing']
    for p, item in verified:
        source_page = item.get('source_page_url', item['source_url'])
        provenance = f"media URL: {media_reference(item['url'])}; source page: [{source_page}]({source_page}); source: [{item['source_id']}](SOURCES.md#{item['source_id'].lower()})"
        if item.get('poster'):
            provenance += f"; poster: {media_reference(item['poster'])}"
        if item.get('source_path'):
            provenance += f"; original path/version: `{item['source_path']}`"
        if item.get('classification'):
            provenance += f"; classification: {item['classification'].rstrip('.')}"
        lines += [f"- **{p['id']} · {p['title']}** — {provenance}."]
    lines += ['', '## Entries without retained verifiable demo media', '', 'These entries keep their original project or lead URL. The gallery intentionally shows an explicit fallback instead of using a generated or decorative image as evidence.', '']
    for p in projects:
        item = media[p['id']]
        if item['kind'] == 'missing':
            checks = '; '.join(f'[{url}]({url})' for url in item.get('checked_pages', [item['source_url']]))
            lines.append(f"- **{p['id']} · {p['title']}** — {item['reason']['en']} Checked: {checks}; evidence source: [{item['source_id']}](SOURCES.md#{item['source_id'].lower()}).")
    write('docs/MEDIA.md', '\n'.join(lines))

    fields = ['id', 'title', 'section', 'category', 'topic_tags', 'environment', 'gpt6_relation', 'evidence_level', 'event_date', 'window_status', 'url', 'code_url', 'license_status', 'summary', 'control_interface', 'source_ids']
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    for p in projects:
        row = {k: p[k] for k in fields if k != 'topic_tags'}
        row['topic_tags'] = ';'.join(topic_tags[p['id']])
        row['source_ids'] = ';'.join(p['source_ids'])
        writer.writerow(row)
    write('data/projects.csv', out.getvalue())
    payload = json.dumps({'metadata': meta, 'projects': projects, 'sources': sources, 'artifacts': artifacts, 'i18n': i18n, 'media': media, 'publication_dates': publication_dates, 'topic_tags': topic_tags, 'tag_labels': tag_taxonomy['labels'], 'labels': {'section': SECTIONS, 'environment': ENV, 'relation': REL, 'date': DATE}}, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    template = (ROOT / 'site' / 'template.html').read_text(encoding='utf-8')
    write('site/index.html', template.replace('__CATALOG_JSON__', payload))
    print(f'Built catalogue: {len(projects)} entries, {len(artifacts)} HF resources, {len(sources)} source records, {len(verified)} verified gallery media items.')

if __name__ == '__main__':
    build()
