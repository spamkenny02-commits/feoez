"""Native finite style-slot grids and bounded breeding headers.
Grid labels retain their source pixel anchors to within one native space rounding pixel.
No generic numeric/name width is applied to the style-command slots.
"""
import re
from french_font import visible_width,layout_fr
GRIDS={
(29,11):[[],[('Save and Stay','Sauver et dormir'),('Stay','Dormir')],[('Save','Sauver'),('Quit','Quitter')]],
(41,130):[[('Head Kibble','Croquettes Tête'),('Body Kibble','Croquettes Corps')]],
(41,135):[[('Heart Kibble','Croquettes Cœur'),('Fart Kibble','Croquettes Pet')]],
(41,139):[[('Mystery Kibble','Croquettes Mystère'),('Quit','Quitter')]],
(66,35):[[('Shell Manju','Manju Carapace'),('Apricot Doll','Poupée abricotier')],[('Floral Earrings','Boucles fleuries'),('Feather Futon','Futon de plumes')],[('Next Page','Page suivante')]],
(66,36):[[('Floral Purse','Sac fleuri'),('Music Box','Boîte à musique')],[('Choking Scent','Parfum Étouffant'),('Evening Scent','Parfum du Soir')],[('Previous Page','Page précédente'),('Next Page','Page suivante')]],
(66,37):[[('Floral Pan','Poêle fleurie'),('Mechanical Doll','Poupée mécanique')],[('Alluring Scent','Parfum Envoûtant'),('Nothing','Rien')],[('Previous Page','Page précédente')]],
}
def line_grid(source,fields,rom):
 zero={4:0,5:0,6:0,7:0};space=visible_width(' ',rom);cursor=0;output='';report=[]
 if not fields:assert not source.strip();return source,[]
 for english,french in fields:
  at=source.index(english,cursor);inter=source[cursor:at];assert not re.sub(r'<[0-9A-F]{2}>|\s','',inter)
  target=visible_width(source[:at],rom,zero)
  if cursor==0:output=inter
  else:
   controls=''.join(re.findall(r'<[0-9A-F]{2}>',inter));remaining=target-visible_width(output+controls,rom,zero);assert remaining>=0,(source,english,remaining);output+=' '*round(remaining/space)+controls
  actual=visible_width(output,rom,zero);assert abs(actual-target)<=1,(english,actual,target);report.append({'english':english,'french':french,'source_x':target,'french_x':actual});output+=french;cursor=at+len(english)
 output+=source[cursor:];assert visible_width(output,rom,zero)<=216;return output,report
def special_layout(key,english,french,rom,widths):
 if key[0]==43 and 1<=key[1]<=6:
  assert '\n' not in french and visible_width(french,rom,widths)<=216
  return french,{'kind':'single_line_result_ui','native_field_pixels':224,'stops_at_lf':True}
 if key in GRIDS:
  source_lines=english.split('\n');assert len(source_lines)==len(GRIDS[key]);lines=[];report=[]
  for source,fields in zip(source_lines,GRIDS[key]):line,points=line_grid(source,fields,rom);lines.append(line);report+=points
  result='\n'.join(lines);assert re.findall(r'<[0-9A-F]{2}>',result)==re.findall(r'<[0-9A-F]{2}>',french);return result,{'kind':'anchored_grid','anchors':report}
 if key==(41,107):
  prompt,choices=french.rsplit('\n',1);source_choice=english.rsplit('\n',1)[1];line,points=line_grid(source_choice,[('Open it','Ouvrir'),('Quit','Quitter')],rom);return layout_fr(prompt,rom,dynamic_widths=widths)+'\n'+line,{'kind':'prompt_and_anchored_choices','anchors':points}
 if key[0]==41 and key[1] in list(range(36,52))+[78,79,80]:
  parts=french.split('\n',3);assert len(parts)==4;header=parts[:3];assert all(visible_width(l,rom,widths)<=216 for l in header);return '\n'.join(header)+'\n'+layout_fr(parts[3],rom,dynamic_widths=widths),{'kind':'three_header_rows_retained','header_widths':[visible_width(l,rom,widths) for l in header]}
 return layout_fr(french,rom,dynamic_widths=widths),{'kind':'standard_contract_wrap'}
