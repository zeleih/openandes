# ANDES 学习笔记 - Creating Models 高级示例（BusFreq / TGOV1 / IEEEST）

来源：
- `creating-models/example-dynamic`
- `creating-models/example-tgov1`
- `creating-models/example-ieeest`

---

## 1) BusFreq（动态测量模型）

### 定位
- 这是“只读型动态模型”：读取母线角/电压，输出局部频率估计，不向网络注入功率。
- 仅参与 TDS：`flags.tds = True`，不参与潮流。

### 关键链路
1. `ExtService` 捕获初始相角 `a0`（来自潮流初值）
2. `ExtAlgeb` 读取当前相角 `a`
3. `Lag` 对 `(a-a0)` 低通滤波（抗噪）
4. `Washout` 近似求导，得到频率偏差 `WO_y`
5. `Algeb` 输出 `f = 1 + WO_y`

### 关键启发
- 动态模型可通过 blocks 自动创建内部状态，开发时不必手写全部状态方程。
- 测量模型常用“读取外部变量 + 信号链处理 + 本地输出”的结构。

---

## 2) TGOV1（两种实现范式）

### 模型结构
- droop + lag(含anti-windup) + lead-lag + 阻尼项 Dt。

### A. Equation-based
- 明确写 `State/Algeb` 与 `e_str`。
- 优点：完全可控，可实现非常规结构。
- 缺点：代码长、出错概率高。

### B. Block-based
- 用 `LagAntiWindup`, `LeadLag` 等标准块拼接。
- 优点：可读性高、贴近控制框图、实现快。
- 缺点：受现有块能力边界约束。

### 官方实践结论
- 性能基本相同。
- 常规控制器优先 block-based；特殊结构再用 equation-based 或混合。

---

## 3) IEEEST（复杂PSS示例）

### 复杂点
- 多输入模式（速度/频率/功率/加速功率/电压/dVdt）
- 多级传函链（二阶滤波 + 两级lead-lag + 增益 + washout/lag）
- 限幅与模式切换
- 可选远端母线

### 关键技术件
1. `Replace`：替换无效输入（如 0 限值）
2. `DataSelect`：可选参数回退（远端母线缺省时用本地母线）
3. `DeviceFinder`：查找或自动创建关联测量设备（如 BusFreq）
4. `Switcher`：将 MODE 解码成 `SW_s1..SW_s6` 标志
5. `Derivative`：模式6需要 `dV/dt`
6. `ExtService(attr='pu_coeff')`：机组基值到系统基值的转换系数

### 输入信号构造方式
- 用 `Switcher` 标志做分段加权和，仅激活当前模式对应项。
- `v_str` 与 `e_str` 分开写，提高初始化与方程可读性。

### 组接口要求
- PSS 组要求共同输出变量 `vsout`，用于统一接入 Exciter。

---

## 4) 我提炼的建模方法论（可直接复用）

1. **先定接口，再定方程**
- 先定义 Group/common vars 和外部连接，再写内部动态。

2. **先可运行，再可优化**
- 首版优先 block-based 验证行为；再按需要切 equation-based。

3. **离散逻辑显式化**
- 所有限幅/切换尽量用 Discrete 组件表达，避免隐式 if-else。

4. **初始化优先级高于动态细节**
- `ExtService`、`v_str`、初始化残差检查是防崩关键。

5. **复杂模型必须三层测试**
- unit + integration + verification（与参考工具对比）。

---

## 当前状态
- Creating Models 四个核心示例（Shunt/BusFreq/TGOV1/IEEEST）已完成。
- 建模从入门到高级控制器实现路径已闭环。
