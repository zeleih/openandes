# 09_cases_learning_path

更新时间：2026-03-08 01:44 (Asia/Shanghai)

## 0) 本轮验证边界
- 代码仓库（本地）：
  - `andesnotes/repos/andes`（HEAD: `1edce20c`, branch: `master`）
  - `andesnotes/repos/demo`（HEAD: `1a17426`, branch: `master`）
- 仅记录已在本机可验证的信息；不记录任何臆测结果。

## 1) 路径总览（优先顺序）

### 路径A：ANDES内置案例（先跑通引擎）
目标：确认 `andes run` 工作正常，再进入 notebook。

1. 环境准备（venv + editable install）
2. CLI自检（`andes --help`）
3. 跑 `pflow` 基线案例（推荐 `ieee39.xlsx`）
4. 跑 `pflow + tds` 短时动态（推荐 `kundur_full.xlsx`）

**价值**：最快验证“求解器 + 数据解析 + 输出文件”。

### 路径B：demo仓库中仅依赖 ANDES 的 notebook
目标：优先执行不依赖 `ams` 的 notebook（成功率高）。

优先建议（从低门槛到高门槛）：
1. `demo/forced_oscillation/forced_oscillation.ipynb`
2. `demo/oscillation/oscillation.ipynb`
3. `demo/interface_andes/interface_andes.ipynb`
4. `demo/misc/*.ipynb`（如 `voltage_sag.ipynb`, `alter_load.ipynb`）

### 路径C：AMS基准类 notebook（后置）
目标：再扩展到 `ams_benchmark/*`。

- 这类 notebook 明确 `import ams`，当前 venv 中未检测到 `ams`。
- 需补齐 `ltbams/ams` 依赖后再执行。

## 2) 目录映射（examples/cases/demo）

### andes 仓库
- 未发现本地 `examples/` 目录（`find -name examples` 无输出）。
- 可复现样例主要位于：`andes/cases/*`
  - 关键子目录：`ieee14`, `ieee39`, `kundur`, `npcc`, `wecc`, `wscc9` 等。

### demo 仓库
- 主内容位于：`demo/demo/*`
- 检出 `.ipynb` 共 **55** 个。
- `README.md` 给出高级用法、仿真、benchmark、debug 的导航入口。

## 3) 已实测通过 vs 待执行

### 已实测通过
1. `andes` 在本地 venv 可安装并可调用 CLI。
2. `andes run andes/cases/ieee39/ieee39.xlsx -r pflow` 收敛成功并生成报告。
3. `andes run andes/cases/kundur/kundur_full.xlsx -r pflow tds --tf 0.2` 成功完成短时动态仿真并输出 `.lst/.npz`。

### 待执行
1. demo 仓库 notebook 批量自动执行（建议 `nbconvert --execute` 或逐个跑）。
2. `ams_benchmark` 相关 notebook（需先安装并验证 `ams` 依赖）。
3. 对 `ieee14` 的更完整链路（raw+dyr 输入、扰动文件等）做专项复现。

## 4) 学习推进建议（下一轮直接执行）
1. 先在 demo 中挑 3 个 ANDES-only notebook 做“可执行最小闭环”（单次运行+关键图/输出文件确认）。
2. 建立 notebook 运行矩阵（成功/失败/缺依赖/耗时）。
3. 再进入 AMS benchmark，单独创建环境并记录 solver 可用性（GUROBI/MOSEK/PIQP/pandapower）。
