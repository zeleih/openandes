import numpy as np
_s={"init":False,"applied":False}

def pert(t, system):
    if not _s["init"]:
        p0=np.array(system.PQ.p0.v,dtype=float)
        q0=np.array(system.PQ.q0.v,dtype=float)
        idx=list(system.PQ.idx.v)
        i=int(np.argmax(p0))
        _s["pq_idx"]=idx[i]
        _s["p0"]=float(p0[i])
        _s["q0"]=float(q0[i])
        _s["gen_cap_sum"]=float(np.sum(system.GENROU.Sn.v))
        _s["dP"]=0.05*_s["gen_cap_sum"]/100.0
        ratio=(_s["q0"]/_s["p0"]) if _s["p0"]!=0 else 0.0
        _s["dQ"]=ratio*_s["dP"]
        print(f"[pert:init] target={_s['pq_idx']} p0={_s['p0']:.5f} q0={_s['q0']:.5f}, sumGenCap={_s['gen_cap_sum']:.3f}, dP={_s['dP']:.5f}")
        _s["init"]=True
    if (not _s["applied"]) and t>=5.0:
        p_new=_s["p0"]+_s["dP"]
        q_new=_s["q0"]+_s["dQ"]
        system.PQ.set(src='p0', attr='v', idx=_s['pq_idx'], value=p_new)
        system.PQ.set(src='q0', attr='v', idx=_s['pq_idx'], value=q_new)
        try:
            system.PQ.set(src='Ppf', attr='v', idx=_s['pq_idx'], value=p_new)
            system.PQ.set(src='Qpf', attr='v', idx=_s['pq_idx'], value=q_new)
        except Exception:
            pass
        system.TDS.custom_event=True
        _s["applied"]=True
        print(f"[pert:event] t={t:.4f}s single-node load step on {_s['pq_idx']}: +dP={_s['dP']:.5f}, +dQ={_s['dQ']:.5f}")
