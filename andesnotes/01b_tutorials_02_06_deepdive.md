# ANDES 学习笔记 - Tutorials 02~06 深读

来源：
- 02-first-simulation
- 03-power-flow
- 04-time-domain
- 05-data-and-formats
- 06-plotting-results

---

## 02 First Simulation

### 最短闭环（5分钟）
1. `andes.load(get_case(...))` 加载案例（System 对象）
2. `ss.PFlow.run()` 建立稳态工况
3. `ss.TDS.config.tf = ...; ss.TDS.run()` 做暂态仿真
4. `ss.TDS.plt.plot(ss.GENROU.omega)` 看转速响应
5. 新建系统 `ss2` 再做 `EIG.run()`（避免 TDS 改写状态影响特征值分析）

### 关键认知
- `System` 是统一容器：模型、参数、例程、输出全在里面。
- 输出文件默认生成：`*_out.txt`, `*_out.lst`, `*_out.npz`。
- CLI 与 Python 接口一一对应：`andes run/plot`。

---

## 03 Power Flow Analysis

### 求解器与收敛
- 方法：Newton-Raphson
- 常见迭代：3~6 次
- 关键配置：
  - `max_iter`（默认 25）
  - `tol`（默认 1e-6）
  - `method='NR'`
  - `init_tds`（是否联动初始化动态模型）

### 结果读取
- 母线电压幅值：`ss.Bus.v.v`
- 母线角度：`ss.Bus.a.v`
- 发电机有功/无功：`ss.PV.p.v`, `ss.PV.q.v`, `ss.Slack.p.v`
- 线路潮流：`ss.Line.a1.v`, `ss.Line.a2.v`
- DataFrame 全量表：`ss.Bus.cache.df`

### 排障框架
- 不收敛通常来自：
  1) 拓扑/数据问题（孤岛、零阻抗等）
  2) 不可行工况（功率平衡/无功支撑不足）
  3) 初值太差
- 手段：增大 `max_iter`、启用 PV-PQ 转换、开 DEBUG 看残差轨迹。

---

## 04 Time-Domain Simulation

### 核心机制
- 求解对象：DAE
- 数值法：隐式梯形（A-stable）
- 必须先有收敛潮流

### 扰动建模三件套
1. `Fault`：三相故障（`bus`, `tf`, `tc`, `rf`, `xf`）
2. `Toggle`：设备切除/重合（线路、机组、负荷等）
3. `Alter`：仿真中改参数/设定值（`src`, `method`, `amount`）

### 非常关键的工程细节
- 增加扰动前通常要 `setup=False` 加载，修改后 `setup()`。
- 动态模型会接管对应静态模型（如 `GENROU` 接管 `PV/Slack`）。
  - 因此仿真中改 `PV.p0` 常常无效；应改 `TGOV1.pref0/paux0`。

### 常用配置
- `tf`, `tstep`, `max_iter`, `tol`, `fixt`
- 时序结果：`ss.dae.ts.t / x / y`
- 地址映射：变量 `a` 属性（状态取 `x`，代数取 `y`）

### 常见排障
- TDS 步进不收敛：减小 `tstep`、增大 `max_iter`
- 先 `TDS.init()` 做初始化检查
- `--flat` 做平跑检查

---

## 05 Data and File Formats

### 支持格式
- ANDES 原生 `.xlsx`（推荐）
- PSS/E `.raw + .dyr`
- 其他互操作格式（文档另章）

### 数据读取与改写
- 读取：`andes.load(...)`
- 查看参数表：`model.cache.df`（pu后） / `model.cache.df_in`（原始输入）
- 读单参数：`model.get('param', idx)`
- 改参数：`model.alter('param', idx, value)`
- 批量改：直接改 `param.v[:]`
- 改完需 `cache.refresh()` 更新视图

### 索引体系
- 外部索引：`idx`（可字符串）
- 内部位置：`uid`（0-based）
- 转换：`idx2uid()`

### 保存
- `andes.io.xlsx.write(system, 'xxx.xlsx', overwrite=True)`

---

## 06 Plotting Results

### Plotter 对象
- `ss.TDS.plt`（若为空可 `ss.TDS.load_plotter()`）

### 两种绘图入口
1. 按变量对象：`plot(ss.GENROU.omega)`（最推荐）
2. 按索引：`plot((5,6,7,8))`（与 CLI 一致）
   - 索引查找：`ss.TDS.plt.find('omega')`

### 常用参数
- `a`（子集选择）
- `ylabel`, `yheader`
- `ycalc`（单位变换，如 pu→Hz）
- `grid`, `greyscale`
- `savefig`, `dpi`
- `fig`, `ax`（叠加曲线）

### 数据导出
- 全量 CSV：`ss.TDS.plt.export_csv('x.csv')`
- 自定义导出：直接拼 `ss.dae.ts` + pandas

---

## 阶段性总结（02~06）
- ANDES 教程不是“功能演示”，而是一条完整工程链：
  **数据 -> 潮流 -> 暂态 -> 可视化 -> 导出 -> 排障**。
- 对实操最有价值的隐性知识：
  1) 动态/静态模型接管关系
  2) setup 时机与事件注入顺序
  3) 地址系统（变量对象 vs 索引）
