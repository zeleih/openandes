_s={"init":False,"applied":False}

def pert(t, system):
    if not _s["init"]:
        p0=list(system.PQ.p0.v)
        i=max(range(len(p0)), key=lambda k: float(p0[k]))
        _s["idx"]=system.PQ.idx.v[i]
        req0=system.PQ.get(src='Req', attr='v', idx=[_s['idx']])[0]
        xeq0=system.PQ.get(src='Xeq', attr='v', idx=[_s['idx']])[0]
        _s['Req0']=float(req0); _s['Xeq0']=float(xeq0)
        ppf0=system.PQ.get(src='Ppf', attr='v', idx=[_s['idx']])[0]
        qpf0=system.PQ.get(src='Qpf', attr='v', idx=[_s['idx']])[0]
        ratio=(qpf0/ppf0) if ppf0!=0 else 0.0
        _s['dP']=0.5
        _s['dQ']=0.5*ratio
        _s['dReq']=_s['dP']
        _s['dXeq']=_s['dQ']
        print(f"[pert:init] idx={_s['idx']} Req0={_s['Req0']:.5f} Xeq0={_s['Xeq0']:.5f} dReq={_s['dReq']:.5f} dXeq={_s['dXeq']:.5f}")
        _s['init']=True
    if (not _s['applied']) and t>=5.0:
        system.PQ.alter(src='Req', idx=_s['idx'], value=_s['Req0']+_s['dReq'])
        system.PQ.alter(src='Xeq', idx=_s['idx'], value=_s['Xeq0']+_s['dXeq'])
        system.TDS.custom_event=True
        _s['applied']=True
        print(f"[pert:event] t={t:.4f}s { _s['idx']} Req/Xeq step applied")
