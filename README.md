# openandes

OpenAndes is a chat-driven workflow for high-intensity power-system simulation using OpenClaw + ANDES.

Recommended model: Codex 5.3 or above.

## Repository Structure
- `andesnotes/`: learning outputs, distilled notes, and simulation memory files
- `simulations/test/`: archived simulation assets, run outputs, figures, and summaries
- `repos/`: external upstream links and submodule pointers

## Self-Learning and Evolution
OpenAndes has a practical self-learning and evolution capability powered by simulation memory files (for example, `andesnotes/12_andes_simulation_memory.md`).

As you use the system more and provide corrections, the workflow captures:
- what worked,
- what failed,
- root causes,
- and validated fixes.

Over time, this makes the simulation process more reliable, more reusable, and progressively more intelligent.

## Remote Simulation from Mobile Chat
You can trigger remote simulations on your computer directly from chat apps, such as:
- Feishu
- WhatsApp
- and similar messaging channels supported by your OpenClaw setup.

This enables a mobile-first control loop: request, run, debug, and receive results without logging into the remote machine manually.

## Official References
- ANDES repository: https://github.com/CURENT/andes
- ANDES docs: https://docs.andes.app/
- Demo repository: https://github.com/CURENT/demo

## Notes
- Python environments are intentionally excluded from this repository.
- External repositories are references to official upstream sources.

If you need to know openclaw from the beginning，check this doc below:
https://my.feishu.cn/wiki/H27Iw9ussiaYbokymhncExtjnAh?from=from_copylink