#!/usr/bin/env python3
"""Recolour devast.io team/clan sprites. Usage: python3 clan_color.py <hex> [name]
Outputs clan_color/<name>/*.png from clan_color/orig/ (originals from devast.io/img/)."""
import sys, os, colorsys
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); O=os.path.join(D,'clan_color','orig')
def hexrgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def lum(r,g,b): return .299*r+.587*g+.114*b
def recolor(src,dst,col,mode):
    im=Image.open(src).convert('RGBA'); px=im.load(); w,h=im.size
    ch,cl,cs=colorsys.rgb_to_hls(*col)
    for y in range(h):
        for x in range(w):
            r,g,b,a=px[x,y]
            if a==0: continue
            R,G,B=r/255,g/255,b/255; hh,ll,ss=colorsys.rgb_to_hls(R,G,B)
            if mode=='ring':      # green ally ring -> colour
                if not (G>R+.15 and G>B): continue
                nr,ng,nb=colorsys.hls_to_rgb(ch,ll,max(cs,ss))
            elif mode=='button':  # grey/coloured fill -> colour, keep white icons & black outline
                if ll<.12 or ll>.85: continue
                nr,ng,nb=colorsys.hls_to_rgb(ch,ll*.9,min(1,cs*.75))
            else:                 # 'panel': dark panel, tint outline/frame + light wash
                t=.55 if ll<.06 else .18
                nr,ng,nb=[c*(1-t)+cc*t*max(.25,ll*3) for c,cc in zip((R,G,B),col)]
            px[x,y]=(int(nr*255),int(ng*255),int(nb*255),a)
    im.save(dst)
SPR={'arrow-minimap2':'ring','team-button-out':'button','team-button-in':'button',
     'team-button-click':'button','memberteam-box':'panel','jointeam-box':'panel','clan-icon':'button'}
def build(hexc,name=None):
    name=name or hexc.lstrip('#'); out=os.path.join(D,'clan_color',name); os.makedirs(out,exist_ok=True)
    for f,m in SPR.items(): recolor(os.path.join(O,f+'.png'),os.path.join(out,f+'.png'),hexrgb(hexc),m)
    return out
if __name__=='__main__':
    print(build(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else None))
