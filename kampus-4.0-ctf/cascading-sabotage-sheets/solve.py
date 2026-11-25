import struct
m=bytearray(open('mem.bin','rb').read())
w=lambda a: struct.unpack('<H',m[a:a+2])[0]
M=0xffff
rol=lambda x,c:((x<<c)|(x>>(16-c)))&M
ror=lambda x,c:((x>>c)|(x<<(16-c)))&M
def fwd(st,bp):
    out=[0]*8; dx=w(bp+0x30)^0xd3d3
    for i in range(8):
        ax=st[i]^dx^(w(bp+2*i+0x10)^0x6d6d)
        ax=rol(ax,3); ax=(ax+w(bp+2*i+0x20)-0x3737)&M
        out[(w(bp+2*i)^0xa7a7)//2]=ax; dx=ax
    return out
def inv(out,bp):
    st=[0]*8; dx=w(bp+0x30)^0xd3d3
    for i in range(8):
        ax=out[(w(bp+2*i)^0xa7a7)//2]
        st[i]=ror((ax-w(bp+2*i+0x20)+0x3737)&M,3)^dx^(w(bp+2*i+0x10)^0x6d6d); dx=ax
    return st
print([hex(w(0x23b+2*i)^0xa7a7) for i in range(8)],[hex(w(0x26d+2*i)^0xa7a7) for i in range(8)])
target=[w(0x29f+2*i)^0x5151 for i in range(8)]
st=inv(inv(target,0x26d),0x23b)
code=b''.join(struct.pack('<H',x) for x in st); print(code)
assert fwd(fwd(st,0x23b),0x26d)==target
# flag
bp=0x29f; cx=w(bp+0x12); dx=w(bp+0x14); di=0x126b; flag=b''
inp=st
for k in range(cx):
    si=2*k; ax=rol(inp[(si&0xf)//2],3)^w(bp+si+0x16)^dx; ax=(ax-di)&M
    flag+=struct.pack('<H',ax); dx=w(bp+si+0x16); di+=0x27
print(cx, flag)
