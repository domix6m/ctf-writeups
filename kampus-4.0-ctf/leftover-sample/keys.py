import sys; sys.path.insert(0,'.')
import emu, struct
from unicorn import *
from unicorn.x86_const import *
def get(inp):
    keys=[]
    def h(mu):
        def c(mu,addr,size,u):
            keys.append(mu.mem_read(0x8222194,1)[0])
        mu.hook_add(UC_HOOK_CODE,c,begin=0x806d096,end=0x806d096)
    o,st=emu.run(inp,hooks=h)
    return keys,o
if __name__=='__main__':
    for s in sys.argv[1:]:
        k,o=get(s.encode()+b'\n'); print(s, bytes(k).hex(), o[-20:])
