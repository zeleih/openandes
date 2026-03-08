# 10_demo_notebooks_deepdive

更新时间：2026-03-08 01:44 (Asia/Shanghai)

## 1) 盘点结果（可验证）
- 扫描路径：`andesnotes/repos/demo/demo/**/*.ipynb`
- notebook 数量：**55**
- kernelspec：抽样均为 `python3`

## 2) 依赖分层（按 import）

### A. ANDES主线（优先执行）
典型特征：`import andes`（常伴随 `matplotlib`）

代表文件：
- `demo/forced_oscillation/forced_oscillation.ipynb`
- `demo/oscillation/oscillation.ipynb`
- `demo/interface_andes/interface_andes.ipynb`
- `demo/TGOV1/TGOV1_variants.ipynb`
- `demo/misc/alter_load.ipynb`
- `demo/misc/voltage_sag.ipynb`

观察到的代码模式（来自 notebook 代码单元）：
- `case = andes.get_case('kundur/kundur_full.xlsx')`
- `andes.load(..., pert='./pert.py')`
- `!andes misc --version`

### B. AMS扩展线（后置）
典型特征：`import ams`

代表文件：
- `demo/ams_benchmark/opf/bench_opf.ipynb`
- `demo/ams_benchmark/opf/bench_opf_repeat.ipynb`
- `demo/ams_benchmark/opf/bench_educ.ipynb`
- `demo/ams_benchmark/UCCase/*.ipynb`

观察到的代码模式：
- `import ams`
- `%run ../benchmarks.py`
- 多求解器对比（GUROBI/MOSEK/PIQP/pandapower）

## 3) 与README对齐情况
- `demo/README.md` 的导航与目录结构一致（Advanced Usage / Simulations / Benchmark / Debug）。
- `demo/ams_benchmark/README.md` 明确 benchmark 环境与工具版本说明。

## 4) 当前可复现性判断

### 已实测通过（环境侧）
- 已在 `andes` 仓库创建 venv 并完成 `andes` editable 安装。
- 在该 venv 中检测：`andes` 可导入，`ams` 不可导入（`find_spec('ams') == False`）。

### 待执行（notebook侧）
- 尚未逐个执行 demo notebooks（本轮仅完成结构与代码单元验证）。
- AMS线 notebooks 待依赖补齐后执行。

## 5) 推荐执行顺序（最小风险）
1. `forced_oscillation` → 2) `oscillation` → 3) `interface_andes`
2. 再跑 `misc/*` 中单案例 notebook
3. 最后进入 `ams_benchmark/*`

## 6) 已识别风险点
- `andes demo` 子命令当前会抛出 `NotImplementedError: Demos have not been implemented`，不作为 notebook 入口。
- 部分案例路径名容易误写（如 `ieee14.xlsx` 在当前仓库并不存在）。
