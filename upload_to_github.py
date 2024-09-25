# -*- coding: utf-8 -*-
# @Time : 2024/9/23 下午4:52
# @Author : LceAn
# @File : upload_to_github.py
# @Software : PyCharm

import subprocess
import requests
from prettytable import PrettyTable
from colorama import Fore, Style, init

# 初始化 colorama（只在 Windows 上需要）
init(autoreset=True)


class Config:
    # 颜色和版本信息（使用 colorama 提供的颜色定义）
    yellow = Fore.YELLOW
    white = Fore.WHITE
    green = Fore.GREEN
    blue = Fore.BLUE
    red = Fore.RED
    end = Style.RESET_ALL

    # 本地版本信息
    local_version = 'v1.0.0'
    version_info = f"{white}{{{red}{local_version} #dev{white}}}"
    repo_api_url = "https://api.github.com/repos/LceAn/UploadToGithub/releases/latest"

    @staticmethod
    def generate_titles(script_function, script_name, author):
        """生成标题信息"""
        return f"""
        功能：{script_function}
{Config.yellow}
 _   _       _                 _   _____        ____ _ _   _           _     
| | | |_ __ | | ___   __ _  __| | |_   _|__    / ___(_) |_| |__  _   _| |__  
| | | | '_ \| |/ _ \ / _` |/ _` |   | |/ _ \  | |  _| | __| '_ \| | | | '_ \ {Config.green}
| |_| | |_) | | (_) | (_| | (_| |   | | (_) | | |_| | | |_| | | | |_| | |_) |
 \___/| .__/|_|\___/ \__,_|\__,_|___|_|\___/___\____|_|\__|_| |_|\__,_|_.__/ {Config.white}
      |_|                      |_____|    |_____|                     By {Config.version_info}       

    作者：{author}
    脚本名称：{script_name}
    内部版本，请勿泄漏
    {Config.red}本脚本正在开发中，请在每次使用前更新！{Config.end}
    """

    @staticmethod
    def print_status(message, status_type='info'):
        """打印带颜色和状态的消息信息"""
        if status_type == 'info':
            prefix = '[ + ]'
            color = Config.green
        elif status_type == 'warning':
            prefix = '[ ! ]'
            color = Config.yellow
        elif status_type == 'error':
            prefix = '[ - ]'
            color = Config.red
        else:
            prefix = '[ * ]'
            color = Config.white

        print(f"{color}{prefix} {message}{Config.end}")

    @staticmethod
    def get_latest_version():
        """从GitHub获取最新版本号"""
        try:
            response = requests.get(Config.repo_api_url)
            if response.status_code == 200:
                latest_version = response.json()["tag_name"]
                return latest_version
            else:
                Config.print_status("无法从GitHub获取版本信息", "warning")
                return None
        except requests.exceptions.RequestException as e:
            Config.print_status(f"请求失败: {e}", "error")
            return None

    @staticmethod
    def check_for_updates():
        """检查是否有新版本"""
        latest_version = Config.get_latest_version()
        if latest_version:
            if Config.local_version < latest_version:
                Config.print_status(f"有新版本可用: {latest_version}，请及时更新！", "warning")
            else:
                Config.print_status("当前版本已是最新版本。", "info")


