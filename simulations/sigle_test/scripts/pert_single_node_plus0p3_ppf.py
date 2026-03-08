_s={"init":False,"applied":False}

def pert(t, system):
    if not _s["init"]:
        # enable Ppf/Qpf participation during TDS
        system.PQ.config.p2p = 1
        system.PQ.config.q2q = 1
        p0=list(system.PQ.p0.v)
        i=max(range(len(p0)), key=lambda k: float(p0[k]))
        _s["idx"]=system.PQ.idx.v[i]
        ppf0=system.PQ.get(src='Ppf', attr='v', idx=[_s['idx']])[0]
        qpf0=system.PQ.get(src='Qpf', attr='v', idx=[_s['idx']])[0]
        _s["Ppf0"]=float(ppf0)
        _s["Qpf0"]=float(qpf0)
        ratio=_s["Qpf0"]/_s["Ppf0"] if _s["Ppf0"]!=0 else 0.0
        _s["dP"]=0.3
        _s["dQ"]=0.3*ratio
        print(f"[pert:init] target={_s['idx']} Ppf0={_s['Ppf0']:.5f} Qpf0={_s['Qpf0']:.5f} dP=0.3 dQ={_s['dQ']:.5f}")
        _s["init"]=True

    if (not _s["applied"]) and t>=5.0:
        p_new=_s["Ppf0"]+_s["dP"]
        q_new=_s["Qpf0"]+_s["dQ"]
        system.PQ.alter(src='Ppf', idx=_s['idx'], value=p_new)
        system.PQ.alter(src='Qpf', idx=_s['idx'], value=q_new)
        system.TDS.custom_event=True
        _s["applied"]=True
        print(f"[pert:event] t={t:.4f}s {_s['idx']} Ppf/Qpf step +0.3 => Ppf={p_new:.5f}, Qpf={q_new:.5f}")
