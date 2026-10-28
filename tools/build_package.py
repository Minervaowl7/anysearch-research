#!/usr/bin/env python3
"""Deterministic, offline ZIP builder. Does not upload the package."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from validate_package import ROOT, package_files, validate

def build(root: Path, output: Path) -> dict[str,str|int]:
    root=root.resolve();output=output.resolve()
    if output.is_relative_to(root): raise ValueError('Archive must be outside the plugin root.')
    if output.suffix.lower()!='.zip': raise ValueError('Output must end in .zip.')
    errors=validate(root)
    if errors: raise ValueError('Invalid package:\n'+'\n'.join(errors))
    output.parent.mkdir(parents=True,exist_ok=True)
    members=package_files(root)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in members:
            n=(Path(root.name)/p.relative_to(root)).as_posix()
            info=zipfile.ZipInfo(n,date_time=(1980,1,1,0,0,0))
            info.create_system=3;info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(output) as z:
        bad=z.testzip()
        if bad: raise ValueError('ZIP CRC error: '+bad)
    return {'path':str(output),'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'files':len(members)}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try: print(json.dumps(build(ROOT,args.output),indent=2));return 0
    except (OSError,ValueError) as e: print(str(e),file=sys.stderr);return 1
if __name__=='__main__': sys.exit(main())
