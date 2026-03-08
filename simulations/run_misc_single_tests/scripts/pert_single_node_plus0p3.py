_s={"init":False,"applied":False}

def pert(t, system):
    if not _s["init"]:
        p0=list(system.PQ.p0.v)
        q0=list(system.PQ.q0.v)
        i=max(range(len(p0)), key=lambda k: float(p0[k]))
        _s["idx"]=system.PQ.idx.v[i]
        _s["p0"]=float(p0[i])
        _s["q0"]=float(q0[i])
        ratio=_s["q0"]/_s["p0"] if _s["p0"]!=0 else 0.0
        _s["dP"]=0.3
        _s["dQ"]=0.3*ratio
        print(f"[pert:init] target={_s['idx']} p0={_s['p0']:.5f} q0={_s['q0']:.5f} dP=0.3 dQ={_s['dQ']:.5f}")
        _s["init"]=True

    if (not _s["applied"]) and t>=5.0:
        p_new=_s["p0"]+_s["dP"]
        q_new=_s["q0"]+_s["dQ"]
        system.PQ.set(src='p0', attr='v', idx=_s['idx'], value=p_new)
        system.PQ.set(src='q0', attr='v', idx=_s['idx'], value=q_new)
        try:
            system.PQ.set(src='Ppf', attr='v', idx=_s['idx'], value=p_new)
            system.PQ.set(src='Qpf', attr='v', idx=_s['idx'], value=q_new)
        except Exception:
            pass
        system.TDS.custom_event=True
        _s["applied"]=True
        print(f"[pert:event] t={t:.4f}s {_s['idx']} load +0.3 => p={p_new:.5f}, q={q_new:.5f}")
