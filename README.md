# Upload to GitHub Script

## 简介

`upload_to_github.py` 是一个用于自动化 Git 操作的 Python 脚本。它可以帮助用户在本地 Git 仓库中快速地添加、提交、并推送更改到远程 GitHub 仓库。同时，脚本具备一些基本的异常处理功能，如检查 Git 登录状态、检查仓库配置等，确保在操作之前用户环境正确。

## 功能特性

- **Git 仓库信息汇总**：通过表格显示当前仓库的状态，包括分支状态、暂存区状态、远程仓库信息等。
- **Git 登录状态检查**：在执行操作前自动检查是否已配置 Git 用户名和邮箱，确保 Git 操作正常。
- **仓库状态检查**：自动检测当前目录是否为 Git 仓库，如果不是则提示用户并退出脚本。
- **远程仓库配置检查**：检查是否配置了远程仓库，如果没有配置远程仓库，脚本将退出并提示用户。
- **自动化 Git 操作**：可以自动添加、提交并推送更改到远程仓库，帮助用户简化 Git 操作流程。
- **用户友好的退出功能**：在输入提交信息时，用户可以输入 `q` 来退出脚本，方便用户中断操作。

## 使用方法

### 前提条件

1. **安装 Python**：确保本地已安装 Python 3.x 版本。
2. **安装依赖**：运行以下命令安装 `prettytable` 库：
   ```bash
   pip install prettytable
   ```
3. **Git 环境配置**：确保本地 Git 已正确配置用户名和邮箱。如果没有配置，可以运行以下命令：
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "youremail@example.com"
   ```
4. **远程仓库配置**：确保本地仓库已配置远程仓库。可以运行以下命令进行检查：
   ```bash
   git remote -v
   ```
   如果没有远程仓库配置，可以通过以下命令添加：
   ```bash
   git remote add origin https://github.com/user/repo.git
   ```

### 使用步骤

1. **克隆或进入本地 Git 仓库**：
   ```bash
   git clone https://github.com/user/repo.git
   cd repo
   ```
   
2. **运行脚本**：
   ```bash
   python3 upload_to_github.py
   ```
   
3. **输入提交信息**：
   - 根据提示输入提交信息，例如 "修复了登录页面的错误"。如果希望退出脚本，可以输入 `q`。

4. **查看输出结果**：
   - 脚本将显示当前仓库的状态，并进行添加、提交和推送操作。操作完成后，会提示推送结果。

### 示例

```bash
$ python3 upload_to_github.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
+----------------------------------------------------+
|                Git 仓库信息汇总                    |
+-----------------+----------------------------------+
| Git 版本        | git version 2.39.3 (Apple Git-146) |
| 当前状态        | On branch main                    |
|                 | Your branch is up to date with    |
|                 | 'origin/main'.                    |
| 暂存区中的文件  | upload_to_github.py               |
| 当前Git用户名   | Your Name                         |
| 当前Git用户邮箱 | youremail@example.com             |
| 远程仓库信息    | origin https://github.com/user/repo.git (fetch) |
|                 | origin https://github.com/user/repo.git (push)  |
+-----------------+----------------------------------+
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请输入提交信息（输入q退出）：修复了README文件中的拼写错误

--------------------------------------------------
暂存区中的文件：
  [✔] upload_to_github.py
--------------------------------------------------
[ℹ] 正在添加所有更改...
--------------------------------------------------
[ℹ] 正在提交更改，提交信息：修复了README文件中的拼写错误
--------------------------------------------------
提交后的暂存区文件：
  [✘] 暂存区中没有文件。
--------------------------------------------------
[ℹ] 正在推送更改到远程仓库...
[✔] 推送成功！详细信息如下：
...
--------------------------------------------------
```

## 错误处理

### 常见错误及解决方法

1. **未配置 Git 用户名和邮箱**：
   - 错误信息：`[✘] Git 未配置用户名或邮箱，请先配置后再运行脚本。`
   - 解决方法：运行以下命令配置 Git 用户名和邮箱：
     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "youremail@example.com"
     ```

2. **当前目录不是 Git 仓库**：
   - 错误信息：`[✘] 当前目录不是一个Git仓库，请先初始化仓库或切换到Git仓库目录后再运行脚本。`
   - 解决方法：确保当前目录为 Git 仓库，可以使用以下命令初始化 Git 仓库：
     ```bash
     git init
     ```

3. **未配置远程仓库**：
   - 错误信息：`[✘] 当前Git仓库没有配置远程仓库，请先添加远程仓库再运行脚本。`
   - 解决方法：添加远程仓库：
     ```bash
     git remote add origin https://github.com/user/repo.git
     ```

## 版本历史

- **v1.0.0**
  - 初始版本，包含基本的 Git 自动化操作功能、异常处理和用户友好的退出功能。

## 贡献

如果你发现了Bug或者有新的功能需求，欢迎提交 [Issue](https://github.com/user/repo/issues) 或者发送 [Pull Request](https://github.com/user/repo/pulls)。

## 许可

本项目遵循 [MIT 许可证](https://opensource.org/licenses/MIT)。

