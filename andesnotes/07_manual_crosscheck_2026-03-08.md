# ANDES 手册交叉映证（基于 docs-andes-app-en-v2.0-dev.pdf）

手册信息：
- 文件：`docs-andes-app-en-v2.0-dev.pdf`
- 版本标识（封面）：`Release 0.0.post50+g7101dce13`
- 页数：1031
- 阅读方式：本地提取目录与章节文本（pypdf）

## 1) 目录结构与核心主题（核验）

- Ch1 About ANDES
- Ch2 Tutorials（2.1~2.16）
  - 已见章节包含：Installation、First Simulation、Power Flow、TDS、Data & File Formats、Plotting、EIG、Parameter Sweeps、Contingency、Dynamic Control、Frequency Response、State Estimation、CPF、Inspecting Equations、RL with ANDES
- Ch3 Modeling Guide（3.1~3.4）
  - Modeling Concepts / Model Components / Creating Models
- Ch4 Reference（CLI / Configuration / Model Reference / Config Reference / API reference）

## 2) 对既有学习成果的映证

### A. 已覆盖并与手册一致
- Tutorials 02~11 + Inspecting（对应 2.3~2.11、2.15）
- Modeling Concepts（对应 3.2）
- Components（对应 3.3：Parameters/Variables/Services/Discrete/Blocks/Groups）
- Creating Models 核心示例（对应 3.4.4~3.4.8：Shunt/BusFreq/TGOV1/IEEEST/Testing）
- Reference 方向（CLI/Config 已建立笔记）

### B. 与手册比对后新增确认点
- Tutorials 实际扩展到 2.16（并非仅到 2.11/2.15）
- Advanced analysis topics 明确在教程主线内：
  - 2.12 Frequency Response and Load Shedding
  - 2.13 State Estimation
  - 2.14 Continuation Power Flow
  - 2.16 Reinforcement Learning with ANDES

## 3) 当前笔记缺口（仅基于手册目录事实）

1. Tutorials 后半段缺口：`2.12/2.13/2.14/2.16` 尚未形成独立深读笔记。
2. Reference 深度缺口：
   - `4.3 Model Reference`（大规模模型族条目）
   - `4.4 Config Reference`（System/PFlow/TDS/EIG/SE/CPF）
   - `4.5 API reference`（System/Routines）
3. 验证层缺口：尚无“实测运行截图/日志型证据”覆盖上述缺口章节。

## 4) 修正建议（可执行）

- 先补 Tutorials 2.12~2.14（贴近电力系统分析场景）
- 再补 2.16（RL）作为扩展
- 对 Reference 采用“按任务反查”而非全量抄录：
  - 先做 `4.1 CLI` + `4.2 Config` 命令索引
  - 结合实际模型需求再下钻 `4.3/4.4/4.5`

## 5) 结论

现有学习成果与手册主干结构一致，且 Creating Models 核心链路已闭环；
主要差距在 Tutorials 后半段（2.12~2.16）与 Reference 深水区（4.3~4.5）的系统覆盖。
