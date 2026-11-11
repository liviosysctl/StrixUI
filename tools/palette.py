def lin(c):
    c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def L(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16) for i in (0,2,4)]
    return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def cr(a,b):
    la,lb=L(a),L(b); 
    if la<lb: la,lb=lb,la
    return (la+0.05)/(lb+0.05)
C = {
 # required ten
 'background':'#0b0a09','surface':'#131211','border':'#2f2c28','text':'#ece6da','text-muted':'#a09a8f',
 'accent':'#c8102e','on-accent':'#ffffff','focus':'#e8324a','error':'#ff6b78','warning':'#d9a441',
 # extras
 'surface-raised':'#1b1917','surface-sunken':'#070606','border-strong':'#6e6a63','text-faint':'#77726a',
 'accent-hover':'#dc1f3d','accent-pressed':'#a50d26','accent-text':'#f2556a','accent-soft':'#2a0c12',
 'line':'#d8d0c0','success':'#8fb894','info':'#8ea8c8',
 'syntax-keyword':'#f2556a','syntax-string':'#cdb98a','syntax-number':'#d99a6c','syntax-function':'#f4efe6',
 'syntax-type':'#9db4cf','syntax-constant':'#c3a6c9','syntax-comment':'#8a847a','syntax-operator':'#a09a8f',
 'chart-1':'#c8102e','chart-2':'#ece6da','chart-3':'#8c877f','chart-4':'#cdb98a','chart-5':'#8ea8c8',
}
T = {'background':'#0b0a09','foreground':'#e6e0d4','cursor':'#c8102e','selection':'#3a1219',
 'black':'#1b1917','red':'#e5475b','green':'#8fb894','yellow':'#d9b36a','blue':'#8ea8c8','magenta':'#c3a6c9','cyan':'#8fbcb8','white':'#c9c3b8',
 'bright-black':'#857f76','bright-red':'#ff7885','bright-green':'#aed3b2','bright-yellow':'#edcd8c','bright-blue':'#b0c6e2','bright-magenta':'#dcc3e1','bright-cyan':'#b0d8d4','bright-white':'#f7f3ea'}
if __name__=='__main__':
    S=['background','surface','surface-raised']
    rows=[]
    def chk(fg,bgs,minr,src=C,bsrc=C):
        for b in bgs:
            r=cr(src[fg],bsrc[b]); rows.append((fg,b,r,minr,'ok' if r>=minr else 'FAIL'))
    chk('text',S,4.5); chk('text-muted',S,4.5); chk('on-accent',['accent','accent-hover','accent-pressed'],4.5)
    chk('error',S,4.5); chk('focus',S,3); chk('accent-text',S,4.5); chk('warning',S,4.5); chk('success',S,4.5); chk('info',S,4.5)
    chk('border-strong',S,3); chk('text-faint',S,3); chk('accent',['background','surface'],3)
    for k in C:
        if k.startswith('syntax-'): chk(k,['background','surface'],4.5)
    for k in ('chart-1','chart-2','chart-3','chart-4','chart-5'): chk(k,['surface'],3)
    chk('accent-text',['accent-soft'],4.5)
    for k in T:
        if k not in('background','cursor','selection','black'):
            r=cr(T[k],T['background']); rows.append(('term '+k,'term bg',r,4.5,'ok' if r>=4.5 else 'FAIL'))
    r=cr(T['foreground'],T['selection']); rows.append(('term fg','selection',r,4.5,'ok' if r>=4.5 else 'FAIL'))
    r=cr(T['cursor'],T['background']); rows.append(('term cursor','term bg',r,3,'ok' if r>=3 else 'FAIL'))
    for x in rows: print(f"{x[0]:22s} on {x[1]:16s} {x[2]:5.2f} (min {x[3]}) {x[4]}")
    print('FAILS', sum(1 for x in rows if x[4]=='FAIL'))
