# 验收记录 — 2026-10-28（Asia/Shanghai）

本文件记录当前验收边界。2026-10-09 的原始四工具快照单独保留，不改写成新接口。

## 当前接口

实时发现五个工具：search、batch_search、get_sub_domains、extract、score。
原有四工具的参数结构与历史快照一致，说明文本有更新。score 为新增反馈接口。
当前参数、输出结构与权限标注的投影见 live-discovery-2026-10-28.json。
不保存会话标识、真实查询请求标识、用户凭证或本机路径。

## 已观察到的业务操作

- 公开资料单次搜索成功，返回可用 URL。
- 两组通用批量搜索成功；不代表五组上限或部分成功场景已验证。
- academic、code、ip 领域发现成功，返回可用子领域及参数。
- 公开 HTML、Markdown、JSON 文本提取成功；不代表超长截断和全部错误场景已验证。
- 一次真实评分收到 queued 确认；只证明已接收排队，不证明数据库持久化。
- 较早的 academic/ip 批量搜索与另一评分提交遇到传输错误，未记为成功。
- 最新一次通用／academic.paper／ip.global 三组混合批量成功。专利结果有公开号、无直链；不据此宣称全文与日期已核验。
- 最新三条评分统一提交，返回 queued=3、rejected=0；此前传输错误本次未复现。

## 离线验证及未完成项

离线结构／契约回归测试另见 offline-tests.txt 和 status.json。
行为用例定义与 evidence/behavior-results.json 中的实际执行记录分开。
反馈阈值、去重与评分判断仍是技能执行规则，不能把文字存在当作行为测试通过。
新发布版本的安装后端到端、私密 Key 认证、完整行为用例及长期稳定性尚未验证。
本次未创建账号、保存凭证或提交公共目录；production_acceptance 保持 NOT_COMPLETE。

## 对齐依据

- https://github.com/anysearch-ai/anysearch-skill/releases/tag/v3.1.1
- https://github.com/anysearch-ai/anysearch-skill/blob/main/SKILL.md
- https://github.com/anysearch-ai/anysearch-skill/blob/main/scripts/shared/doc_spec.md
- https://github.com/anysearch-ai/anysearch-mcp-server

官方独立 Skill、静态 MCP README 与实时 MCP 的路由描述及工具数量存在差异。
本包保留 native MCP，按当前契约调用，并在 interface-alignment.md 中解释差异。
