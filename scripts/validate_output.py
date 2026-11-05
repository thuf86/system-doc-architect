#!/usr/bin/env python3
"""Validação heurística; não substitui inspeção visual ou revisão de segurança."""
import argparse,json,re
from pathlib import Path
from datetime import datetime,timezone
MODULES=['01_arquitetura','02_inventario_tecnologico','03_apis_integracoes','04_banco_de_dados','05_infraestrutura_devops','06_seguranca_governanca','07_regras_de_negocio','08_testes_qualidade','09_manual_tecnico_operacional','10_manual_usuario']
PATTERNS=[('private_key',re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),('cloud_key',re.compile(r'AKIA[0-9A-Z]{16}')),('token_assignment',re.compile(r'(?i)(?:password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*["\x27]?[A-Za-z0-9_./+\-=]{12,}'))]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--dir',required=True);ap.add_argument('--mode',choices=['auditoria','completo','atualizacao'],default='completo');a=ap.parse_args();root=Path(a.dir).resolve()
 if not root.is_dir():ap.error('Diretório inexistente')
 md=list(root.glob('*.md'));pdf=list((root/'pdf').glob('*.pdf')) if (root/'pdf').is_dir() else []
 required=['00_auditoria'] if a.mode=='auditoria' else ['00_documento_mestre']+MODULES
 missing=[n for n in required if not (root/(n+'.md')).exists()]
 findings=[]
 for f in md:
  content=f.read_text(encoding='utf-8',errors='replace')
  if len(content.strip())<100:findings.append({'file':f.name,'issue':'Documento muito curto'})
  for name,pat in PATTERNS:
   if pat.search(content):findings.append({'file':f.name,'issue':'Possível segredo: '+name})
 for f in pdf:
  try:
   if f.stat().st_size<1000 or f.open('rb').read(5)!=b'%PDF-':findings.append({'file':f.name,'issue':'PDF possivelmente inválido'})
  except OSError:findings.append({'file':f.name,'issue':'PDF ilegível'})
 if not pdf:findings.append({'issue':'Nenhum PDF encontrado'})
 report={'generated_utc':datetime.now(timezone.utc).isoformat(),'mode':a.mode,'missing_markdown':missing,'markdown_count':len(md),'pdf_count':len(pdf),'findings':findings,'passed_basic_checks':not missing and not findings,'warning':'Checagem heurística; revisão humana de segredos, evidências, paginação e diagramas continua obrigatória.'}
 out=root/'validation_report.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(0 if report['passed_basic_checks'] else 1)
if __name__=='__main__':main()
