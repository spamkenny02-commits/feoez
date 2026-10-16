"""Fixed-span text edits for the pinned English ROM's startup screens.
No executable instructions or date/time fields are changed.
"""
from french_font import encode_fr
ASCII={
0xF140:("THE BACKUP DATA ISN'T WORKING.","SAUVEGARDE INUTILISABLE."),
0xF160:('PRESS THE A BUTTON.','APPUYEZ SUR A.'),
0xF175:('PRESS THE B BUTTON.','APPUYEZ SUR B.'),
0xF18A:('RESET THE SYSTEM.','REINITIALISEZ.'),
0xFF022:('SPC7110 CHECK PROGRAM V2.2','SPC7110 CONTROLE MEM. V2.2'),
0xFF044:('REG INIT','INIT REG'),
0xFF04D:('S-RAM DATA BUS','SRAM BUS DONN.'),
0xFF05C:('S-RAM ADDR BUS','SRAM BUS ADR.'),
0xFF06B:('S-RAM R/W','SRAM L/E'),
0xFF075:('D-PORT ACC','ACC.PORT D'),
0xFF088:('C-LENGTH','LONGUEUR'),
0xFF091:('D-PORT B+O+S','PORT D B+O+S'),
0xFF09E:('RTC TIME','H. RTC'),
0xFF0AE:('RTC BACKUP','SAUV. RTC'),
0xFF0B9:('S-RAM BACKUP','SAUV. SRAM'),
0xFF0C6:('ON TEST','EN TEST'),
0xFF0CE:('COMPLETE','TERMINE'),
0xFF0D7:('ID DETECT','DETECT ID'),
0xFF0E4:('NG','KO'),
}
NATIVE={
0xEB25:('Is this okay?',"C'est bon ?"),
0xEB37:('Yes','Oui'),
0xF1D4:('Enter your birthday and the year.','Date de naissance (mois-jour-an)'),
0xF1FD:('Press up and down on the direction pad','Utilise les directions Haut et Bas'),
0xF228:('to change the number.','pour le modifier.'),
0xF242:('Press the A Button to confirm.','Appuie sur A pour valider.'),
0x6D2511:('Enter the current date and time.',"Règle la date et l'heure."),
0x6D2536:('(Month, day, year, and A.M./P.M. time)','(Mois, jour, année ; heure AM/PM)'),
0x6D2561:('Press up and down on the direction pad','Utilise les directions Haut et Bas'),
0x6D258C:('to change the number.','pour le modifier.'),
0x6D25A6:('Press the A Button to confirm.','Appuie sur A pour valider.'),
}
def encode_menu(text):
    return encode_fr(text.replace('(', '<17>').replace(')', '<18>').replace('/', '<1E>'))

def patch_startup(source):
    out=bytearray(source);edits=[]
    for encoding,table in [('ascii',ASCII),('native',NATIVE)]:
        for offset,(english,french) in table.items():
            enc=(lambda s:s.encode('ascii')) if encoding=='ascii' else encode_menu
            old=enc(english);new=enc(french)
            assert source[offset:offset+len(old)]==old,(hex(offset),english)
            assert len(new)<=len(old),(hex(offset),len(new),len(old))
            new=new.ljust(len(old),b' ');out[offset:offset+len(old)]=new
            edits.append({'offset':hex(offset),'length':len(old),'encoding':encoding,'english':english,'french':french,'source_hex':old.hex(),'modified_hex':new.hex()})
    offset=0xEB3F;old=encode_fr('No')+b'\x00\xff';new=encode_fr('Non')+b'\x00'
    assert source[offset:offset+4]==old and source[offset+4]==0xff
    out[offset:offset+4]=new
    edits.append({'offset':hex(offset),'length':4,'encoding':'native','english':'No','french':'Non','source_hex':old.hex(),'modified_hex':new.hex(),'note':'Consumes one verified FF padding byte; following list terminator stays FF.'})
    # The success banner is a tile stream, not an ASCII string. FF ends the
    # native draw routine before its second-row pass; all instructions stay intact.
    offset=0xFE286;old=bytes.fromhex('a6 a7 c2 c3 c2 c3 10 10 c4 00 c7 0d');new=b'    TOUT OK\xff'
    assert source[offset:offset+len(old)]==old and len(new)==len(old)
    out[offset:offset+len(old)]=new
    edits.append({'offset':hex(offset),'length':len(old),'encoding':'diagnostic_tile_stream','english':'ALL OK','french':'TOUT OK','source_hex':old.hex(),'modified_hex':new.hex(),'note':'Existing ASCII tiles; four leading spaces center the single-row result. No font or executable change.'})
    for marker_offset in (0x2F25,0xFF0E7):
        marker=b'SPC7110 CHECK OK'
        assert source[marker_offset:marker_offset+len(marker)]==marker,'Unsupported backup signature'
        assert out[marker_offset:marker_offset+len(marker)]==marker,'Never translate an internal backup signature'
    return bytes(out),edits
