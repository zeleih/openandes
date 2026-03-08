# 11_runbook_repro_commands

更新时间：2026-03-08 01:44 (Asia/Shanghai)

> 目标：给出可直接复制执行的命令链，并区分“已实测通过 / 待执行”。

---

## 命令链 1：建立 ANDES 可运行环境（已实测通过）

```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/andes
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -e .
andes --help
```

**预期输出（关键片段）**
- `Successfully installed ... andes-1.10.0.post12+g1edce20cd`
- `usage: andes [-h] ... {run,plot,doc,misc,prepare,prep,selftest,st,demo} ...`

**常见报错与修复**
1. 报错：`externally-managed-environment`（PEP 668）
   - 原因：在系统 Python 直接 `pip install`。
   - 修复：使用 venv（即本命令链做法）。
2. 报错：`command not found: andes`
   - 原因：未激活 venv。
   - 修复：`source .venv/bin/activate` 后再执行。

---

## 命令链 2：运行潮流基线案例（已实测通过）

```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/andes
source .venv/bin/activate
andes run andes/cases/ieee39/ieee39.xlsx -r pflow --no-preamble
```

**预期输出（关键片段）**
- `Parsing input file "andes/cases/ieee39/ieee39.xlsx"...`
- `-> Power flow calculation`
- `Converged in 5 iterations`
- `Report saved to "ieee39_out.txt"`

**常见报错与修复**
1. 报错：`error: file "..." does not exist.`
   - 示例：`andes/cases/ieee14/ieee14.xlsx`（当前仓库不存在该文件名）。
   - 修复：先 `find andes/cases -name '*.xlsx'` 确认真实路径。
2. 报错：`No module named andes`
   - 修复：确认使用的是 `.venv/bin/python` 与 `.venv/bin/andes`。

---

## 命令链 3：运行短时动态仿真（已实测通过）

```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/andes
source .venv/bin/activate
andes run andes/cases/kundur/kundur_full.xlsx -r pflow tds --tf 0.2 --no-preamble
```

**预期输出（关键片段）**
- `Converged in 5 iterations`
- `Initialization for dynamics completed`
- `Simulation to t=0.20 sec completed`
- `Outputs to "kundur_full_out.lst" and "kundur_full_out.npz"`

**常见报错与修复**
1. 报错：初始化失败（不同案例可能出现）
   - 修复：先单独跑 `-r pflow`；确认工况可收敛，再加 `tds`。
2. 报错：仿真时间过长
   - 修复：先缩短 `--tf`（如 0.1~0.5s）进行烟测。

---

## 命令链 4：demo notebook 预检（已实测通过）

```bash
python3 - <<'PY'
import json,glob,os,re
root='/Users/hhuhzl/.openclaw/workspace/andesnotes/repos/demo/demo'
paths=sorted(glob.glob(root+'/**/*.ipynb',recursive=True))
print('count', len(paths))
for p in paths[:12]:
    nb=json.load(open(p))
    ks=nb.get('metadata',{}).get('kernelspec',{}).get('name')
    imports=[]
    for c in nb.get('cells',[])[:8]:
        if c.get('cell_type')=='code':
            src=''.join(c.get('source',[]))
            for m in re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)',src,flags=re.M):
                imports.append(m.split('.')[0])
    print(os.path.relpath(p,os.path.dirname(root)), 'kernel=',ks,'imports=',sorted(set(imports))[:8])
PY
```

**预期输出（关键片段）**
- `count 55`
- 若干行 `... kernel= python3 imports= [...]`

**常见报错与修复**
1. 报错：`JSONDecodeError`
   - 修复：该 notebook 可能损坏；换下一个文件验证并单独定位损坏文件。
2. 报错：路径为空
   - 修复：确认仓库已克隆到 `andesnotes/repos/demo`。

---

## 待执行命令链（未实测）

### A) 执行单个 ANDES-only notebook
```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/demo/demo/forced_oscillation
# 任选其一：jupyter lab / jupyter notebook
jupyter lab
```
- 说明：本轮未实测 notebook UI 执行；仅完成结构与代码检查。

### B) AMS 依赖检查后执行 benchmark notebook
```bash
# 在目标环境中
python -c "import ams; print(ams.__version__)"
```
- 说明：当前 andes venv 下 `ams` 不可导入；需先补齐依赖（参考 demo/environment.yml 与 ams_benchmark/README.md）。

---

## 额外验证记录（已实测）

```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/andes
source .venv/bin/activate
andes demo
```

- 实际结果：`NotImplementedError: Demos have not been implemented`
- 结论：`andes demo` 不是当前版本的可用演示入口，应改走 `andes run` 或 demo 仓库 notebook。
