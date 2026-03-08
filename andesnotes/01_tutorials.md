# ANDES 学习笔记 - Tutorials

来源：
- `tutorials/index.html`
- `tutorials/01-installation.html`

## 教程总览
教程链路覆盖：
1. Installation
2. First Simulation
3. Power Flow Analysis
4. Time-Domain Simulation
5. Data and File Formats
6. Plotting Results
7. Eigenvalue Analysis
8. Parameter Sweeps and Batch Processing
9. Contingency Analysis
10. Dynamic Control and Setpoint Changes
11. Frequency Response and Load Shedding
12. Inspecting Model Equations

### 学习路径
- New User：01-06
- Power System Analyst：07-11
- Model Developer：先完成基础后进入 Modeling Guide

---

## Installation 细节

### 快速安装
- 推荐：`conda install -c conda-forge andes`
- 也支持 pip、uv。

### 新手环境建议
- 推荐 Miniforge + conda-forge。
- Apple Silicon 建议 `arm64` 安装包。
- 建议单独环境：
  - `mamba create --name andes python=3.11`
  - `mamba activate andes`

### uv 路径
- `uv pip install andes`
- 新环境示例（3.12）
- 支持 `andes[dev]`。

### 扩展依赖组
- `dev`：测试/文档
- `interop`：与其他电力系统工具互操作
- all extras：`pip install andes[all]`

### 开发安装
- `git clone https://github.com/curent/andes`
- `pip install -e .`
- dev 模式下更新用 `git pull`，不要混用 conda/pip 造成重复安装。

### 升级与排障
- conda：`conda install -c conda-forge --yes andes`
- pip：`pip install --upgrade andes`
- uv：`uv pip install --upgrade andes`
- 典型问题：多副本安装、Windows DLL load failed（建议 conda 环境）。

## 我的理解
- 官方非常强调“环境隔离 + 不混装 + 版本可追踪（setuptools-scm）”。
- ANDES 在安装策略上对开发者和普通用户的路径区分清楚。
