_s={"init":False,"applied":False}

def pert(t, system):
    if not _s["init"]:
        # pick largest PQ by p0
        p0=list(system.PQ.p0.v)
        q0=list(system.PQ.q0.v)
        i=max(range(len(p0)), key=lambda k: float(p0[k]))
        _s["pq_idx"]=system.PQ.idx.v[i]
        _s["p0"]=float(p0[i])
        _s["q0"]=float(q0[i])
        print(f"[pert:init] target_load={_s['pq_idx']} p0={_s['p0']:.5f} q0={_s['q0']:.5f}")
        _s["init"]=True

    if (not _s["applied"]) and t>=5.0:
        k=1.15  # +15% load step
        p_new=_s["p0"]*k
        q_new=_s["q0"]*k
        # update both base and pf setpoint fields for robustness
        system.PQ.set(src='p0', attr='v', idx=_s['pq_idx'], value=p_new)
        system.PQ.set(src='q0', attr='v', idx=_s['pq_idx'], value=q_new)
        try:
            system.PQ.set(src='Ppf', attr='v', idx=_s['pq_idx'], value=p_new)
            system.PQ.set(src='Qpf', attr='v', idx=_s['pq_idx'], value=q_new)
        except Exception:
            pass
        system.TDS.custom_event=True
        _s["applied"]=True
        print(f"[pert:event] t={t:.4f}s +15% load on {_s['pq_idx']}: p={p_new:.5f}, q={q_new:.5f}")
