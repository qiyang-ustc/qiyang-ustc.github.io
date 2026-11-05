#!/usr/bin/env python3
"""Build the public CV from data/public_cv.json (requires reportlab).

Run from any directory: python scripts/build_public_cv.py
The public document deliberately contains academic contact details only.
"""
from pathlib import Path
from html import escape
import json, re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/public_cv.json').read_text())
TARGET = ROOT / 'docs/files/Qi_Yang_CV.pdf'
TARGET.parent.mkdir(parents=True, exist_ok=True)
FONT_ROOT = Path('/System/Library/Fonts/Supplemental')
if (FONT_ROOT / 'Times New Roman.ttf').exists():
    for name, filename in [('CV','Times New Roman.ttf'),('CV-Bold','Times New Roman Bold.ttf'),('CV-Italic','Times New Roman Italic.ttf'),('CV-BoldItalic','Times New Roman Bold Italic.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(FONT_ROOT / filename)))
    pdfmetrics.registerFontFamily('CV',normal='CV',bold='CV-Bold',italic='CV-Italic',boldItalic='CV-BoldItalic')
    FONT, BOLD = 'CV', 'CV-Bold'
else:
    FONT, BOLD = 'Times-Roman', 'Times-Bold'
INK, BLUE, MUTED = (colors.HexColor(s) for s in ['#20262e','#284863','#53616d'])
WIDTH = A4[0] - 100
styles = dict(
    body=ParagraphStyle('body',fontName=FONT,fontSize=10.7,leading=13.4,textColor=INK,spaceAfter=3),
    small=ParagraphStyle('small',fontName=FONT,fontSize=10,leading=12.4,textColor=INK,spaceAfter=3),
    title=ParagraphStyle('title',fontName=BOLD,fontSize=23,leading=27,textColor=INK,spaceAfter=7),
    heading=ParagraphStyle('heading',fontName=BOLD,fontSize=13,leading=16,textColor=BLUE,spaceBefore=12,spaceAfter=7,keepWithNext=True),
    date=ParagraphStyle('date',fontName=FONT,fontSize=10,leading=13.4,textColor=MUTED),
)

def clean(s):
    s=s.replace('<strong>','<b>').replace('</strong>','</b>').replace('<em>','<i>').replace('</em>','</i>')
    return s.replace('<sup>','<super>').replace('</sup>','</super>').replace('–','-').replace('—','-')

def p(text, style='body'):
    return Paragraph(clean(text), styles[style])

def link(label,url):
    if url.startswith('/'):
        url='https://qiyang-ustc.github.io'+url
    return f'<link href="{escape(url,quote=True)}" color="#284863">{escape(label)}</link>'

def row(date,title,body,extra=''):
    content=[p('<b>'+escape(title)+'</b>'),p(escape(body))]
    if extra:
        content.append(p(extra,'small'))
    table=Table([[p(escape(date),'date'),content]],colWidths=[91,WIDTH-91],hAlign='LEFT')
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,-1),10),('RIGHTPADDING',(1,0),(1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return table

story=[p('Qi Yang, Ph.D.','title'),p('Postdoctoral researcher · University of Amsterdam'),
    p(link('q.yang2@uva.nl','mailto:q.yang2@uva.nl')+' · Amsterdam, The Netherlands','small'),
    p(link('qiyang-ustc.github.io','https://qiyang-ustc.github.io/')+' · '+link('GitHub','https://github.com/qiyang-ustc')+' · '+link('ORCID: 0000-0002-7325-3100','https://orcid.org/0000-0002-7325-3100'),'small'),
    p('Research interests','heading'),
    p('Tensor-network methods for quantum many-body physics: long-range interactions and criticality, iMPS and iPEPS, frustrated magnets and quantum spin liquids, numerical linear algebra, automatic differentiation, and scalable scientific computing.'),
    p('Appointments and education','heading')]
story.extend(row(*item) for item in DATA['appointments'])
story.append(p('Supervision and mentoring','heading'))
story.extend(row(*item) for item in DATA['mentoring'])
story.append(p('Research funding and computing','heading'))
story.extend(row(*item) for item in DATA['funding'])
story.append(p('Open-source software','heading'))
story.append(p('Personal projects and contributions to collaborative software.','small'))
for s in DATA['software']:
    story.append(p('<b>'+link(s['name'],s['url'])+'</b> - '+escape(s['description']),'small'))

story += [PageBreak(),p('Publications','title'),p('7 journal articles and 1 preprint. † Equal contribution.','small'),p('Journal articles','heading')]
for index,item in enumerate(DATA['publications'][1:],1):
    authors=item['authors']
    if item['citation'].startswith('Science'):
        authors='Dian Wu, Riccardo Rossi, Filippo Vicentini, <i>et al.</i> (including <b>Qi Yang</b>)'
    block=[p(f'<b>{index}.</b> '+authors+'.'),p('<b>'+escape(item['title'])+'</b>'),p(escape(item['citation'])+'. '+link('DOI: '+item['url'].removeprefix('https://doi.org/'),item['url']),'small'),Spacer(1,8)]
    story.append(KeepTogether(block))
story.append(p('Preprint','heading'))
item=DATA['publications'][0]
story.append(KeepTogether([p('<b>Qi Yang.</b>'),p('<b>'+escape(item['title'])+'</b>'),p(link(item['citation'],item['url']),'small')]))

story += [PageBreak(),p('Talks and academic activities','title')]
for category,label in [('invited','Invited talks and lectures'),('workshop','Workshop talk'),('contributed','Contributed talk')]:
    story.append(p(label,'heading'))
    for t in DATA['talks']:
        if t['category']!=category:
            continue
        extra=' '.join(link(label,url) for label,url in t['links'])
        story.append(row(t['date'],t['title'],t['venue'],extra))
story.append(p('Awards','heading'))
for date,award in DATA['awards']:
    story.append(p('<b>'+date+'</b> - '+escape(award),'small'))

def footer(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#d6dee5'))
    canvas.line(50,43,A4[0]-50,43)
    canvas.setFont(FONT,9)
    canvas.setFillColor(MUTED)
    canvas.drawString(50,29,'Qi Yang | Updated '+DATA['updated'])
    canvas.drawRightString(A4[0]-50,29,str(doc.page))
    canvas.restoreState()

doc=SimpleDocTemplate(str(TARGET),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=39,bottomMargin=56,
    title='Qi Yang - Curriculum Vitae',author='Qi Yang',subject='Academic CV, updated '+DATA['updated'])
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(TARGET)
