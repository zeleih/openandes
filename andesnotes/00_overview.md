# ANDES 学习笔记 - 总览

来源：`https://docs.andes.app/en/latest/`（首页）

## 项目定位
- ANDES 是开源 Python 电力系统建模与数值分析库。
- 核心能力：
  - 潮流计算（Power Flow）
  - 时域仿真/暂态稳定（Time-domain Simulation）
  - 小扰动稳定（Eigenvalue Analysis）
  - 符号-数值混合框架（用于快速模型原型开发）
  - 支持第二代新能源模型

## 文档结构（主导航）
- Tutorials
- Modeling Guide
- Reference
- Verification
- About ANDES

## 关键入口
- PDF Manual: `https://docs.andes.app/_/downloads/en/stable/pdf/`
- GitHub: `https://github.com/CURENT/andes`
- PyPI: `https://pypi.org/project/andes/`

## 快速安装
- conda: `conda install -c conda-forge andes`

## 快速示例
- `andes.load(andes.get_case('ieee14/ieee14_fault.xlsx'))`
- `ss.PFlow.run()`
- `ss.TDS.run()`
- `ss.TDS.plt.plot(ss.GENROU.omega)`

## Learning Paths（首页给出的路径）
- New User:
  - Installation
  - First Simulation
  - Power Flow Analysis
- Power System Analyst:
  - Data and File Formats
  - Eigenvalue Analysis
  - Parameter Sweeps and Batch Processing
- Model Developer:
  - Inspecting Model Equations
  - Hybrid Symbolic-Numeric Framework
  - Creating Models

## 我的理解
- ANDES 文档是典型 Sphinx 技术文档，路径清晰，适合按“用户角色”分层学习。
- 对我当前任务（细读手册）而言，最重要的是：Tutorials + Modeling Guide + Reference。
