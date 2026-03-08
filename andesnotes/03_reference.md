# ANDES 学习笔记 - Reference

来源：
- `reference/index.html`
- `reference/cli.html`
- `reference/configuration.html`

## Reference 总体结构
- Command Line Interface
- Configuration
- Model Reference（大量模型页面）
- Config Reference
- API reference
- Release notes

---

## CLI 关键点

### 命令总览
- `andes run`：运行仿真
- `andes plot`：绘制时域结果
- `andes doc`：查询模型/例程文档
- `andes prepare`：从符号模型生成数值代码
- `andes selftest`：安装验证
- `andes misc`：杂项工具

### run 常用
- 默认潮流：`andes run case.xlsx`
- 时域：`andes run case.xlsx -r tds`
- 特征值：`andes run case.xlsx -r eig`
- PSS/E：`andes run system.raw --addfile system.dyr -r tds`
- 配置注入：`-O Section.option=value`
- 并行批量：`andes run *.xlsx -r tds --ncpu 4`

### plot 常用
- `andes plot case_out.lst 0 5`
- 支持变量范围、按名称搜索、导出 CSV。

### 其他
- `andes prepare -f/-i/-q`
- `andes selftest -q`
- `andes misc --edit-config`、`-C` 清理输出

### 运行噪声控制
- `-v 10/20/30/40`（DEBUG/INFO/WARNING/ERROR）
- 环境变量：
  - `ANDES_USE_UMFPACK`
  - `ANDES_DISABLE_NUMBA`

---

## Configuration 关键点

### 三层配置
- System：全局
- Routine：分析例程级（PFlow/TDS/EIG）
- Model：模型级（如 TGOV1）

### 配置查看
- `ss.config`
- `ss.PFlow.config`
- `ss.TDS.config`
- `ss.TGOV1.config`

### 配置修改路径
1. 运行前 Python 改写
2. `andes.run(..., config_option=[...])`
3. CLI `-O`
4. 持久化 `~/.andes/andes.rc`（`andes --save-config`）

### 常见选项（文档给出默认值）
- System: `freq=60`, `mva=100`, `numba=1`
- PFlow: `tol=1e-6`, `max_iter=25`, `sparselib=klu`
- TDS: `tf=20`, `tstep=1/30`, `fixt=1`, `max_iter=15`, `tol=1e-6`

### 稀疏求解器
- 推荐 KLU（默认），可切 UMFPACK / KVXOPT。

### 限值自动调整
- `allow_adjust`, `adjust_lower`, `adjust_upper`
- 官方强调：可保仿真继续，但可能掩盖数据质量问题。

## 我的理解
- ANDES 的 CLI 和配置体系非常工程化，适合“脚本化批量研究 + 可复现实验”。
- 建议未来固定模板：`run + -O + 输出目录 + 日志等级`。
