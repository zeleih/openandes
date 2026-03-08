# ANDES 学习笔记 - Components + Creating Models 深读（本轮）

来源：
- modeling/components/{parameters, services, discrete, blocks, groups}
- modeling/creating-models/model-structure
- modeling/creating-models/example-static
- modeling/creating-models/testing-models

---

## 1) Parameters（参数体系）

### 核心认知
- 参数是 `v-provider`，用于给方程提供值。
- 常见类型：
  - `NumParam`：数值参数（可默认值/约束/TeX）
  - `IdxParam`：索引参数（跨模型引用入口）
  - 以及外部参数 `ExtParam`（通过 group/indexer 取其它模型参数）

### 工程意义
- 参数定义是模型可移植性的核心：输入数据、单位、约束统一。
- `mandatory=True`、`non_zero=True` 等约束可提前暴露数据问题。

---

## 2) Services（服务体系）

### 核心认知
- Service 是“中间计算层”，不直接作为未知变量求解。
- 常见：
  - `ConstService`：常量型表达
  - `VarService`：依赖变量动态更新
  - `BackRef`：反向连接关系（例如 Bus 收集挂接设备 idx 列表）

### 工程意义
- 把复杂方程拆成“可读中间项 + 最终方程”，便于调试与审计。

---

## 3) Discrete Components（离散组件）

### 核心认知
- 离散组件用于分段逻辑/限幅/比较/切换。
- 典型导出 flag：
  - `Limiter` 导出 `zi/zl/zu`（在界内/下越/上越）
- 更新时序非常关键：
  - `check_var`：方程求值前更新变量类 flag
  - `check_eq`：方程求值后更新方程类 flag
  - `set_var`：求解后回写（如 AntiWindup 状态钳位）

### 高价值组件
- `Limiter`, `HardLimiter`, `SortedLimiter`
- `RateLimiter`, `AntiWindup`, `AntiWindupRate`
- `LessThan`, `Switcher`, `DeadBand`, `Delay`, `Sampling`

### 实操纪律
- 分段方程用 flag 拼 `e_str`，不要写散乱 if-else 逻辑。
- RateLimiter 与 AntiWindup 叠加要按文档建议用组合版本（AntiWindupRate）。

---

## 4) Blocks（控制积木）

### 核心认知
- Block 是“预定义变量+方程”的可复用子系统（类似控制模块库）。
- 所有导出元素必须注册到 `self.vars`。
- 可嵌套，但官方建议不要超过 1 层，避免命名膨胀。

### 典型块族
- 线性传函：`Gain`, `Lag`, `Washout`, `LeadLag`, `Lag2ndOrd`
- 含约束：`GainLimiter`, `LagAntiWindup`, `LagRate`, `LeadLagLimit`
- 控制器：`PIController`, `PIDController`, tracking/anti-windup/freeze 变体
- 非线性门控：`HVGate`, `LVGate`, `Piecewise`, `DeadBand1`

### 命名机制（关键）
- 父块名 + 子块名 + 变量名拼接（如 `A_B_x`），由框架自动传播。
- 写 `define()` 时必须用运行期最终名模式（`{self.name}_v`）。

---

## 5) Groups（分组与多态接口）

### 核心认知
- Group 是“同类模型的统一接口契约”。
- 作用：
  - 公共参数/变量接口
  - 模型多态替换（如 GENCLS ↔ GENROU）
  - 跨模型引用兼容
  - 反向连接查询（BackRef）

### 典型标准组
- `StaticGen`, `SynGen`, `Exciter`, `TurbineGov`, `PSS`, `StaticLoad`, `RenGen` 等。

### GroupBase 常用能力
- `add_model`, `add`, `get`, `set`, `alter`, `find_idx`, `idx2model`, `idx2uid`, `doc_all`。

### 实操价值
- 通过 group + indexer 设计，能做到“替换模型不改 case 文件”。

---

## 6) Creating Models - Model Structure（建模骨架）

### 标准两类
1. `ModelData`：参数定义
2. `Model`：行为定义（flags/group/service/var/equation）

### 推荐组件顺序
1) flags/group → 2) config → 3) const/ext services → 4) ext params/vars → 5) var services → 6) discrete/blocks → 7) Algeb/State

### flags
- `pflow`, `tds`, `tds_init` 决定参与的分析流程。

### 注册与代码生成
- 模型加到 `andes/models/__init__.py`。
- 修改后执行：`andes prepare -i`。

---

## 7) Example: Static Model (Shunt)

### 学到的重点
- Static 模型只提供代数方程，不含状态变量。
- `Shunt` 用 `ExtAlgeb` 直接挂到 `Bus.a / Bus.v`。
- 方程体现恒阻抗特性：
  - `P = V^2 g`
  - `Q = -V^2 b`
- `y=True` 参数标注与导纳矩阵相关，利于稀疏求解。

### 关键启发
- 这是最清晰的“Data/Model 分离 + 外部变量注入 + 代数注入”模板。

---

## 8) Testing Models（测试体系）

### 三层测试
1. Unit：能实例化、参数可读
2. Integration：系统内潮流/暂态能跑
3. Verification：与参考工具（如 PSS/E）对比

### 必做用例
- PFlow 收敛
- TDS 平跑不漂移
- 扰动后 `exit_code==0`
- 初始化残差 `f/g` 足够小
- 关键变量边界检查（如频率、电压）

### 调试工具链
- 看 `dae.f/dae.g` 残差
- 看 Jacobian 稀疏图（`spy(gy)`）
- 缩小步长+缩短仿真窗口+DEBUG日志

---

## 阶段总结
- 我已经把 ANDES 的“建模中台”基本打通：
  **参数/服务/离散/块/分组/骨架/测试** 七件套。
- 下一个阶段将补齐 Creating Models 剩余示例页的细化要点：
  - Dynamic (BusFreq)
  - TGOV1
  - IEEEST
（本轮中部分页面 snapshot 出现 tab 丢失，后续重开单页补齐）
