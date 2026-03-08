# ANDES 学习笔记 - Tutorials 07~11 + Inspecting Models 深读

来源：
- 07-eigenvalue-analysis
- 08-parameter-sweeps
- 09-contingency-analysis
- 10-dynamic-control
- 11-frequency-response
- inspecting-models

---

## 07 Eigenvalue Analysis（小扰动稳定）

### 核心流程
1. 建立运行点（自动先跑潮流）
2. 线性化得到状态矩阵
3. 计算特征值并统计正/零/负根
4. 用 s-plane 图解释稳定性与阻尼

### 关键结论
- 实部 < 0：稳定模态；实部 > 0：不稳定。
- 虚部决定振荡频率。
- 零特征值通常对应角度参考自由度（物理可接受）。

### 工程能力
- `ss.EIG.plot()` 看模态分布。
- `ss.EIG.sweep(param, idx, range)` 做根轨迹，直接用于控制参数整定（如 EXDC2.KA）。
- `*_eig.txt` 报告包含阻尼比、频率、关联状态。

---

## 08 Parameter Sweeps & Batch Processing

### 三种批量范式
1. **文件批处理 + CLI 并行**（大规模研究首选）
   - 先批量生成 case 文件，再 `andes run batch/*.xlsx -r tds --ncpu N`。
2. **Python 循环内存扫参**（小规模、快速试验）
3. **`pool=True` 并行返回 System 对象**（中规模、需程序化后处理）

### 选择原则
- >100 场景：文件并行
- 中等：pool=True
- 小样本：单进程循环（开发最快）

### 关键认知
- ANDES 的批处理并不是“附带功能”，而是完整实验流水线能力。

---

## 09 Contingency Analysis（N-1与故障清除）

### 标准流程
1. 枚举待测元件（Line/Gen/Bus）
2. 每个场景新建系统并注入扰动
3. 运行 TDS
4. 用统一稳定性指标打分

### 常见指标
- `omega_max < 1.05`
- `omega_min > 0.95`
- `v_min > 0.8`
- `exit_code == 0`

### CCT（临界切除时间）
- 文档给出二分搜索模板，按稳定/失稳更新上下界。
- CCT 是保护定值与系统韧性核心指标。

---

## 10 Dynamic Control & Setpoint Changes（分阶段仿真）

### 关键机制
- `ss.TDS.run()` 可多次调用，仿真从当前状态继续推进。
- 两次 run 之间可修改设定值（例如 `TGOV1.paux0`），实现 AGC/调度/控制策略注入。

### 实操注意
- 参数数组修改必须“原地写入”（in-place）。
- 控制注入后再继续到新 `tf`。

### 应用场景
- 经济调度跟踪
- AGC 频率调节
- 电压设定值控制
- 强化学习闭环控制

---

## 11 Frequency Response & Load Shedding

### 研究对象
- 发电机跳机后的频率跌落与恢复。
- UFLS（低频减载）动作效果。

### 关键流程
1. 注入发电机跳闸（Toggle）
2. 观察频率跌落（Governor droop 形成低于额定的新平衡）
3. 定量估算功率缺额
4. 在第二阶段按策略减载（修改 `PQ.Ppf`）
5. 继续仿真验证频率恢复

### 核心概念
- Droop 控制不是等频控制，故障后稳态频率通常低于额定。
- 减载若接近缺额，可显著恢复频率。
- RoCoF 与系统惯量强相关。

---

## Inspecting Model Equations（模型方程审查）

### 能力入口
- `ss.supported_models()`：列模型清单。
- `model.prepare()`：准备符号方程。
- `model.doc()`：输出完整模型文档（参数、变量、方程、服务、配置）。

### 符号对象
- `syms.xy`：变量向量
- `syms.f`：微分方程 RHS
- `syms.g`：代数方程 RHS
- `syms.df`, `syms.dg`：雅可比
- `syms.s`：服务方程

### 实际价值
- 验证：检查模型物理含义是否正确
- 调试：定位异常响应来源
- 扩展：开发新模型前的结构基线
- 报告：生成可引用的数学表达

---

## 阶段结论（Tutorials 基本闭环完成）
- 我已把 Tutorials 从“功能使用”提升到“实验设计 + 批量分析 + 稳定性判据 + 方程审查”的层级。
- 当前可以直接支撑：
  1) 小扰动稳定研究（EIG + 根轨迹）
  2) 大规模 N-1 批处理
  3) 分阶段控制策略仿真
  4) 跳机与减载策略评估
  5) 模型级方程审计
