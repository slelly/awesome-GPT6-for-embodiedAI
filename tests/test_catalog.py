"""Offline tests for this catalogue. No third-party robot/model execution."""
from __future__ import annotations
import copy
import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('catalog_validate',ROOT/'scripts/validate.py')
validate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)

class CatalogueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.projects=validate.load('projects.json')
        cls.sources=validate.load('sources.json')
        cls.artifacts=validate.load('artifacts.json')
        cls.meta=validate.load('metadata.json')
        cls.i18n=validate.load('i18n.json')
        cls.media=validate.load('media.json')
        cls.tag_taxonomy=validate.load('tag_taxonomy.json')
        cls.by_id={p['id']:p for p in cls.projects}

    def test_schema(self):
        self.assertEqual(validate.validate_data(self.projects,self.sources,self.artifacts,self.meta),[])

    def test_complete_bilingual_gallery_data(self):
        self.assertEqual(validate.validate_presentation(self.projects,self.sources,self.i18n,self.media,validate.load('publication_dates.json'),self.tag_taxonomy),[])
        self.assertEqual(set(self.i18n['en']),set(self.by_id))
        self.assertTrue({'P01','P02','P03','P04','P05'}.issubset(self.media['media']))

    def test_scene_tags_are_complete_and_source_bounded(self):
        allowed={'sim','real'}
        self.assertTrue(all(set(p['scene_tags'])<=allowed and p['scene_tags'] for p in self.projects))
        self.assertEqual(sum('sim' in p['scene_tags'] for p in self.projects),21)
        self.assertEqual(sum('real' in p['scene_tags'] for p in self.projects),18)
        self.assertEqual(sum(set(p['scene_tags'])==allowed for p in self.projects),5)
        self.assertEqual(self.by_id['P12']['scene_tags'],['real'])
        self.assertEqual(self.by_id['P15']['scene_tags'],['sim','real'])
        ledger=(ROOT/'docs/SCENE_TAGS.md').read_text(encoding='utf-8')
        self.assertIn('P06 的两个标签',ledger)
        self.assertIn('X01–X04',ledger)

    def test_workflow_tags_are_complete_and_factual(self):
        labels=self.tag_taxonomy['labels']
        category_tags=self.tag_taxonomy['category_tags']
        self.assertEqual(set(category_tags),validate.CATEGORIES)
        self.assertTrue(all(tags and set(tags)<=set(labels) for tags in category_tags.values()))
        self.assertEqual(category_tags['real2sim'],['real-to-sim','replay'])
        self.assertEqual(category_tags['coding_evaluation'],['evaluation','code-generation'])
        ledger=(ROOT/'docs/TAGS.md').read_text(encoding='utf-8')
        self.assertIn('| P08 | sim | real-to-sim, replay |',ledger)
        self.assertIn('| X08 | sim | rl-training, dexterous |',ledger)

    def test_retained_media_manifest_has_expected_covers_and_videos(self):
        retained=[item for item in self.media['media'].values() if item['kind'] in {'image','video'}]
        self.assertEqual(len(retained),34)
        self.assertEqual(sum(item['kind']=='image' for item in retained),15)
        self.assertEqual(sum(item['kind']=='video' for item in retained),19)
        videos={pid:item for pid,item in self.media['media'].items() if item['kind']=='video'}
        self.assertEqual(len(videos),19)
        self.assertTrue(all(item.get('poster','').startswith('assets/') for item in videos.values()))
        self.assertTrue(all((ROOT/'site'/item['poster']).is_file() for item in videos.values()))
        self.assertTrue(all('first decoded frame at 00:00:00' in item.get('source_path','') for item in videos.values()))
        self.assertEqual({pid:videos[pid]['poster'] for pid in ('P01','P08','P10','P12')},{
            'P01':'assets/posters/P01.jpg','P08':'assets/posters/P08.jpg',
            'P10':'assets/posters/P10.jpg','P12':'assets/posters/P12.jpg',
        })
        social_video_names={
            'X01':'Physical Robot Keyboard Typing.mp4',
            'X02':'Physical Ethernet Insertion.mp4',
            'X03':'Robot Arm Draws the Golden Gate Bridge.mp4',
            'X04':'Cross-Scene Mobile Manipulation ICL.mp4',
            'X05':'G1 Coke-Bottle Grasp.mp4',
            'X06':'G1 Navigation.mp4',
            'X08':'Sharpa Dexterous-Hand Pen Spinning PPO.mp4',
            'X09':'Go1 Paused-Physics Joint Control.mp4',
            'X10':'CARLA Visual Waypoint Driving.mp4',
            'X11':'Two-Robot Ball Toss.mp4',
            'X12':'G1 Bicycle-Control Code.mp4',
            'X13':'Dual-ALOHA Spatial-Constraint Demo.mp4',
            'X14':'Office Scene to Newton  G1.mp4',
            'X15':'savetwt.com_2100754714971287557_640x360.mp4',
        }
        social_video_ids=set(social_video_names)
        self.assertTrue(all(self.media['media'][pid]['url'].startswith('assets/social/') for pid in social_video_ids))
        self.assertEqual({pid:unquote(self.media['media'][pid]['url']).removeprefix('assets/social/') for pid in social_video_ids},social_video_names)
        self.assertTrue(all(' ' not in self.media['media'][pid]['url'] for pid in social_video_ids))
        self.assertTrue(all(self.media['media'][pid]['poster']==f'assets/social/{pid}.jpg' for pid in social_video_ids))
        self.assertTrue(all((ROOT/'site'/unquote(self.media['media'][pid]['url'])).is_file() or validate.optional_lightweight_media(self.media['media'][pid]) for pid in social_video_ids))
        self.assertTrue(all((ROOT/'site'/self.media['media'][pid]['poster']).is_file() for pid in social_video_ids))
        self.assertEqual(self.media['media']['X07']['kind'],'image')
        self.assertEqual(self.media['media']['X07']['url'],'assets/social/SaveTwitter.Net_HST8HsrawAAkgPu.jpg')
        self.assertTrue((ROOT/'site'/self.media['media']['X07']['url']).is_file() or validate.optional_lightweight_media(self.media['media']['X07']))
        self.assertEqual(self.media['media']['X13']['kind'],'video')
        self.assertTrue(all(item['url'].startswith('https://') or item['url'].startswith(('assets/social/','assets/posters/')) for item in retained))
        additions={f'P{i:02}' for i in range(13,18)}
        self.assertTrue(all(self.media['media'][pid]['source_page_url'].startswith('https://') for pid in additions))
        self.assertTrue(all(self.media['media'][pid]['source_path'] for pid in additions))
        self.assertIn('not an experiment demonstration',self.media['media']['P15']['classification'])

    def test_new_cards_keep_source_media_and_cover_provenance(self):
        p18=self.by_id['P18']
        self.assertEqual(p18['links']['post'],'https://x.com/chooi_jeq/status/2101118049944543545')
        self.assertEqual(p18['code_url'],'https://github.com/robocurve/roboharm')
        self.assertEqual(self.media['media']['P18']['url'],'assets/social/wujie2.mp4')
        self.assertIn('b372896be1a04201f8e0a891d8ab60ae94ed2fc2ed537e455d6dcf5b8c7a21f1',self.media['media']['P18']['source_path'])
        self.assertEqual(self.media['media']['P19']['fit'],'contain')
        self.assertIn('page 4, Fig. 3',self.media['media']['P19']['source_path'])
        self.assertIn('not a video frame',self.media['media']['P19']['classification'])
        self.assertEqual(self.by_id['X15']['url'],'https://x.com/frankzydou/status/2100754714971287557')
        self.assertEqual(self.media['media']['X15']['url'],'assets/social/savetwt.com_2100754714971287557_640x360.mp4')
        self.assertIn('f9f554b52f32eb66dd19e5e0475db11d989eb08e1e314c0802e7f0a0f7bd36c3',self.media['media']['X15']['source_path'])
        self.assertEqual(self.meta['window_start'],'2026-08-20')
        self.assertEqual(self.meta['window_end'],'2026-09-20')

    def test_initial_snapshot_counts(self):
        if self.meta['version']!='0.1.0':
            self.skipTest('Initial snapshot count fixture applies only to 0.1.0.')
        self.assertEqual(Counter(p['section'] for p in self.projects),{'core':12,'supporting':7,'watchlist':14,'rednote_leads':8})
        self.assertEqual(len(self.artifacts),8)
        self.assertEqual(len(self.sources),51)
        self.assertEqual(len(validate.load('search-log.json')['queries']),34)

    def test_catalogue_excludes_awesome_collection_pseudo_cards(self):
        removed={'R01','R02','R03','R04','R05','R06','R07','R08'}
        self.assertTrue(removed.isdisjoint(self.by_id))
        self.assertEqual(Counter(p['section'] for p in self.projects),{'core':14,'supporting':5,'watchlist':15})
        self.assertFalse(any(p['section']=='rednote_leads' for p in self.projects))
        self.assertNotIn('小红书待核实线索 · 0',(ROOT/'docs/CATALOG.md').read_text(encoding='utf-8'))
        repositories={}
        for project in self.projects:
            repository=validate.normalized_repository_url(project['url'])
            if repository:
                self.assertNotIn(repository,repositories,(repository,repositories.get(repository),project['id']))
                repositories[repository]=project['id']
        # Every retained Social post is a distinct exact status target. X13's
        # target was supplied by the user and is retained without claiming an
        # independent content verification.
        self.assertEqual(urlsplit(self.by_id['X01']['url']).netloc,'x.com')
        self.assertNotEqual(self.by_id['X01']['url'],self.by_id['X02']['url'])
        social=[self.by_id[f'X{n:02d}'] for n in (*range(1,7),*range(8,16))]
        verified=[p for p in social if '/status/' in p['url']]
        self.assertEqual(len(verified),14)
        self.assertEqual(len({p['url'] for p in verified}),14)
        self.assertEqual(self.by_id['X13']['links'],{})
        self.assertEqual(self.by_id['X13']['url'],'https://x.com/qineng_wang/status/2099893504658866561')
        self.assertIn('S052',self.by_id['X13']['source_ids'])

    def test_no_claimed_independent_experiment(self):
        if self.meta['independent_experiments_run']==0:
            self.assertTrue(all(p['independently_reproduced'] is False for p in self.projects))

    def test_source_references_exist(self):
        ids={s['id'] for s in self.sources}
        self.assertTrue(all(set(p['source_ids'])<=ids for p in self.projects))
        self.assertTrue(all(set(a['source_ids'])<=ids for a in self.artifacts))

    def test_unknown_dates_remain_unknown(self):
        self.assertIsNone(self.by_id['P12']['event_date'])
        self.assertEqual(self.by_id['P12']['window_status'],'date_unconfirmed')

    def test_rednote_is_not_primary(self):
        for p in self.projects:
            if p['section']=='rednote_leads':
                self.assertEqual(p['evidence_level'],'D')
                self.assertEqual(p['metrics'],[])

    def test_same_name_projects_are_distinct(self):
        urls=[self.by_id[x]['url'] for x in ['P01','P02','P03']]
        self.assertEqual(len(set(urls)),3)

    def test_score_denominator_is_not_success_denominator(self):
        metrics={m['name']:m for m in self.by_id['P02']['metrics']}
        self.assertIn('48',metrics['Direct mean Score']['denominator'])
        self.assertIn('50',metrics['Direct success']['denominator'])
        self.assertIn('not token',metrics['GPT correction fraction']['protocol'])

    def test_detects_bad_source(self):
        p=copy.deepcopy(self.projects)
        p[0]['source_ids']=['MISSING']
        self.assertTrue(any('unknown source' in e for e in validate.validate_data(p,self.sources,self.artifacts,self.meta)))

    def test_detects_impossible_success_count(self):
        p=copy.deepcopy(self.projects)
        next(x for x in p if x['id']=='P04')['metrics'][0]['value']=21
        self.assertTrue(any('successes outside denominator' in e for e in validate.validate_data(p,self.sources,self.artifacts,self.meta)))

    def test_bad_dates_and_urls(self):
        self.assertFalse(validate.valid_date('2026-09-31'))
        self.assertTrue(validate.valid_date('2026-09',True))
        self.assertFalse(validate.valid_url('javascript:alert(1)'))
        self.assertFalse(validate.valid_url('https://user:secret@example.com'))
        self.assertTrue(validate.valid_url('https://github.com/robocurve/inspect-robots'))

    def test_local_markdown_links(self):
        self.assertEqual(validate.check_local_markdown(),[])

    def test_csv_round_trip(self):
        with (ROOT/'data/projects.csv').open(encoding='utf-8',newline='') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual([r['id'] for r in rows],[p['id'] for p in self.projects])
        self.assertEqual(rows[0]['title'],self.projects[0]['title'])

    def test_html_embedded_data(self):
        text=(ROOT/'site/index.html').read_text(encoding='utf-8')
        match=re.search(r'<script id="catalog-data" type="application/json">(.*?)</script>',text,re.S)
        self.assertIsNotNone(match)
        data=json.loads(match.group(1))
        self.assertEqual(data['projects'],self.projects)
        self.assertEqual(data['i18n'],self.i18n)
        self.assertEqual(set(data['media']),set(self.by_id))
        self.assertEqual(set(data['topic_tags']),set(self.by_id))
        self.assertEqual(data['topic_tags']['P08'],['real-to-sim','replay'])
        self.assertEqual(data['tag_labels']['real-to-sim']['zh'],'真转仿')
        self.assertNotIn('__CATALOG_JSON__',text)
        self.assertNotRegex(text,r'<script[^>]+src=')
        self.assertNotIn('fetch(',text)

    def test_gallery_language_media_and_subpath_contract(self):
        template=(ROOT/'site/template.html').read_text(encoding='utf-8')
        generated=(ROOT/'site/index.html').read_text(encoding='utf-8')
        self.assertIn("localStorage.getItem(store)||browserLang()",template)
        self.assertIn('navigator.languages',template)
        self.assertIn("if(candidate==='en'||candidate==='zh')return candidate",template)
        self.assertIn("img.addEventListener('error'",template)
        self.assertIn("video.addEventListener('error'",template)
        self.assertIn('function linkKind(key,url)',template)
        self.assertIn("if(host==='github.com')return'code'",template)
        self.assertIn("function projectLinks(p)",template)
        self.assertIn("['paper','code','project']",template)
        self.assertIn("displayLinks(p).forEach",template)
        self.assertIn('function displayLinks(p)',template)
        self.assertIn("function groupFor(p)",template)
        self.assertIn("if(['X07','X15'].includes(p.id))return'social'",template)
        self.assertIn("data-group=\"projects\"",template)
        self.assertIn("data-group=\"social\"",template)
        self.assertIn("let group='projects'",template)
        self.assertIn('scene_tags',template)
        self.assertIn('function projectTags(p)',template)
        self.assertIn('DATA.topic_tags[p.id]',template)
        self.assertIn('DATA.tag_labels[tag]',template)
        self.assertIn('function matchesQuery(p)',template)
        self.assertIn('DATA.i18n.en[p.id].title',template)
        self.assertIn('queryTerms().every',template)
        self.assertIn('id="query"',template)
        self.assertIn('id="clear-query"',template)
        self.assertIn('aria-label="GitHub repository"',template)
        self.assertIn('https://github.com/slelly/awesome-GPT6-for-embodiedAI',template)
        self.assertNotIn("Author profile",template)
        self.assertNotIn('DETAIL_COPY',template)
        self.assertNotIn('openDetail',template)
        self.assertNotIn('detail-dialog',template)
        self.assertNotIn('<dialog',template)
        self.assertNotIn('View details',template)
        self.assertNotIn('查看详情',template)
        self.assertIn('function imageBox(item)',template)
        self.assertNotIn('media-summary',template)
        self.assertNotIn('highlight=',template)
        self.assertNotIn("image_source:'Image source'",template)
        self.assertNotIn("image_source:'图片来源'",template)
        self.assertNotIn('showModal',template)
        self.assertIn('function linkLabel',template)
        self.assertNotIn('id="evidence"',template)
        self.assertNotIn('id="environment"',template)
        self.assertNotIn('id="detail-grid"',template)
        self.assertNotIn('id="metrics"',template)
        self.assertNotIn('id="reset"',template)
        self.assertNotIn('class="notice"',template)
        self.assertNotIn('class="toolbar"',template)
        self.assertNotIn("text('evidence')+' '+p.evidence_level",template)
        self.assertNotRegex(template,r'(?:src|href)="/(?!/)')
        self.assertNotRegex(generated,r'(?:src|href)="/(?!/)')

    def test_awesome_readme_and_pages_gates(self):
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        pages=(ROOT/'.github/workflows/pages.yml').read_text(encoding='utf-8')
        validate_workflow=(ROOT/'.github/workflows/validate.yml').read_text(encoding='utf-8')
        self.assertIn('[![Awesome](https://awesome.re/badge.svg)]',readme)
        self.assertIn('[中文版本 / Chinese](README.zh-CN.md)',readme)
        self.assertIn('## Contents',readme)
        self.assertIn('docs/MEDIA.md',readme)
        self.assertIn('docs/TAGS.md',readme)
        self.assertIn('docs/PUBLICATION_DATES.md',readme)
        self.assertNotIn('docs/ASTRA_RELEVANCE_REVIEW.md',readme)
        self.assertIn('workflow_dispatch:',pages)
        self.assertIn('path: site',pages)
        self.assertTrue((ROOT/'docs/SOCIAL_LINKS.md').is_file())
        self.assertIn('python -m unittest discover -s tests -v',pages)
        self.assertIn('docs/MEDIA.md',pages)
        self.assertIn('docs/MEDIA.md',validate_workflow)
        self.assertIn('34 entries:',readme)
        self.assertIn('34 条', (ROOT/'README.zh-CN.md').read_text(encoding='utf-8'))

    def test_network_probe_is_opt_in(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/check_links.py')],capture_output=True,text=True,timeout=10)
        self.assertNotEqual(p.returncode,0)
        self.assertIn('opt-in',p.stderr)

    def test_build_is_deterministic(self):
        paths=['docs/CATALOG.md','docs/SOURCES.md','docs/HUGGING_FACE.md','docs/MEDIA.md','data/projects.csv','site/index.html']
        before={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
        subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],check=True,capture_output=True,timeout=10)
        after={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
        self.assertEqual(before,after)

if __name__=='__main__':
    unittest.main()
