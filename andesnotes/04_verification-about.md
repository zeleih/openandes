# ANDES 学习笔记 - Verification & About

来源：
- `verification/index.html`
- `about.html`

## Verification

### 验证目标
- 与商业软件比对，验证模型与算法正确性（时域仿真结果）。

### 对标对象
- PSS/E
- TSAT
- 已发表基准数据

### 典型系统
- IEEE 14-bus：结果高度一致
- NPCC：多区域多模型系统，对商业工具比对
- WECC：大系统含新能源，存在轻微差异（多工具在大系统下本就难完全一致）

### 比对方法
- 参数一致
- 扰动一致
- 时间步尽量可比
- 比对变量：转子角、转速、母线电压

## About

### 项目定位
- ANDES 是 CURENT Large Scale Testbed 的动态仿真引擎之一。

### 核心技术
- 符号-数值混合框架：
  - Python + SymPy 写模型
  - 自动生成优化后的数值代码
  - 代码缓存复用（符号开销不是每次都付）

### 能力宣称（文档给出）
- 覆盖传统机组控制模型 + 新能源二代模型（含 WECC 规范）
- 支持 PSS/E raw/dyr 直接解析
- 大系统仿真性能可在桌面机达到秒级（文档示例口径）

### 引用
- H. Cui, F. Li, K. Tomsovic, IEEE TPWRS 2021, DOI: 10.1109/TPWRS.2020.3017019

### 许可
- GPL v3

## 我的理解
- ANDES 的“可信度”来自两条线：
  1) 可解释的符号建模流程
  2) 与商业工具和标准测试系统的系统性对比
