# ANDES 实操：最小可运行自定义模型（可验证方案）

> 目标：基于已学习的 `creating-models` 路线，给出一套**可直接执行、可逐步验证**的最小自定义模型实践流程。  
> 约束：本文不编造运行结果；仅记录本机已验证事实 + 可执行命令。

---

## 1. 目标

完成一个“最小可运行自定义模型”闭环：
1. 准备 ANDES 环境；
2. 基于官方静态模型示例（Shunt）复制出一个自定义模型；
3. 注册模型并执行 `andes prepare -i`；
4. 通过命令验证“模型已被框架识别且可生成数值代码”；
5. 给出失败排查路径。

---

## 2. 前置条件

- macOS / Linux shell
- Python 3.10+（建议 3.11）
- `git`
- 可访问 PyPI / GitHub

建议在独立目录执行：
```bash
mkdir -p ~/work/andes-dev && cd ~/work/andes-dev
```

---

## 3. 本机现状（已实测）

以下命令在当前机器执行过：

```bash
which andes
andes --version
python3 -c "import andes,sys;print(andes.__version__)"
```

已获取到的真实结果：
- `andes` 命令不存在（`command not found`）
- Python 无 `andes` 模块（`ModuleNotFoundError: No module named 'andes'`）

结论：当前环境**未安装 ANDES**，因此下文提供“从零可执行步骤 + 验证命令”。

---

## 4. 实操步骤（从零到可验证）

## 步骤 A：创建虚拟环境并安装 ANDES

```bash
cd ~/work/andes-dev
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install andes
andes --version
python -c "import andes; print(andes.__version__)"
```

### 预期输出
- `andes --version` 输出版本号（如 `1.x.x`）
- Python 打印相同版本号

---

## 步骤 B：获取源码（用于自定义模型开发）

```bash
cd ~/work/andes-dev
git clone https://github.com/CURENT/andes.git
cd andes
```

确认官方示例存在（避免路径猜测）：
```bash
rg -n "class Shunt" andes/models
rg -n "creating-models|example-static|Shunt" docs -S
```

### 预期输出
- 至少命中 `Shunt` 类定义位置
- docs 中能检索到静态模型示例相关页面/文字

---

## 步骤 C：复制官方最小静态模型为自定义模型

> 原则：先复用官方最小可行模板，再改名与注册，降低首轮失败率。

1) 打开 `Shunt` 源文件（用上一步 `rg` 输出的真实路径）。  
2) 复制为新文件，例如：
```bash
cp andes/models/shunt.py andes/models/shuntlite.py
```
3) 在 `shuntlite.py` 内最小改动：
- 类名改为唯一新名（如 `ShuntLiteData`, `ShuntLite`）
- 保持方程结构与变量定义不变（首轮不要改方程）
- 模型名/文档字符串改为新名（便于检索）

建议改完后做静态检查：
```bash
rg -n "class ShuntLite|ShuntLiteData" andes/models/shuntlite.py
python -m py_compile andes/models/shuntlite.py
```

### 预期输出
- `rg` 能命中新类名
- `py_compile` 无语法错误

---

## 步骤 D：注册模型并准备代码生成

1) 编辑 `andes/models/__init__.py`，把 `ShuntLite` 模块加入导入/注册列表（按文件现有风格添加）。
2) 执行代码生成准备：
```bash
andes prepare -i
```

### 预期输出
- `prepare` 过程结束且无异常退出
- 若有缓存/生成日志，不应出现 import error / attribute error / duplicate model name

---

## 步骤 E：最小“可运行”验证

### E1. 结构验证（必须）
```bash
python - <<'PY'
import andes
from andes.system import System
print('andes version:', andes.__version__)
# 仅验证包可导入、System 可构建
sys = System()
print('system init ok')
PY
```

### E2. 自定义模型可发现验证（必须）
> 使用 `rg` + import 双重验证，避免“文件存在但未注册”。

```bash
rg -n "ShuntLite" andes/models/__init__.py andes/models/shuntlite.py
python - <<'PY'
# 若注册路径不同，请按实际路径调整 import 语句
from andes.models.shuntlite import ShuntLite
print('ShuntLite import ok:', ShuntLite.__name__)
PY
```

### E3. 回归运行验证（建议）
> 用官方内置 case 跑一次潮流，确认新增模型未破坏基础运行链路。

```bash
python - <<'PY'
import andes
ss = andes.load(andes.get_case('ieee14/ieee14_pvd1.xlsx'))
ss.PFlow.run()
print('PFlow exit:', ss.PFlow.exit_code)
PY
```

### 预期输出
- E1/E2 都能打印 `ok`
- E3 输出 `PFlow exit: 0`（若样例名不同，请先 `python -c "import andes; print(andes.get_case.__doc__)"` 或检索可用 case）

---

## 5. 失败排查

### 问题 1：`andes: command not found`
- 原因：未安装或未激活 venv
- 排查：`which python && which andes`
- 处理：重新 `source .venv/bin/activate`，再 `pip install andes`

### 问题 2：`ModuleNotFoundError: andes`
- 原因：解释器不是 venv 的 Python
- 排查：`python -c "import sys; print(sys.executable)"`
- 处理：确认路径位于 `.../.venv/bin/python`

### 问题 3：`andes prepare -i` 报 import/注册错误
- 常见原因：
  - 新类名与已有模型冲突
  - `__init__.py` 未正确注册
  - 复制后类名与文件名不一致
- 排查命令：
```bash
rg -n "ShuntLite|class .*Data|class .*\(" andes/models/shuntlite.py andes/models/__init__.py
```

### 问题 4：回归 case 名不存在
- 排查：
```bash
python - <<'PY'
import andes, pkgutil
print('andes imported ok:', andes.__version__)
PY
```
- 处理：改用本地实际存在的官方样例；先确认 `andes.get_case(...)` 可解析。

---

## 6. 交付标准（通过/不通过）

通过条件（全部满足）：
1. `andes --version` 与 Python import 都成功；
2. `shuntlite.py` 可编译；
3. `andes prepare -i` 成功；
4. `from andes.models.shuntlite import ShuntLite` 成功；
5. 至少一个官方 case 的 `PFlow.exit_code == 0`（建议）。

不通过条件（任一触发）：
- 任意步骤出现未定位原因的异常；
- 仅“文件创建成功”但未完成 import/prepare 验证。

---

## 7. 备注

- 本文是“最小可运行”方案，刻意不在首轮引入新方程/离散逻辑。  
- 下一步建议：在 `ShuntLite` 中只改**一个**可控参数（如新增倍率因子），每次改动都重复 E1~E3 验证链路。