#!/usr/bin/env python3
"""Focused real-browser acceptance checks for the static Gallery."""
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlsplit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8765/')
    parser.add_argument('--browser', required=True)
    parser.add_argument('--screenshots', type=Path, required=True)
    parser.add_argument('--skip-screenshots', action='store_true')
    parser.add_argument('--subpath-html', type=Path)
    args = parser.parse_args()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        errors: list[str] = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text) if message.type == 'error' and 'Failed to load resource' not in message.text else None)
        page.goto(args.url, wait_until='domcontentloaded')
        assert page.locator('html').get_attribute('lang') == 'en'
        assert page.locator('.card').count() == 35
        assert page.locator('[data-group="projects"]').inner_text() == 'Projects'
        assert page.locator('[data-group="social"]').inner_text() == 'Social'
        assert page.locator('dialog, #detail-dialog, .dialog-media').count() == 0
        assert page.locator('.card button, .media[role="button"]').count() == 0
        visible = page.locator('body').inner_text()
        assert 'View details' not in visible and '查看详情' not in visible
        assert not errors, errors

        manifest = page.evaluate("""() => {
            const data = JSON.parse(document.querySelector('#catalog-data').textContent);
            return {projects: data.projects, media: data.media, i18n: data.i18n, publication_dates: data.publication_dates, topic_tags: data.topic_tags, tag_labels: data.tag_labels};
        }""")
        projects = manifest['projects']
        by_id = {project['id']: project for project in projects}
        publication_dates = manifest['publication_dates']
        topic_tags = manifest['topic_tags']
        tag_labels = manifest['tag_labels']
        assert set(topic_tags) == set(by_id)
        assert set(tag_labels) >= {'sim', 'real', 'control', 'real-to-sim', 'replay'}
        assert sum(item['status'] == 'verified' for item in publication_dates.values()) == 47
        assert sum(item['status'] == 'estimated' for item in publication_dates.values()) == 3

        def group_for(project: dict) -> str:
            if project['id'] in {'X07', 'X15'}:
                return 'social'
            if project['section'] != 'watchlist':
                return 'projects'
            for url in (project['url'], project['code_url'], *project['links'].values()):
                host = (urlsplit(url or '').hostname or '').lower()
                if host and host not in {'x.com', 'www.x.com'}:
                    return 'projects'
            return 'social'

        expected = {
            name: [project['id'] for project in sorted(
                (p for p in projects if group_for(p) == name),
                key=lambda p: publication_dates[p['id']]['date'], reverse=True,
            )]
            for name in ('projects', 'social')
        }
        assert len(expected['projects']) == 35 and len(expected['social']) == 15
        assert set(expected['projects']).isdisjoint(expected['social'])

        def activate(name: str):
            page.locator(f'[data-group="{name}"]').evaluate('(element) => element.click()')
            actual = page.locator('.card').evaluate_all('(els) => els.map((el) => el.dataset.projectId)')
            assert actual == expected[name], (name, actual, expected[name])

        def label_pairs(project: dict, language: str):
            labels = {'en': {'paper': 'Paper', 'code': 'Code', 'project': 'Project page', 'post': 'Post'}, 'zh': {'paper': '论文', 'code': '代码', 'project': '项目主页', 'post': '原帖'}}[language]
            result = []
            first = {}
            for key, url in [('main', project['url']), ('code', project['code_url']), *project['links'].items()]:
                if not url:
                    continue
                host = (urlsplit(url).hostname or '').lower()
                kind = 'code' if host == 'github.com' else 'paper' if host == 'arxiv.org' else ({'paper': 'paper', 'code': 'code', 'project': 'project', 'main': 'project'}.get(key) if host not in {'x.com', 'www.x.com', 'huggingface.co', 'raw.githubusercontent.com', 'assets.andonlabs.com', 'media.luminis-sim.com'} else None)
                if kind and kind not in first:
                    first[kind] = url
            result.extend((labels[kind], first[kind]) for kind in ('paper', 'code', 'project') if kind in first)
            post = next((url for url in (project['url'], project['links'].get('x'), project['links'].get('post')) if '/status/' in (url or '') and (urlsplit(url).hostname or '').lower() in {'x.com', 'www.x.com'}), None)
            if post:
                result.append((labels['post'], post))
            return result

        def publication(project: dict):
            entry = publication_dates[project['id']]
            value = entry['date']
            rendered = f'{value[:7]}{value[8:]}'
            return (entry['status'], rendered)

        retained = {pid: item for pid, item in manifest['media'].items() if item['kind'] in {'image', 'video'}}
        videos = {pid: item for pid, item in retained.items() if item['kind'] == 'video'}
        assert len(retained) == 50 and len(videos) == 21
        statuses = page.evaluate("""async (posters) => Promise.all(posters.map(async (poster) => {
            const response = await fetch(new URL(poster, location.href));
            return response.ok && (response.headers.get('content-type') || '').startsWith('image/');
        }))""", [item['poster'] for item in videos.values()])
        assert all(statuses), statuses

        for language, switch_label in [('en', None), ('zh', '中文')]:
            if switch_label:
                page.get_by_role('button', name=switch_label).evaluate('(element) => element.click()')
            for name in ('projects', 'social'):
                activate(name)
                for pid in expected[name]:
                    card = page.locator(f'.card[data-project-id="{pid}"]')
                    assert card.locator('button, dialog, [role="button"]').count() == 0, pid
                    pairs = label_pairs(by_id[pid], language)
                    assert card.locator('.actions a').all_inner_texts() == [label for label, _ in pairs], pid
                    assert card.locator('.actions a').evaluate_all('(els) => els.map((el) => el.getAttribute("href"))') == [url for _, url in pairs], pid
                    date_state, date_value = publication(by_id[pid])
                    published = card.locator('.published')
                    assert published.count() == 1 and published.get_attribute('data-date-state') == date_state, pid
                    assert 'estimated' not in (published.get_attribute('class') or ''), pid
                    assert published.locator('.label').text_content() == {'en': 'Published', 'zh': '发布日期'}[language], pid
                    assert published.locator('span').nth(1).inner_text() == date_value, pid
                    expected_tags = [*by_id[pid]['scene_tags'], *topic_tags[pid]]
                    assert card.locator('.tags .tag').evaluate_all('(els) => els.map((el) => el.dataset.tag)') == expected_tags, pid
                    assert card.locator('.tags .tag').all_inner_texts() == [tag_labels[tag][language] for tag in expected_tags], pid
                    item = retained.get(pid)
                    if item and item['kind'] == 'video':
                        video = card.locator('video')
                        assert video.count() == 1 and video.get_attribute('controls') is not None, pid
                        assert video.get_attribute('preload') == 'none' and video.get_attribute('poster') == item['poster'], pid
                styles = page.locator('.published').evaluate_all("""els => els.map(el => {
                    const style = getComputedStyle(el);
                    return [style.backgroundColor, style.borderColor, style.color, style.fontSize];
                })""")
                assert len(styles) == len(expected[name]) and len({tuple(style) for style in styles}) == 1, (language, name, styles)
            activate('projects')
            p09 = page.locator('.card[data-project-id="P09"]')
            p09_image = p09.locator('.media img')
            assert p09_image.count() == 1 and p09_image.get_attribute('src').endswith('assets/posters/P09-real2sim-title.svg')
            if args.url.startswith('http://127.0.0.1'):
                p09.evaluate('(element) => element.scrollIntoView({block: "center"})')
                page.wait_for_function("""selector => {
                    const image = document.querySelector(selector);
                    return image && image.complete && image.naturalWidth > 0;
                }""", arg='.card[data-project-id="P09"] .media img', timeout=10_000)
            assert not p09.locator('.media').evaluate('(element) => element.classList.contains("missing") || element.classList.contains("failed")')
            assert p09.evaluate('(card) => card.scrollWidth <= card.clientWidth')
            assert page.locator('dialog, #detail-dialog, .dialog-media').count() == 0

        activate('social')
        page.locator('#query').fill('Physical Robot Keyboard Typing')
        assert page.locator('.card').evaluate_all('(els) => els.map((el) => el.dataset.projectId)') == ['X01']
        page.get_by_role('button', name='English').evaluate('(element) => element.click()')
        assert page.locator('.card').evaluate_all('(els) => els.map((el) => el.dataset.projectId)') == ['X01']
        page.locator('#query').fill('真实机器人键盘打字')
        assert page.locator('.card').evaluate_all('(els) => els.map((el) => el.dataset.projectId)') == ['X01']
        page.locator('#clear-query').evaluate('(element) => element.click()')
        activate('projects')
        page.locator('#query').fill('real-to-sim')
        assert page.locator('.card').evaluate_all('(els) => els.map((el) => el.dataset.projectId)') == ['P11', 'P10', 'P08', 'P09']
        page.get_by_role('button', name='中文').evaluate('(element) => element.click()')
        assert page.locator('.card').evaluate_all('(els) => els.map((el) => el.dataset.projectId)') == ['P11', 'P10', 'P08', 'P09']
        page.locator('#query').fill('真转仿')
        assert page.locator('.card').evaluate_all('(els) => els.map((el) => el.dataset.projectId)') == ['P11', 'P10', 'P08', 'P09']
        page.locator('#query').fill('sim real')
        actual_dual = page.locator('.card').evaluate_all('(els) => els.map((el) => el.dataset.projectId)')
        assert actual_dual == ['P35', 'P06', 'P16', 'P14', 'P15', 'P13'], actual_dual
        page.locator('#clear-query').evaluate('(element) => element.click()')
        page.set_viewport_size({'width': 390, 'height': 844})
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        assert page.locator('#gallery').bounding_box()['y'] < 460
        p09 = page.locator('.card[data-project-id="P09"]')
        assert p09.evaluate('(card) => card.scrollWidth <= card.clientWidth')
        assert p09.locator('.published').evaluate('(element) => element.scrollWidth <= element.clientWidth')
        if not args.skip_screenshots:
            args.screenshots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=args.screenshots / 'mobile-layout.png')

        html = (args.subpath_html or Path(__file__).resolve().parents[1] / 'site' / 'index.html').read_text(encoding='utf-8')
        def subpath_route(route):
            if route.request.is_navigation_request():
                route.fulfill(status=200, content_type='text/html', body=html)
            else:
                route.fulfill(status=204)
        page.route('http://gallery.test/**', subpath_route)
        page.goto('http://gallery.test/project/', wait_until='domcontentloaded')
        assert page.locator('.card').count() == 35
        assert page.locator('dialog, #detail-dialog').count() == 0
        assert not errors, errors
        browser.close()
    print('PASS: no detail UI/keyboard/click hooks; all 50 sourced verified-or-explicitly-estimated publication displays, 21 first-frame video posters plus retained image covers, video controls, search, groups, language, mobile, and Pages subpath work.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
