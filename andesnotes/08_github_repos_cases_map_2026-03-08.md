# ANDES GitHub + Demo 仓库学习记录（2026-03-08）

## 1) 仓库同步
- ANDES 源码仓库：`andesnotes/repos/andes`
- Demo 仓库：`andesnotes/repos/demo`

## 2) Case / Demo 资源盘点（重点）

### ANDES 内置 case（`andes/andes/cases`）
- 典型系统：`ieee14`, `ieee39`, `kundur`, `wecc`, `npcc`, `wscc9`, `nordic44`, `GBnetwork`, `matpower`, `5bus`, `smib` 等。
- 文件形态：`.xlsx`, `.json`, `.raw`, `.dyr`, `.m` 等混合。
- `ieee14` 子目录含大量控制器/扰动/故障示例（如 `fault`, `linetrip`, `gentrip`, `pllvfu1`, `esst*`, `hygov*`）。

### demo 仓库（`demo/demo/*`）
- 仿真类：`forced_oscillation`, `oscillation`, `freq_response`, `TGOV1`, `TurbineGov_response`, `bus_current_injection`, `andes_stochastic`
- 系统级：`texas7k`, `hawaii`, `rolling_horizon`
- 调试与技巧：`misc`（含 `output_select`, `alter_load`, `voltage_sag`, `andes_tds_init`, `busfreq` 等）
- benchmark：`pflow_benchmark`

## 3) 运行环境安装与实测

### 环境
- `/.venv-andes`（Python 3.14）已装 ANDES，但运行 case 出现兼容性问题。
- 新建 `/.venv-andes312`（Python 3.12.13）并安装 ANDES 1.10.0。

### 关键命令与结果
1. 版本检查
- `andes misc --version` ✅
- 说明：`andes --version` 不是有效参数。

2. 数值代码生成
- `andes prepare -q` ✅
- 生成路径：`~/.andes/pycode`

3. 基础 case 验证
- Python API：`andes.load(andes.get_case('ieee14/ieee14.json')); ss.PFlow.run()` ✅ `PFlow converged True`

4. demo case 验证
- 命令：
  `andes run .../demo/TGOV1/ieee39_TGOV1.xlsx -r pflow`
- 结果：NR 5 次迭代收敛，输出 `ieee39_TGOV1_out.txt` ✅

## 4) 当前学习结论
- GitHub 仓库中的“案例学习路径”已可落地执行（可跑通内置 case 与 demo case 的 PFlow）。
- 后续重点：
  1) 逐个学习 demo 的 notebook 结构（输入、扰动脚本、输出分析）；
  2) 把 `TGOV1 / forced_oscillation / freq_response` 做成可复现实操笔记；
  3) 在 ANDES 主仓库中对照 `cases` 与文档章节建立“章节-样例映射表”。
