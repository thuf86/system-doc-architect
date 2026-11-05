#!/usr/bin/env python3
"""Converte Markdown básico em PDFs paginados com ReportLab, sem executar conteúdo."""
import argparse,re
from pathlib import Path
from xml.sax.saxutils import escape

def build(src,dest):
 from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Preformatted,PageBreak,KeepTogether
 from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
 from reportlab.lib.enums import TA_LEFT
 from reportlab.lib import colors
 from reportlab.lib.pagesizes import A4
 from reportlab.lib.units import mm
 styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='DocTitleCustom',parent=styles['Title'],fontSize=17,leading=22,spaceAfter=15,textColor=colors.HexColor('#17324D')))
 for n,size,lead in [('H1Custom',14,18),('H2Custom',12,16),('H3Custom',10.5,14)]:styles.add(ParagraphStyle(name=n,parent=styles['Heading2'],fontSize=size,leading=lead,spaceBefore=13,spaceAfter=7,textColor=colors.HexColor('#17324D')))
 styles.add(ParagraphStyle(name='BodyCustom',parent=styles['BodyText'],fontSize=9.2,leading=13.5,spaceAfter=7))
 styles.add(ParagraphStyle(name='CodeCustom',fontName='Courier',fontSize=7.5,leading=10,spaceAfter=8))
 story=[];in_code=False;code=[]
 def inline(s):
  s=escape(s)
  s=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',s)
  s=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',s)
  return s
 for line in src.read_text(encoding='utf-8').splitlines():
  if line.strip().startswith('```'):
   if in_code:
    story.append(Preformatted('\n'.join(code)[:12000],styles['CodeCustom'],maxLineLength=100,splitChars=' /,.;'));code=[]
   in_code=not in_code;continue
  if in_code:code.append(line);continue
  if not line.strip():story.append(Spacer(1,3));continue
  if line.startswith('# '):style='DocTitleCustom';line=line[2:]
  elif line.startswith('## '):style='H1Custom';line=line[3:]
  elif line.startswith('### '):style='H2Custom';line=line[4:]
  elif line.startswith('#### '):style='H3Custom';line=line[5:]
  else:style='BodyCustom'
  if line.startswith(('- ','* ')):line='• '+line[2:]
  # markdown tables remain readable as separate paragraphs, rather than claiming full table layout
  if line.startswith('|'):line=line.strip('|').replace('|','  •  ')
  story.append(Paragraph(inline(line),styles[style]))
 if in_code:story.append(Preformatted('\n'.join(code),styles['CodeCustom']))
 def footer(c,doc):
  c.setFont('Helvetica',8);c.setFillColor(colors.grey);c.drawString(19*mm,13*mm,src.stem[:75]);c.drawRightString(192*mm,13*mm,str(doc.page))
 dest.parent.mkdir(parents=True,exist_ok=True)
 doc=SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=19*mm,leftMargin=19*mm,topMargin=19*mm,bottomMargin=20*mm,title=src.stem,author='System Documentation Architect')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 folder=Path(a.input).resolve();output=Path(a.output).resolve()
 if not folder.is_dir():ap.error('Diretório de entrada inexistente')
 files=sorted(folder.glob('*.md'))
 if not files:ap.error('Nenhum arquivo Markdown encontrado')
 try:import reportlab
 except ImportError:ap.error('Dependência ausente: reportlab. Solicite autorização antes de instalar.')
 for f in files:
  target=output/(f.stem+'.pdf');build(f,target);print(target)
if __name__=='__main__':main()
