"""Offline structural and contract-regression checks, not live service tests."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate_package import validate, read_json
from build_package import build

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'anysearch-research'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.git'))
    def edit(self,name,fn):
        p=self.root/name; data=read_json(p);fn(data);p.write_text(json.dumps(data),encoding='utf-8')
    def contract(self):
        return read_json(self.root/'evidence/status.json')['contract_snapshot']
    def tools(self):
        return read_json(self.root/self.contract())['tools']
    def bad(self,text):
        self.assertTrue(any(text in x for x in validate(self.root)),validate(self.root))
    def test_baseline(self): self.assertEqual(validate(self.root),[])
    def test_identity(self): self.edit('plugin.json',lambda x:x.update(name='renamed'));self.bad('identity')
    def test_semver(self): self.edit('plugin.json',lambda x:x.update(version='release1'));self.bad('semantic')
    def test_unknown_portable_field(self): self.edit('plugin.json',lambda x:x.update(skills='./skills/'));self.bad('unexpected portable')
    def test_duplicate_json_key(self):
        p=self.root/'plugin.json';p.write_text(p.read_text(encoding='utf-8').replace('"name":','"name":"duplicate", "name":',1),encoding='utf-8');self.bad('duplicate JSON')
    def test_subtitle(self): self.edit('plugin.json',lambda x:x['extensions']['com.openai']['interface'].update(shortDescription='x'*31));self.bad('subtitle')
    def test_default_prompts(self): self.edit('plugin.json',lambda x:x['extensions']['com.openai']['interface'].update(defaultPrompt=['a']*4));self.bad('default prompts')
    def test_missing_logo(self): (self.root/'assets/logo.png').unlink();self.bad('logo')
    def test_icon_escape(self): self.edit('plugin.json',lambda x:x['extensions']['com.openai']['interface'].update(logo='../secret.png'));self.bad('logo')
    def test_small_icon(self):
        p=self.root/'assets/icon.png';data=bytearray(p.read_bytes());data[16:24]=(16).to_bytes(4,'big')*2;p.write_bytes(data);self.bad('dimensions')
    def test_wrong_transport(self): self.edit('mcp.json',lambda x:x['mcpServers']['anysearch'].update(type='sse'));self.bad('transport')
    def test_wrong_endpoint(self): self.edit('mcp.json',lambda x:x['mcpServers']['anysearch'].update(url='http://localhost/mcp'));self.bad('endpoint')
    def test_no_embedded_credentials(self): self.edit('mcp.json',lambda x:x['mcpServers']['anysearch']['headers'].update(Authorization='Bearer dummy_test_only'));self.bad('credentials')
    def test_no_extra_server(self): self.edit('mcp.json',lambda x:x['mcpServers'].update(other={'type':'stdio','command':'x'}));self.bad('unexpected MCP')
    def test_no_secret_file(self): (self.root/'.env').write_text('TEST_ONLY=not_a_secret');self.bad('potential secret')
    def test_no_symlink(self):
        try: (self.root/'assets/alias.png').symlink_to(self.root/'assets/icon.png')
        except OSError as e:
            if sys.platform=='win32' and getattr(e,'winerror',None)==1314: self.skipTest('Windows symlink privilege unavailable')
            raise
        self.bad('symlink')
    def test_no_hooks(self): (self.root/'hooks').mkdir();self.bad('hooks')
    def test_no_app_binding(self): (self.root/'.app.json').write_text('{}');self.bad('app binding')
    def test_skill_name(self):
        p=self.root/'skills/anysearch-setup/SKILL.md';p.write_text(p.read_text(encoding='utf-8').replace('name: anysearch-setup','name: wrong'),encoding='utf-8');self.bad('name mismatch')
    def test_broken_reference(self):
        p=self.root/'README.md';p.write_text(p.read_text(encoding='utf-8')+'\n[broken](not-present.md)\n',encoding='utf-8');self.bad('broken/escaping')
    def test_missing_tool_snapshot(self): self.edit(self.contract(),lambda x:x['tools'].pop());self.bad('captured tool')
    def test_invalid_annotation(self): self.edit(self.contract(),lambda x:x['tools'][0]['annotations'].update(destructiveHint='false'));self.bad('annotation')
    def test_changed_annotation_allowed(self):
        self.edit(self.contract(),lambda x:x['tools'][0]['annotations'].update(destructiveHint=False));self.assertEqual(validate(self.root),[])
    def test_additional_tool_allowed(self):
        self.edit(self.contract(),lambda x:x['tools'].append(dict(copy.deepcopy(x['tools'][0]),name='future_tool')));self.assertEqual(validate(self.root),[])
    def test_no_false_production_acceptance(self): self.edit('evidence/status.json',lambda x:x.update(production_acceptance='COMPLETE'));self.bad('overclaim')
    def test_record_real_behavior_pass(self):
        self.edit('evidence/behavior-results.json',lambda x:x.append({'case_id':'simple-zh','status':'PASS','date':'2026-10-28','observation':'Synthetic fixture only'}));self.assertEqual(validate(self.root),[])
    def test_unknown_behavior_case(self):
        self.edit('evidence/behavior-results.json',lambda x:x.append({'case_id':'unknown','status':'PASS','date':'2026-10-28','observation':'Synthetic fixture only'}));self.bad('unknown behavior')
    def test_missing_score(self):
        self.edit(self.contract(),lambda x:x.update(tools=[t for t in x['tools'] if t['name']!='score']));self.bad('captured tool')
    def test_score_bounds(self):
        def change(x):
            s=next(t for t in x['tools'] if t['name']=='score')
            s['inputSchema']['properties']['feedbacks']['items']['properties']['score']['maximum']=10
        self.edit(self.contract(),change);self.bad('score bounds')
    def test_score_batch_bounds(self):
        def change(x):
            s=next(t for t in x['tools'] if t['name']=='score')
            s['inputSchema']['properties']['feedbacks']['maxItems']=11
        self.edit(self.contract(),change);self.bad('batch contract')
    def test_reproducible_archives(self):
        parent=Path(self.tmp.name)
        a=build(self.root,parent/'a.zip');b=build(self.root,parent/'b.zip')
        self.assertEqual(a['sha256'],b['sha256'])
        with zipfile.ZipFile(parent/'a.zip') as z:
            self.assertIsNone(z.testzip())
            self.assertTrue(all(n.startswith('anysearch-research/') and '..' not in Path(n).parts for n in z.namelist()))
            self.assertFalse(any('__pycache__' in n or n.endswith('.pyc') for n in z.namelist()))
    def test_archive_must_be_external(self):
        with self.assertRaises(ValueError): build(self.root,self.root/'release.zip')
    def test_invalid_package_not_buildable(self):
        (self.root/'plugin.json').unlink()
        with self.assertRaises(ValueError): build(self.root,Path(self.tmp.name)/'bad.zip')
    def test_search_contract_bounds(self):
        tools=self.tools()
        s=next(t for t in tools if t['name']=='search')['inputSchema']
        self.assertEqual(s['required'],['query'])
        self.assertEqual((s['properties']['max_results']['minimum'],s['properties']['max_results']['maximum']),(1,10))
        self.assertFalse('before' in s['properties'] or 'page' in s['properties'])
    def test_batch_contract_limit(self):
        tools=self.tools()
        t=next(t for t in tools if t['name']=='batch_search')
        self.assertEqual(t['inputSchema']['properties']['queries']['maxItems'],5)
    def test_discovery_contract(self):
        tools=self.tools()
        p=next(t for t in tools if t['name']=='get_sub_domains')['inputSchema']['properties']
        self.assertEqual(p['domains']['maxItems'],5)
        self.assertIn('ip',p['domains']['items']['enum']);self.assertIn('academic',p['domains']['items']['enum'])
    def test_extract_contract(self):
        tools=self.tools()
        t=next(t for t in tools if t['name']=='extract')
        self.assertEqual(t['inputSchema']['required'],['url'])
        self.assertEqual(set(t['outputSchema']['required']),{'title','url','content'})

if __name__=='__main__': unittest.main(verbosity=2)
