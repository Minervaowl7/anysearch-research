#!/usr/bin/env python3
"""Offline package checks. Does not open network connections or invoke models."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import struct
import sys
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
ENDPOINT='https://api.anysearch.com/mcp'
SKIP_DIRS={'__pycache__','.git','.venv','node_modules','dist','.agents','.github'}

def package_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob('*') if p.is_file()
        and not any(x in SKIP_DIRS for x in p.relative_to(root).parts)
        and p.suffix not in {'.pyc','.pyo','.zip','.gz'})

def _pairs(pairs: list[tuple[str,Any]]) -> dict[str,Any]:
    obj={}
    for k,v in pairs:
        if k in obj: raise ValueError('duplicate JSON key: '+k)
        obj[k]=v
    return obj

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=_pairs)

def validate(root: Path) -> list[str]:
    root=root.resolve(); errors=[]
    def need(ok: bool,msg: str) -> None:
        if not ok: errors.append(msg)
    def contained(base: Path,value: str) -> Path | None:
        if not value or '\\' in value or '\x00' in value: return None
        p=(base/value).resolve()
        return p if p.is_relative_to(root) else None
    if not root.is_dir(): return ['invalid package root']
    for p in root.rglob('*'):
        if any(x in SKIP_DIRS for x in p.relative_to(root).parts): continue
        need(not p.is_symlink(),'symlink: '+p.name)
        need(not (p.name=='.env' or p.name.startswith('.env.') or p.suffix in {'.key','.pem'}),'potential secret file: '+p.name)
    files=package_files(root)
    need(sum(p.stat().st_size for p in files)<=10*1024*1024,'package exceeds 10 MiB')
    data={}
    for p in files:
        if p.suffix=='.json':
            try: data[p.relative_to(root).as_posix()]=read_json(p)
            except (OSError,ValueError) as e: errors.append(str(p.relative_to(root))+': '+str(e))
    m=data.get('plugin.json')
    if not isinstance(m,dict): return errors+['missing or invalid plugin.json']
    allowed={'$schema','name','version','description','author','homepage','repository','license','keywords','extensions'}
    need(not set(m)-allowed,'unexpected portable manifest field')
    need(m.get('$schema')=='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json','invalid manifest schema')
    need(m.get('name')==root.name=='anysearch-research','identity/root mismatch')
    v=m.get('version')
    need(isinstance(v,str) and bool(re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?',v)),'invalid semantic version')
    try:
        ext=m['extensions']['com.openai']; ui=ext['interface']
        need(set(ext)=={'interface'},'unexpected OpenAI extension field')
        need(bool(ui.get('displayName')),'missing displayName')
        sub=ui.get('shortDescription')
        need(isinstance(sub,str) and 1<=len(sub)<=30,'invalid subtitle length')
        prompts=ui.get('defaultPrompt')
        need((isinstance(prompts,str) and bool(prompts.strip())) or (isinstance(prompts,list) and 1<=len(prompts)<=3 and all(isinstance(x,str) and x.strip() for x in prompts)),'invalid default prompts')
        need(ui.get('capabilities')==['Read'],'unexpected capabilities')
        for field in ['logo','composerIcon']:
            value=ui.get(field); p=contained(root,value) if isinstance(value,str) else None
            need(bool(isinstance(value,str) and value.startswith('./assets/') and p and p.is_file()),'invalid '+field+' path')
            if p and p.is_file():
                raw=p.read_bytes()
                need(24<=len(raw)<=5*1024*1024 and raw[:8]==b'\x89PNG\r\n\x1a\n','invalid PNG '+field)
                if len(raw)>=24:
                    w,h=struct.unpack('>II',raw[16:24]);need(w==h and 48<=w<=4096,'invalid '+field+' dimensions')
    except (KeyError,TypeError,AttributeError) as e: errors.append('invalid interface: '+str(e))
    mc=data.get('mcp.json')
    if not isinstance(mc,dict): errors.append('missing mcp.json')
    else:
        need(set(mc)=={'$schema','mcpServers'},'invalid MCP root fields')
        need(mc.get('$schema')=='https://agent-plugins.org/schemas/1.0.0/mcp.schema.json','invalid MCP schema')
        servers=mc.get('mcpServers',{})
        if not isinstance(servers,dict): errors.append('invalid MCP server map');servers={}
        need(set(servers)=={'anysearch'},'unexpected MCP server')
        server=servers.get('anysearch',{})
        if not isinstance(server,dict): errors.append('invalid MCP server');server={}
        need(set(server)=={'type','url','headers'},'invalid MCP server fields')
        need(server.get('type')=='streamable-http','wrong MCP transport')
        need(server.get('url')==ENDPOINT,'unapproved MCP endpoint')
        need(server.get('headers')=={'X-Anysearch-Client':'mcp/1.0.0'},'unexpected headers or credentials')
    need(not (root/'.app.json').exists(),'unverified app binding')
    need(not (root/'hooks').exists(),'runtime hooks forbidden')
    skills=list((root/'skills').glob('*/SKILL.md'));need(len(skills)==2,'expected two skills')
    for p in skills:
        text=p.read_text(encoding='utf-8'); match=re.match(r'\A---\n(.*?)\n---\n',text,re.S)
        need(bool(match),'missing frontmatter')
        if match:
            name=re.search(r'^name:\s*(\S+)\s*$',match[1],re.M)
            need(bool(name and name[1]==p.parent.name),'skill name mismatch')
            need(bool(re.search(r'^description:\s*\S.+$',match[1],re.M)),'missing description')
        need(len(text.encode())<=18000,'skill too large')
    for p in files:
        if p.suffix=='.md':
            for raw in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
                url=raw.split(' ',1)[0]
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',url) or url.startswith('#'): continue
                target=contained(p.parent,url.split('#',1)[0])
                need(bool(target and target.is_file()),'broken/escaping reference: '+url)
    status=data.get('evidence/status.json',{})
    snapshot=status.get('contract_snapshot','')
    need(isinstance(snapshot,str) and snapshot.startswith('evidence/') and snapshot in data,'missing current contract snapshot')
    discovery=data.get(snapshot,{}) if isinstance(snapshot,str) else {}
    need(discovery.get('endpoint')==ENDPOINT,'discovery endpoint mismatch')
    need(discovery.get('initialize_status')=='PASS' and discovery.get('tools_list_status')=='PASS','missing discovery evidence')
    tools=discovery.get('tools',[])
    names=[t.get('name') for t in tools]
    need({'search','batch_search','get_sub_domains','extract','score'}<=set(names),'missing captured tool')
    need(len(names)==len(set(names)),'duplicate captured tool')
    for t in tools:
        a=t.get('annotations',{})
        need(all(isinstance(a.get(k),bool) for k in ['readOnlyHint','destructiveHint','idempotentHint','openWorldHint']),'invalid tool annotation')
    score=next((t for t in tools if t.get('name')=='score'),{})
    try:
        schema=score['inputSchema'];f=schema['properties']['feedbacks'];p=f['items']['properties']
        need(schema['required']==['feedbacks'] and f['minItems']==1 and f['maxItems']==10,'invalid feedback batch contract')
        need(set(f['items']['required'])=={'request_id','score'},'invalid feedback fields')
        need(p['score']['type']=='integer' and p['score']['minimum']==1 and p['score']['maximum']==5,'invalid feedback score bounds')
        need(p['request_id']['type']=='string','invalid feedback request identifier')
    except (KeyError,TypeError): errors.append('missing feedback contract')
    need(status.get('package_version')==m.get('version'),'evidence version mismatch')
    acceptance=status.get('production_acceptance')
    need(acceptance in {'NOT_COMPLETE','COMPLETE'},'invalid acceptance status')
    if acceptance=='COMPLETE':
        need(all(status.get(k)=='PASS' for k in ['live_search','live_batch_search','live_get_sub_domains','live_extract','live_score','authenticated_access','target_host_end_to_end','behavior_cases']),'release overclaim: acceptance incomplete')
    cases=data.get('tests/behavior-cases.json',[])
    need(isinstance(cases,list) and len(cases)>=20,'missing behavior cases')
    if isinstance(cases,list):
        ids=[c.get('id') for c in cases]
        need(all(isinstance(x,str) and x for x in ids) and len(ids)==len(set(ids)),'invalid behavior case IDs')
        runs=data.get('evidence/behavior-results.json',[])
        need(isinstance(runs,list),'invalid behavior results')
        if isinstance(runs,list):
            for run in runs:
                need(run.get('case_id') in ids,'unknown behavior case result')
                need(run.get('status') in {'PASS','FAIL','ERROR','PARTIAL','NOT_RUN'},'invalid behavior result status')
                need(bool(run.get('date')) and bool(run.get('observation')),'missing behavior result evidence')
    for name in ['README.md','README_zh.md','SECURITY.md','LICENSE','CHANGELOG.md','MAINTAINING.md','tools/validate_package.py','tools/build_package.py','tests/test_package.py','evidence/VERIFICATION.md']:
        need((root/name).is_file(),'missing required file: '+name)
    return errors

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args();errors=validate(args.root)
    if errors: print('\n'.join('FAIL: '+x for x in errors));return 1
    print(f'PASS: offline validation; {len(package_files(args.root))} files; no network or models.');return 0
if __name__=='__main__': sys.exit(main())
