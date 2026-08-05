# UploadToGithub

交互式 Git 提交与推送助手。它检查当前仓库、Git 用户和 `origin`，展示待提交文件，并根据用户选择暂存、提交和推送。

## 安装与运行

需要 Python 3.9+ 和 Git：

```bash
git clone https://github.com/LceAn/UploadToGithub.git
cd UploadToGithub
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python upload_to_github.py
```

脚本必须在准备提交的 Git 工作区内运行。若把脚本复制到其他仓库，首次运行会将脚本名、`.env`、日志和常见 Python 缓存补入该仓库的 `.gitignore`。

## 提交模式

| 模式 | Git 行为 | 删除文件 |
| --- | --- | --- |
| 仅上传变更文件 | `git add --ignore-removal .` | 不暂存 |
| 上传全部文件 | `git add -A` | 暂存 |

提交信息通过参数数组传给 Git，不经过 Shell。脚本不会自动执行强制推送、重写历史或删除远端分支。没有暂存内容时会停止，不创建空提交。

## 安全边界

- `.gitignore` 只能阻止尚未跟踪的文件；已经被 Git 跟踪的敏感文件不会因此自动消失。
- 提交前仍应检查状态表和 `git diff --cached`，确认 Cookie、Token、私钥、数据库和本地配置没有进入暂存区。
- HTTPS 远端 URL 在状态表中会移除内嵌用户名和凭据。
- 推送使用当前仓库已经配置的上游，不创建或改写远端配置。

## 本地验证

```bash
python -m compileall -q upload_to_github.py tests
python -m unittest discover -s tests -v
```

测试覆盖命令参数隔离、提交信息、两种暂存模式、版本比较和远端凭据脱敏。测试不会执行真实提交或推送。

## 文件

- `upload_to_github.py`：交互入口与 Git 操作
- `tests/`：无网络单元测试
- `UPDATE_SUMMARY.md`：v2.0.0 历史更新记录

## 许可

[MIT](LICENSE)

<!-- repo-readme-standard:v1 -->
## 仓库维护信息

- 项目类型：Git 命令行工具
- 当前状态：维护中
- 可见性：public
- 维护节奏：按月检查 Git 行为、凭据显示和依赖版本
- 相关仓库：未发现功能相同、可直接合并的仓库
- 维护边界：归档、删除、历史重写或强制推送需单独确认
