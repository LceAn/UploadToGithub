# UploadToGithub - Git 自动化上传工具

> 🚀 一键完成 Git 添加、提交、推送操作 | 智能检查 | 版本检测 | 自动排除

[![Version](https://img.shields.io/badge/version-v2.0.0-blue.svg)](https://github.com/LceAn/UploadToGithub/releases)
[![Python](https://img.shields.io/badge/python-3.6+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/LceAn/UploadToGithub/blob/main/LICENSE)

---

## 📖 简介

`upload_to_github.py` 是一个功能强大的 Git 自动化上传工具，帮助你快速完成代码的添加、提交和推送操作。具备智能检查、版本检测、文件排除等功能，让 Git 操作更高效、更安全。

**适用场景：**
- ✅ 频繁提交代码的开发者
- ✅ 需要批量上传项目的团队
- ✅ 想要简化 Git 流程的初学者
- ✅ 需要标准化提交流程的项目

---

## ✨ 功能特性

### 🎯 核心功能

| 功能 | 说明 |
|------|------|
| **智能检查** | 自动检查 Git 安装、配置、仓库状态、远程仓库 |
| **版本检测** | 自动检测 GitHub 最新版本，提示更新 |
| **文件排除** | 自动排除脚本自身、缓存文件、敏感文件等 |
| **状态展示** | 美观的表格展示仓库状态、暂存区、工作区变更 |
| **双模式上传** | 支持仅上传变更 / 上传全部（包括删除） |
| **错误处理** | 完善的异常捕获和友好的错误提示 |

### 🆕 v2.0.0 新增

- 🎨 全新 UI 界面，更清晰的视觉展示
- 🔧 代码重构，采用面向对象设计
- 📦 支持更多排除文件类型（.pyc, __pycache__, .env, *.log）
- ⚡ 优化命令执行，增加超时保护
- 📊 增强状态展示，区分暂存区/工作区/未跟踪文件
- 🛡️ 更完善的前置检查和错误处理

---

## 🚀 快速开始

### 前置要求

1. **Python 3.6+**
2. **Git 已安装并配置**

### 安装依赖

```bash
pip install prettytable colorama requests
```

或使用 `requirements.txt`：

```bash
pip install -r requirements.txt
```

### 配置 Git

```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```

### 使用方法

#### 方式一：克隆仓库

```bash
git clone https://github.com/LceAn/UploadToGithub.git
cd UploadToGithub
python3 upload_to_github.py
```

#### 方式二：放入现有项目

```bash
# 将脚本复制到你的项目目录
cp upload_to_github.py /path/to/your/project/
cd /path/to/your/project/
python3 upload_to_github.py
```

---

## 📋 使用示例

### 基础使用

```bash
$ python3 upload_to_github.py

╔══════════════════════════════════════════════════════════╗
║  UploadToGithub - Git 自动化上传工具                     ║
║  Git 操作自动化脚本                                       ║
╠══════════════════════════════════════════════════════════╣
║  版本：v2.0.0                                            ║
║  作者：LceAn                                             ║
║  更新：2026-03-06 09:57:00                               ║
╚══════════════════════════════════════════════════════════╝

[ + ] Git 已安装：git version 2.39.3
[ + ] Git 已配置：Your Name <youremail@example.com>
[ + ] 当前目录是 Git 仓库
[ + ] 远程仓库已配置
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Git 仓库信息汇总
+-----------------+----------------------------------+
| 项              | 状态                             |
+-----------------+----------------------------------+
| Git 版本        | git version 2.39.3               |
| 当前分支        | main                             |
| 远程仓库        | https://github.com/LceAn/...     |
| 暂存区文件      | README.md                        |
| 工作区变更      | upload_to_github.py              |
| Git 用户        | Your Name <youremail@example.com>|
+-----------------+----------------------------------+

请选择上传类型：
  1 - 仅上传变更文件（推荐）
  2 - 上传全部文件（包括删除的文件）

输入选项 (1/2) [默认:1]: 1

请输入提交信息（输入 q 退出）：
> 优化了脚本结构和 UI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ℹ ] 正在添加变更文件...
[ ℹ ] 正在提交：优化了脚本结构和 UI
[ ✔ ] 提交成功
[ ℹ ] 正在推送到远程仓库...
[ ✔ ] 推送成功
[ ℹ ] 最近提交：abc1234 优化了脚本结构和 UI
[ ✔ ] 本次提交包含 2 个文件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 所有操作完成！
```

### 高级用法

#### 自动排除文件

脚本会自动创建/更新 `.gitignore`，排除以下文件：

```
upload_to_github.py
.DS_Store
*.pyc
__pycache__
.env
*.log
```

#### 版本检查

每次启动自动检查 GitHub 最新版本：

```
[ ! ] 发现新版本：v2.1.0，当前版本：v2.0.0
[ ℹ ] 请及时更新：git pull origin main
```

---

## ⚙️ 配置说明

### 自定义排除文件

编辑脚本中的 `Config.EXCLUDE_FILES`：

```python
class Config:
    # 排除文件列表
    EXCLUDE_FILES = [
        'upload_to_github.py',  # 脚本自身
        '.DS_Store',            # macOS 系统文件
        '*.pyc',                # Python 缓存
        '__pycache__',          # Python 缓存目录
        '.env',                 # 环境变量文件
        '*.log'                 # 日志文件
    ]
```

### 修改仓库信息

```python
class Config:
    REPO_OWNER = 'LceAn'
    REPO_NAME = 'UploadToGithub'
    AUTHOR = 'Your Name'
```

---

## 🔧 常见问题

### 1. Git 未配置用户名或邮箱

```bash
[ - ] Git 未配置用户名或邮箱，请先配置后再运行脚本。
[ ℹ ] git config --global user.name "Your Name"
[ ℹ ] git config --global user.email "youremail@example.com"
```

**解决：** 按提示运行配置命令即可。

### 2. 当前目录不是 Git 仓库

```bash
[ - ] 当前目录不是 Git 仓库
[ ℹ ] git init  # 初始化仓库
[ ℹ ] git clone <url>  # 克隆仓库
```

**解决：** 初始化或克隆仓库。

### 3. 未配置远程仓库

```bash
[ - ] 未配置远程仓库
[ ℹ ] git remote add origin https://github.com/user/repo.git
```

**解决：** 添加远程仓库地址。

### 4. 推送失败

```bash
[ - ] 推送失败：Permission denied (publickey)
```

**解决：** 检查 SSH 密钥或改用 HTTPS 方式。

---

## 📦 依赖说明

| 依赖 | 版本 | 用途 |
|------|------|------|
| `prettytable` | >=2.0 | 表格展示 |
| `colorama` | >=0.4 | 跨平台颜色支持 |
| `requests` | >=2.25 | HTTP 请求（版本检测） |

---

## 📝 版本历史

### v2.0.0 (2026-03-06) 🎉
- 🎨 全新 UI 设计，更清晰的视觉展示
- 🔧 代码重构，采用面向对象设计
- 📦 扩展排除文件列表
- ⚡ 增加命令执行超时保护
- 📊 增强状态展示功能
- 🛡️ 完善错误处理机制

### v1.2.0
- 修订推送时排除脚本自身

### v1.1.0
- 新增 ASCII 字符动画
- 版本检测功能
- 输出格式统一

### v1.0.0
- 初始版本
- 基本 Git 自动化操作
- 异常处理功能

---

## 🤝 贡献

欢迎提交 Issue 或 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)

---

## 📬 联系方式

- **作者：** LceAn
- **仓库：** https://github.com/LceAn/UploadToGithub
- **问题反馈：** https://github.com/LceAn/UploadToGithub/issues

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by LceAn

</div>
