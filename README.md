# AI 与开发者热点日报

这是一个完全托管在 GitHub Actions 上的 Python 自动化项目。它每天收集近 24 小时的 AI、计算机、编程、开源与开发者工具动态，使用 OpenAI 生成中文摘要，并通过 Resend 发送一封适配 Outlook 的 HTML 邮件。

任务由 GitHub 托管的运行器执行：**电脑关机、休眠或断网都不会影响执行**。只要 GitHub 仓库、Actions 和所需密钥仍可用，工作流会继续运行。

## 工作流

1. 并行读取 OpenAI、Google AI、Anthropic、Microsoft Developer、GitHub、Python、Rust、Kubernetes 的公开 RSS。
2. 读取 GitHub Search API 中新建且有热度的仓库，以及 Hacker News 热门技术故事。
3. 仅保留发布时间在最近 24 小时内、主题相关且非明显推广的条目；按来源可信度、主题相关度和社区热度排序、去重，最多选择 12 条。
4. 向 OpenAI 提供标题、来源、时间与来源摘录；模型只能据此编写中文标题、2–4 句摘要和标签。原始链接与来源不会交给模型改写。
5. 渲染 HTML 并通过 Resend API 发至微软邮箱。

当新闻源短暂不可用时，其他来源会继续执行；当模型调用失败时，邮件会明确标注为“基于来源原文”的兜底内容，绝不伪造摘要。

## 部署到 GitHub

1. 将本目录推送至一个 GitHub 仓库。
2. 在仓库中进入 **Settings → Secrets and variables → Actions → New repository secret**，添加以下 Secrets：

| Secret | 必填 | 说明 |
| --- | --- | --- |
| `OPENAI_API_KEY` | 是 | OpenAI API 密钥。 |
| `RESEND_API_KEY` | 是 | Resend 的 API 密钥。 |
| `SENDER_EMAIL` | 是 | Resend 中已验证域名下的发件人，例如 `AI 日报 <digest@example.com>`。 |
| `RECIPIENT_EMAIL` | 是 | 你的微软收件邮箱，例如 `name@outlook.com`。 |
| `OPENAI_MODEL` | 否 | 覆盖默认模型；未配置时使用 `gpt-4.1-mini`。请填你账户可用的模型。 |

3. 在 Resend 中添加并验证你的发件域名，然后按其 DNS 指引添加 SPF/DKIM 记录。生产环境中，`SENDER_EMAIL` 必须使用该已验证域名；否则 Resend 会拒绝发送或只允许受限的测试收件人。
4. 打开仓库的 **Actions** 页面，选择 **Daily Chinese Tech Digest**，点击 **Run workflow** 测试。先确认邮件能到达 Outlook，再等待定时任务。

## 定时时间与可靠性

`.github/workflows/daily-digest.yml` 使用 `0 0 * * *`。GitHub Actions 的 cron 使用 UTC，UTC 00:00 正好是北京时间（UTC+8）08:00，中国没有夏令时。

GitHub 托管调度通常会在该时点启动，但公共 GitHub Actions 的 scheduled workflow 可能因平台负载而稍有延迟；它不是严格实时调度。电脑状态不参与该流程。

若仓库是公开仓库且连续 60 天没有任何仓库活动，GitHub 可能自动停用 scheduled workflow。要长期保持每日投递，请定期查看 Actions 页面并重新启用被停用的工作流；该闲置规则在 GitHub 文档中明确针对公开仓库。

## 本地运行

需要 Python 3.11+：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

在 `.env` 中填写自己的值后，将其加载进当前 PowerShell 会话（或使用你惯用的环境变量工具），然后运行：

```powershell
python -m src.main
```

`.env` 已被 `.gitignore` 忽略，绝不能提交密钥。程序本身不自动读取 `.env`，避免在 GitHub 上混淆 Secrets；本地可以手工设置环境变量，或使用你自己的安全加载方式。

## 排查

- **工作流在配置阶段失败**：核对四个必填 Secrets 名称是否完全一致，重新从 Actions 页面手动运行。
- **Resend 返回 403 或 422**：通常是发件域名未验证、发件人地址不属于该域名，或测试账号没有获准向该收件人发信。
- **收不到 Outlook 邮件**：检查垃圾邮件/“其他”收件箱，并确认域名 SPF/DKIM 验证已完成。
- **邮件项目较少**：项目严格限制在近 24 小时、可信且相关的内容；它宁可少发，也不会为了凑数而编造热点。
- **某个新闻源失败**：查看 GitHub Actions 日志。单个来源失败只会记录 warning，不会中断其他来源或邮件投递。
- **OpenAI 摘要失败**：日志会记录原因；邮件会发送可核验的原始来源兜底内容。确认 API Key、模型名和账户额度。

## 安全边界

项目不包含真实密钥，也不写入或输出密钥。GitHub Actions 仅授予 `contents: read` 权限，密钥只通过 Actions Secrets 注入运行环境。
