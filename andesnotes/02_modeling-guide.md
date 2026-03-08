# ANDES 学习笔记 - Modeling Guide

来源：`modeling/index.html`

## 定位
Modeling Guide 面向开发者：
- 理解内部建模机制
- 自定义设备模型
- 扩展框架能力

## 章节结构

### 1) Modeling Concepts
- Hybrid Symbolic-Numeric Framework
- Atomic Types
- System Architecture
- DAE Formulation

### 2) Model Components
- Parameters
- Variables
- Services
- Discrete Components
- Blocks
- Groups

### 3) Creating Models
- Model Structure
- 示例：Shunt（静态模型）
- 示例：BusFreq（动态模型）
- 示例：TGOV1
- 示例：IEEEST
- Testing Models

## 我的理解
- 这是 ANDES 的“引擎层手册”，核心是 **符号建模 -> 自动生成数值计算代码**。
- 对研究型用户最大价值：避免手工推导雅可比和手写数值求解代码。
- 对工程实践价值：模型可复用、可测试、可版本化。

## 后续精读计划
- 优先读 `framework-overview` 与 `dae-formulation`。
- 再读 `creating-models` 的 4 个官方示例，提炼模板化开发流程。
