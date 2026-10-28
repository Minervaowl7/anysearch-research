# AnySearch Research 1.1.1

独立集成，非 AnySearch 官方出品。使用官方托管 MCP 与官网原始方形标志，
不代表官方授权、背书或已通过公共目录审核。

## 安装与使用

在现有插件页面安装／启用并完成连接确认；不要重复注册同名连接。
更新后在新对话中检查技能和工具是否加载，再执行一次公开资料搜索。
插件直连 https://api.anysearch.com/mcp，普通使用无需本地 CLI、代理或后台进程。
已保存、已安装、已连接与业务实测成功是四种不同状态。
API Key 可选；按宿主支持的私密凭证流程配置，匿名额度以实际返回为准。

## 工作流

| 场景 | 行为 |
| --- | --- |
| 普通查询 | 单意图通用搜索；摘要不足时再提取决定性来源。 |
| 专业查询 | 先发现相关领域，使用实际返回的子领域和参数。 |
| 模糊或跨领域问题 | 通用查询与相关垂直查询组成混合批次，每次最多五组。 |
| 领域字典 | 本轮按领域复用；参数错误或实际变化时刷新。必填而不适用的参数传空字符串。 |
| 评分反馈 | 每条成功搜索保留真实请求标识并按 1–5 分评价；累计十条及本轮检索结束时提交。 |
| 科技查新 | 保留技术关系、数值与时序，逐篇比较；不拼接多篇冒充单篇覆盖。 |
| 正文与引用 | 标明全文未读、截断、日期未核等边界，引用可追溯来源。 |

评分提交只携带请求标识和分数；成功但无结果仍需评价，失败搜索及正文提取不计入。
批次逐项判断成功与失败；不重复提交已排队的评分，不把排队确认当作数据库持久化。
详情见[搜索技能](skills/anysearch-search/SKILL.md)和[接口对齐说明](skills/anysearch-search/references/interface-alignment.md)。

## 接口边界

search 的 max_results 使用整数 1–10；batch_search 最多五组，各组自行填写参数。
当前 MCP 使用 domain、sub_domain、对象形式的 sub_domain_params。
官方独立 Skill 的 tag、params、zone、language 和 CLI 共享参数不直接适用于此 MCP。
extract 支持 HTML/XHTML、纯文本、JSON、Markdown；不解析 PDF、Word、图片及其他二进制文件。
HTML／纯文本可能在 50,000 字符处截断，过大的 JSON／Markdown 可能报错。

原有四工具仍带相互矛盾的只读／破坏性标注；score 标注为非只读、非破坏性、幂等反馈。
这些是提供方实时标注，不由本包修改；尊重宿主实际权限决定。
服务能力与文档可能不同步，按实时契约和实际返回核验，不能照抄旧示例。

## 验证与维护

本轮已取得公开搜索、通用／学术／专利混合批量、领域字典及正文提取的可用返回；
三条评分收到排队确认、无拒收。此前传输错误本次未复现。
认证场景、新版本安装后端到端及完整行为验收尚未完成。
最新逐项状态见[验收记录](evidence/VERIFICATION.md)；历史快照保留原日期。
离线单元测试、真实服务调用、工作流质量和安装后验收分别记录，不互相替代。

开发者在包根目录运行：

```sh
python tools/validate_package.py
python -m unittest discover -s tests -v
python tools/build_package.py --output ../anysearch-research-1.1.1.zip
```

这些开发命令只做离线校验和打包。行为用例保存在 tests/behavior-cases.json，
执行结果另存 evidence/behavior-results.json。凭证与传输边界见[安全说明](SECURITY.md)。

## 从公开仓库安装

```sh
codex plugin marketplace add Minervaowl7/anysearch-research
codex plugin add anysearch-research@anysearch-research
```

安装后新开对话。已有官方 Skill/MCP 与其他集成；本项目聚焦独立的原生 MCP 插件和查新工作流，不声称首创。
本项目代码和原创工作流按 MIT 开源，官方标志的权利不包含在 MIT 授权中。
GitHub 开源不等于公共插件目录上架。相关项目与安装边界见[英文说明](README.md)。
