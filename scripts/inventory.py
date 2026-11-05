#!/usr/bin/env python3
"""Inventário estático de metadados, sem abrir conteúdo de código ou segredos."""
import argparse, json, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

SKIP={'.git','.env','.ssh','.aws','.kube','node_modules','vendor','dist','build','target','.next','.venv','venv','__pycache__','.terraform','.gradle','.idea','.vscode','coverage','private','secrets'}
SENSITIVE={'id_rsa','id_ed25519','credentials','credentials.json','secrets.json','key.pem','privkey.pem','fullchain.pem','.npmrc','.pypirc','.netrc'}
MANIFESTS={'package.json','package-lock.json','pnpm-lock.yaml','yarn.lock','pyproject.toml','requirements.txt','Pipfile','Pipfile.lock','poetry.lock','go.mod','go.sum','Cargo.toml','Cargo.lock','pom.xml','build.gradle','build.gradle.kts','settings.gradle','Gemfile','composer.json','Dockerfile','docker-compose.yml','docker-compose.yaml','compose.yml','compose.yaml','openapi.yaml','openapi.json','swagger.yaml','schema.prisma','manage.py','Makefile','CMakeLists.txt'}
EXT={'.py':'Python','.js':'JavaScript','.jsx':'JavaScript JSX','.ts':'TypeScript','.tsx':'TypeScript TSX','.java':'Java','.kt':'Kotlin','.go':'Go','.rs':'Rust','.cs':'C#','.php':'PHP','.rb':'Ruby','.dart':'Dart','.swift':'Swift','.sql':'SQL','.vue':'Vue','.svelte':'Svelte','.html':'HTML','.css':'CSS','.sh':'Shell','.ps1':'PowerShell'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--out',required=True);ap.add_argument('--max-files',type=int,default=20000);args=ap.parse_args()
 root=Path(args.root).resolve();out=Path(args.out).resolve()
 if not root.is_dir():ap.error('Diretório de projeto inexistente')
 if out==root or root in out.parents: ap.error('Saída deve ficar fora do projeto para evitar alteração do repositório')
 counts={};manifests=[];sample=[];n=0;truncated=False
 for base,dirs,files in os.walk(root,followlinks=False):
  dirs[:]=sorted(d for d in dirs if d not in SKIP and not d.startswith('.') and not (Path(base)/d).is_symlink())
  for filename in sorted(files):
   if n>=args.max_files:truncated=True;break
   path=Path(base)/filename
   if path.is_symlink() or filename in SENSITIVE or filename.startswith('.env') or filename.endswith(('.pem','.key','.p12','.pfx','.jks','.keystore')):continue
   try:
    st=path.stat()
    if not path.is_file() or st.st_size>10*1024*1024:continue
    rel=path.relative_to(root).as_posix()
   except (OSError,ValueError):continue
   n+=1
   if path.suffix.lower() in EXT:counts[EXT[path.suffix.lower()]]=counts.get(EXT[path.suffix.lower()],0)+1
   if filename in MANIFESTS:manifests.append(rel)
   if len(sample)<150:sample.append(rel)
  if truncated:break
 result={'schema_version':'1.0','generated_utc':datetime.now(timezone.utc).isoformat(),'root':str(root),'total_files_scanned':n,'truncated':truncated,'language_file_counts':dict(sorted(counts.items())),'manifest_paths':manifests[:1000],'sample_paths':sample,'limitations':['Inventário por extensão e nomes de manifests; não comprova uso efetivo, versões ou arquitetura.','Conteúdo de arquivos e segredos não são extraídos.']}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out)
if __name__=='__main__':main()