def run_command(command):
    """运行一个命令并返回其输出。"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None


def print_divider(symbol="━", length=60):
    """打印分隔线"""
    print(symbol * length)


def check_git_login():
    """检查Git是否登录，未登录则退出脚本"""
    user_name, error = run_command("git config user.name")
    user_email, error = run_command("git config user.email")
    if not user_name or not user_email:
        Config.print_status("Git 未配置用户名或邮箱，请先配置后再运行脚本。", "error")
        Config.print_status("示例：git config --global user.name \"Your Name\"", "error")
        Config.print_status("      git config --global user.email \"youremail@example.com\"", "error")
        exit(1)
    Config.print_status(f"Git 已登录：{user_name} <{user_email}>", "info")


def check_git_repository():
    """检查当前目录是否是Git仓库"""
    git_dir, error = run_command("git rev-parse --is-inside-work-tree")
    if error:
        Config.print_status("当前目录不是一个Git仓库，请先初始化仓库或切换到Git仓库目录后再运行脚本。", "error")
        exit(1)
    Config.print_status("当前目录是Git仓库。", "info")


def check_remote_repository():
    """检查是否存在远程仓库配置"""
    remotes, error = run_command("git remote -v")
    if not remotes:
        Config.print_status("当前Git仓库没有配置远程仓库，请先添加远程仓库再运行脚本。", "error")
        Config.print_status("示例：git remote add origin https://github.com/user/repo.git", "error")
        exit(1)
    Config.print_status("远程仓库配置检查通过。", "info")


def get_git_info():
    """获取并返回所有 Git 信息，组成一个大的表格。"""
    table = PrettyTable()
    table.title = "Git 仓库信息汇总"
    table.field_names = ["项", "状态"]
    table.align["项"] = "l"  # 左对齐
    table.align["状态"] = "l"  # 左对齐
    table.max_width = 60  # 设置列的最大宽度
    table.header = True

    # Git 版本
    git_version, _ = run_command("git --version")
    table.add_row(["Git 版本", git_version])

    # Git 状态信息
    git_status, _ = run_command("git status --short --branch")
    table.add_row(["当前状态", git_status])

    # 获取详细的状态信息
    git_detailed_status, _ = run_command("git status")
    current_section = None
    detailed_lines = git_detailed_status.splitlines()
    changes_to_commit = []
    changes_not_staged = []
    untracked_files = []

    for line in detailed_lines:
        line = line.strip()
        if line.startswith("Changes to be committed:"):
            current_section = "暂存区的更改"
        elif line.startswith("Changes not staged for commit:"):
            current_section = "未暂存的更改"
        elif line.startswith("Untracked files:"):
            current_section = "未跟踪的文件"
        elif line.startswith("(use "):
            continue
        elif current_section and line:
            if current_section == "暂存区的更改":
                changes_to_commit.append(line)
            elif current_section == "未暂存的更改":
                changes_not_staged.append(line)
            elif current_section == "未跟踪的文件":
                untracked_files.append(line)

    # 合并详细状态信息
    if changes_to_commit:
        table.add_row(["暂存区的更改", "\n".join(changes_to_commit)])
    if changes_not_staged:
        table.add_row(["未暂存的更改", "\n".join(changes_not_staged)])
    if untracked_files:
        table.add_row(["未跟踪的文件", "\n".join(untracked_files)])

    # 用户名和邮箱
    user_name, _ = run_command("git config user.name")
    user_email, _ = run_command("git config user.email")
    table.add_row(["当前Git用户名", user_name])
    table.add_row(["当前Git用户邮箱", user_email])

    # 检查当前暂存区的内容
    staged_files, _ = run_command("git diff --cached --name-only")
    staged_files = staged_files.splitlines() if staged_files else ["暂存区中没有文件。"]
    table.add_row(["暂存区中的文件", "\n".join(staged_files)])

    # 远程仓库信息
    remote_info, _ = run_command("git remote -v")
    formatted_remote_info = remote_info.replace('\t', ' ')
    table.add_row(["远程仓库信息", formatted_remote_info])

    return table


def check_staged_files():
    """只检查暂存区文件并显示。"""
    staged_files, _ = run_command("git diff --cached --name-only")
    print_divider("-", 40)
    print("暂存区中的文件：")
    if staged_files:
        for file in staged_files.splitlines():
            print(f"  [✔] {file}")
    else:
        print("  [✘] 暂存区中没有文件。")


def git_update(commit_message, upload_all):
    """添加、提交并推送更改到GitHub仓库。"""
    # 添加更改
    print_divider("-", 40)
    if upload_all:
        Config.print_status("正在添加所有文件（包括删除的文件）...", "info")
        run_command("git add -A")
    else:
        Config.print_status("正在添加变更文件...", "info")
        run_command("git add .")

    # 提交更改
    print_divider("-", 40)
    Config.print_status(f"正在提交更改，提交信息：{commit_message}", "info")
    commit_result, commit_error = run_command(f"git commit -m \"{commit_message}\"")
    if commit_error:
        Config.print_status(f"提交失败：{commit_error}", "error")
        return

    # 获取提交的文件数量
    committed_files, _ = run_command("git diff --cached --name-only")
    committed_files_list = committed_files.splitlines() if committed_files else []
    committed_files_count = len(committed_files_list)

    # 显示提交后的暂存区状态
    print_divider("-", 40)
    print("提交后的暂存区文件：")
    check_staged_files()

    # 推送更改
    print_divider("-", 40)
    Config.print_status("正在推送更改到远程仓库...", "info")
    push_result, push_error = run_command("git push")
    if push_error:
        Config.print_status(f"推送失败：{push_error}", "error")
        Config.print_status("请检查错误信息，确保远程仓库配置正确。", "error")
    elif push_result:
        Config.print_status("推送成功！详细信息如下：", "info")
        print(push_result)

        # 显示最近一次提交的详细信息
        latest_commit_info, _ = run_command("git log -1 --stat")
        if latest_commit_info:
            Config.print_status("最近一次提交的详细信息：", "info")
            print(latest_commit_info)
        else:
            Config.print_status("无法获取最近一次提交的详细信息。", "warning")

        Config.print_status(f"本次提交包含的文件数量：{committed_files_count} 个", "info")
    else:
        Config.print_status("推送成功！但没有返回任何详细信息。", "info")


if __name__ == "__main__":
    try:
        # 初始化占位符内容
        script_function = "Git 操作自动化脚本"
        script_name = "upload_to_github.py"
        author = "LceAn"

        # 打印脚本标题信息，传递三个参数
        print(Config.generate_titles(script_function, script_name, author))

        # 检查更新
        Config.check_for_updates()

        # 检查是否已登录Git
        check_git_login()

        # 检查是否在Git仓库中
        check_git_repository()

        # 检查是否存在远程仓库配置
        check_remote_repository()

        # 打印所有Git信息
        print_divider()
        git_info_table = get_git_info()
        print(git_info_table)
        print_divider()

        # 选择上传类型
        upload_choice = input("\n请选择上传类型（1：仅上传变更文件，2：上传全部文件，包括删除的文件）：")
        if upload_choice == '2':
            upload_all = True
        else:
            upload_all = False

        # 提交更改
        commit_message = input("\n请输入提交信息（输入q退出）：")
        if commit_message.lower() == 'q':
            Config.print_status("已退出脚本。", "info")
            exit(0)

        # 只显示暂存区文件状态（避免重复输出所有状态信息）
        check_staged_files()

        # 提交并推送更改
        git_update(commit_message, upload_all)
        print_divider()
    except Exception as e:
        Config.print_status(f"发生严重错误，程序终止: {e}", 'error')