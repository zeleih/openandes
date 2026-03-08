# ANDES 建模速查表（面向最小自定义模型）

> 用途：执行/复盘“最小可运行自定义模型”时快速查命令与检查点。  
> 原则：先跑通，再扩展；每步必须有验证命令。

---

## 1) 目标

- 在不编造结果的前提下，快速完成：环境可用 → 模型复制改名 → 注册 → prepare → import 验证 → 回归运行。

---

## 2) 前置条件

```bash
python3 --version
git --version
```

若 ANDES 未安装：
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install andes
andes --version
python -c "import andes; print(andes.__version__)"
```

---

## 3) 最小步骤（Checklist）

## Step A. 找到官方最小模板
```bash
cd ~/work/andes-dev/andes
rg -n "class Shunt" andes/models
```

## Step B. 复制并改名
```bash
cp andes/models/shunt.py andes/models/shuntlite.py
# 手动编辑类名：ShuntData/Shunt -> ShuntLiteData/ShuntLite
python -m py_compile andes/models/shuntlite.py
```

## Step C. 注册模型
```bash
# 编辑 andes/models/__init__.py 后验证
rg -n "ShuntLite" andes/models/__init__.py andes/models/shuntlite.py
```

## Step D. 生成/刷新数值代码
```bash
andes prepare -i
```

## Step E. 可运行验证
```bash
python - <<'PY'
from andes.models.shuntlite import ShuntLite
print('import ok:', ShuntLite.__name__)
PY
```

```bash
python - <<'PY'
import andes
ss = andes.load(andes.get_case('ieee14/ieee14_pvd1.xlsx'))
ss.PFlow.run()
print('PFlow exit:', ss.PFlow.exit_code)
PY
```

---

## 4) 命令与预期输出（速查）

- `andes --version` → 输出版本号
- `python -m py_compile andes/models/shuntlite.py` → 无输出且退出码 0
- `andes prepare -i` → 结束无异常
- `from andes.models.shuntlite import ShuntLite` → 打印 `import ok`
- `PFlow.exit_code` → 期望 `0`

---

## 5) 常见失败排查

### A. CLI 不存在
```bash
which andes
which python
```
处理：激活 venv，重新安装。

### B. 模块不可导入
```bash
python -c "import sys; print(sys.executable)"
python -c "import andes; print(andes.__version__)"
```
处理：确保使用同一 venv 解释器。

### C. prepare 失败
```bash
rg -n "ShuntLite|class" andes/models/shuntlite.py andes/models/__init__.py
```
处理：检查类名冲突、注册遗漏、拼写错误。

### D. case 路径错误
处理：改用本地可解析的官方 case，再验证 `PFlow.exit_code`。

---

## 6) 扩展建议（通过最小方案后）

1. 每次只引入一个新改动（参数/方程/离散逻辑三选一）；
2. 每次改动都重复：`py_compile -> prepare -> import -> PFlow`；
3. 记录失败日志与修复动作，形成个人建模回归清单。