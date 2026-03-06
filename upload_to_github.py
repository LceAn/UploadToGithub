# -*- coding: utf-8 -*-
# @Time : 2024/9/23 下午 4:52
# @Author : LceAn
# @File : upload_to_github.py
# @Software : PyCharm
# @Version: v2.0.0

"""
UploadToGithub - Git 自动化上传工具
功能：自动化 Git 添加、提交、推送操作，具备状态检查、版本检测、智能排除等功能
"""

import os
import sys
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List
from prettytable import PrettyTable
from colorama import Fore, Style, init

# ============================================================================
# 初始化配置
# ============================================================================

# 初始化 colorama（跨平台颜色支持）
init(autoreset=True)


class Config:
    """全局配置类"""
    
    # 颜色定义
    YELLOW = Fore.YELLOW
    WHITE = Fore.WHITE
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    RED = Fore.RED
    CYAN = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL
    
    # 版本信息
    LOCAL_VERSION = 'v2.0.0'
    REPO_OWNER = 'LceAn'
    REPO_NAME = 'UploadToGithub'
    REPO_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    
    # 脚本元数据
    SCRIPT_NAME = 'upload_to_github.py'
    AUTHOR = 'LceAn'
    DESCRIPTION = 'Git 操作自动化脚本'
    
    # 排除文件列表（不会上传到 Git）
    EXCLUDE_FILES = [
        'upload_to_github.py',
        '.DS_Store',
        '*.pyc',
        '__pycache__',
        '.env',
        '*.log'
    ]


class Colors:
    """颜色工具类"""
    
    @staticmethod
    def info(text: str) -> str:
        return f"{Fore.GREEN}[ + ] {text}{Style.RESET_ALL}"
    
    @staticmethod
    def warning(text: str) -> str:
        return f"{Fore.YELLOW}[ ! ] {text}{Style.RESET_ALL}"
    
    @staticmethod
    def error(text: str) -> str:
        return f"{Fore.RED}[ - ] {text}{Style.RESET_ALL}"
    
    @staticmethod
    def success(text: str) -> str:
        return f"{Fore.GREEN}[ ✔ ] {text}{Style.RESET_ALL}"
    
    @staticmethod
    def info_msg(text: str) -> str:
        return f"{Fore.CYAN}[ ℹ ] {text}{Style.RESET_ALL}"


# ============================================================================
# 工具函数
# ============================================================================

def print_banner():
    """打印启动横幅"""
    banner = f"""
{Config.WHITE}╔══════════════════════════════════════════════════════════╗
║{Config.CYAN}  UploadToGithub - Git 自动化上传工具{Config.WHITE}                          ║
║{Config.GREEN}  {Config.DESCRIPTION}{Config.WHITE}                                          ║
╠══════════════════════════════════════════════════════════╣
║  版本：{Config.RED}{Config.LOCAL_VERSION}{Config.WHITE}                                      ║
║  作者：{Config.MAGENTA}{Config.AUTHOR}{Config.WHITE}                                        ║
║  更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Config.WHITE}                          ║
╚══════════════════════════════════════════════════════════╝
{Config.RESET}"""
    print(banner)


def print_divider(symbol: str = "━", length: int = 60) -> None:
    """打印分隔线"""
    print(symbol * length)


def run_command(command: str, capture: bool = True) -> Tuple[Optional[str], Optional[str]]:
    """
    运行 shell 命令
    
    Args:
        command: 要执行的命令
        capture: 是否捕获输出
        
    Returns:
        (stdout, stderr) 元组
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            return None, result.stderr.strip()
        return result.stdout.strip(), None
    except subprocess.TimeoutExpired:
        return None, f"命令执行超时：{command}"
    except Exception as e:
        return None, str(e)


# ============================================================================
# 检查函数
# ============================================================================

def check_git_installed() -> bool:
    """检查 Git 是否已安装"""
    git_version, error = run_command("git --version")
    if error:
        print(Colors.error("Git 未安装，请先安装 Git"))
        print(Colors.info_msg("macOS: brew install git"))
        print(Colors.info_msg("Windows: https://git-scm.com/download/win"))
        return False
    print(Colors.success(f"Git 已安装：{git_version}"))
    return True


def check_git_config() -> bool:
    """检查 Git 用户配置"""
    user_name, _ = run_command("git config user.name")
    user_email, _ = run_command("git config user.email")
    
    if not user_name or not user_email:
        print(Colors.error("Git 未配置用户名或邮箱"))
        print(Colors.info_msg("git config --global user.name \"Your Name\""))
        print(Colors.info_msg("git config --global user.email \"youremail@example.com\""))
        return False
    
    print(Colors.success(f"Git 已配置：{user_name} <{user_email}>"))
    return True


def check_git_repository() -> bool:
    """检查当前目录是否是 Git 仓库"""
    git_dir, error = run_command("git rev-parse --is-inside-work-tree")
    if error:
        print(Colors.error("当前目录不是 Git 仓库"))
        print(Colors.info_msg("git init  # 初始化仓库"))
        print(Colors.info_msg("git clone <url>  # 克隆仓库"))
        return False
    print(Colors.success("当前目录是 Git 仓库"))
    return True


def check_remote_repository() -> bool:
    """检查远程仓库配置"""
    remotes, error = run_command("git remote -v")
    if not remotes:
        print(Colors.error("未配置远程仓库"))
        print(Colors.info_msg("git remote add origin https://github.com/user/repo.git"))
        return False
    
    print(Colors.success("远程仓库已配置"))
    return True


def check_for_updates() -> None:
    """检查新版本"""
    try:
        response = requests.get(Config.REPO_API_URL, timeout=5)
        if response.status_code == 200:
            latest_version = response.json().get("tag_name", "")
            if latest_version and Config.LOCAL_VERSION < latest_version:
                print(Colors.warning(f"发现新版本：{latest_version}，当前版本：{Config.LOCAL_VERSION}"))
                print(Colors.info_msg("请及时更新：git pull origin main"))
            else:
                print(Colors.success("当前已是最新版本"))
        else:
            print(Colors.warning("无法获取版本信息"))
    except requests.exceptions.RequestException as e:
        print(Colors.warning(f"检查更新失败：{e}"))


# ============================================================================
# Git 信息展示
# ============================================================================

def get_git_info_table() -> PrettyTable:
    """获取 Git 仓库信息表格"""
    table = PrettyTable()
    table.title = "📊 Git 仓库信息汇总"
    table.field_names = ["项", "状态"]
    table.align = "l"
    table.max_width = 60
    
    # Git 版本
    git_version, _ = run_command("git --version")
    table.add_row(["Git 版本", git_version])
    
    # 当前分支
    branch, _ = run_command("git branch --show-current")
    table.add_row(["当前分支", branch])
    
    # 远程仓库
    remote_url, _ = run_command("git remote get-url origin")
    if remote_url:
        table.add_row(["远程仓库", remote_url])
    
    # 暂存区文件
    staged_files, _ = run_command("git diff --cached --name-only")
    staged_list = staged_files.splitlines() if staged_files else []
    table.add_row(["暂存区文件", "\n".join(staged_list) if staged_list else "无"])
    
    # 工作区变更
    changed_files, _ = run_command("git diff --name-only")
    changed_list = changed_files.splitlines() if changed_files else []
    table.add_row(["工作区变更", "\n".join(changed_list) if changed_list else "无"])
    
    # 未跟踪文件
    untracked, _ = run_command("git ls-files --others --exclude-standard")
    untracked_list = untracked.splitlines() if untracked else []
    # 排除配置中的文件
    untracked_list = [f for f in untracked_list if f not in Config.EXCLUDE_FILES]
    table.add_row(["未跟踪文件", "\n".join(untracked_list[:5]) + ("\n..." if len(untracked_list) > 5 else "") if untracked_list else "无"])
    
    # 用户信息
    user_name, _ = run_command("git config user.name")
    user_email, _ = run_command("git config user.email")
    table.add_row(["Git 用户", f"{user_name} <{user_email}>"])
    
    return table


def show_file_status(files: List[str], status: str = "staged") -> None:
    """显示文件状态"""
    print_divider("-", 50)
    if status == "staged":
        print("📦 暂存区文件：")
    elif status == "changed":
        print("📝 工作区变更：")
    else:
        print("📄 未跟踪文件：")
    
    if files:
        for file in files[:10]:  # 最多显示 10 个
            print(f"  {Colors.success(file)}")
        if len(files) > 10:
            print(f"  ... 还有 {len(files) - 10} 个文件")
    else:
        print(f"  {Colors.warning('无')}")


# ============================================================================
# Git 操作
# ============================================================================

def update_gitignore() -> None:
    """更新 .gitignore 文件，排除配置的文件"""
    gitignore_path = Path(".gitignore")
    
    # 读取现有内容
    existing_content = []
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            existing_content = [line.strip() for line in f.readlines()]
    
    # 添加需要排除的文件
    new_entries = [f for f in Config.EXCLUDE_FILES if f not in existing_content]
    
    if new_entries:
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write("\n# Auto-generated by UploadToGithub\n")
            for entry in new_entries:
                f.write(f"{entry}\n")
        print(Colors.success(f"已更新 .gitignore，添加 {len(new_entries)} 个排除项"))
    else:
        print(Colors.info_msg(".gitignore 已是最新"))


def git_add(upload_all: bool = False) -> bool:
    """添加文件到暂存区"""
    if upload_all:
        print(Colors.info_msg("正在添加所有文件（包括删除）..."))
        _, error = run_command("git add -A")
    else:
        print(Colors.info_msg("正在添加变更文件..."))
        _, error = run_command("git add .")
    
    if error:
        print(Colors.error(f"添加失败：{error}"))
        return False
    return True


def git_commit(message: str) -> bool:
    """提交更改"""
    if not message.strip():
        print(Colors.error("提交信息不能为空"))
        return False
    
    print(Colors.info_msg(f"正在提交：{message}"))
    _, error = run_command(f'git commit -m "{message}"')
    
    if error:
        print(Colors.error(f"提交失败：{error}"))
        return False
    
    print(Colors.success("提交成功"))
    return True


def git_push() -> bool:
    """推送到远程仓库"""
    print(Colors.info_msg("正在推送到远程仓库..."))
    output, error = run_command("git push")
    
    if error:
        print(Colors.error(f"推送失败：{error}"))
        return False
    
    if output:
        print(Colors.success("推送成功"))
        # 显示最近提交
        commit_info, _ = run_command("git log -1 --oneline")
        if commit_info:
            print(Colors.info_msg(f"最近提交：{commit_info}"))
    return True


def git_upload(commit_message: str, upload_all: bool = False) -> bool:
    """完整的上传流程"""
    # 更新 .gitignore
    update_gitignore()
    
    # 添加文件
    if not git_add(upload_all):
        return False
    
    # 显示暂存区状态
    staged_files, _ = run_command("git diff --cached --name-only")
    staged_list = staged_files.splitlines() if staged_files else []
    show_file_status(staged_list, "staged")
    
    # 提交
    if not git_commit(commit_message):
        return False
    
    # 推送
    if not git_push():
        return False
    
    # 显示统计
    files_count = len(staged_list)
    print(Colors.success(f"本次提交包含 {files_count} 个文件"))
    
    return True


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    try:
        # 打印横幅
        print_banner()
        
        # 检查更新
        check_for_updates()
        print_divider()
        
        # 前置检查
        print(Colors.info_msg("进行前置检查..."))
        checks = [
            check_git_installed(),
            check_git_config(),
            check_git_repository(),
            check_remote_repository()
        ]
        
        if not all(checks):
            print(Colors.error("前置检查失败，请修复后重试"))
            sys.exit(1)
        
        print_divider()
        
        # 显示 Git 信息
        git_table = get_git_info_table()
        print(git_table)
        print_divider()
        
        # 选择上传类型
        print("\n请选择上传类型：")
        print("  1 - 仅上传变更文件（推荐）")
        print("  2 - 上传全部文件（包括删除的文件）")
        
        choice = input("\n输入选项 (1/2) [默认:1]: ").strip()
        upload_all = (choice == '2')
        
        # 获取提交信息
        print("\n请输入提交信息（输入 q 退出）：")
        commit_message = input("> ").strip()
        
        if commit_message.lower() == 'q':
            print(Colors.info_msg("已退出"))
            sys.exit(0)
        
        if not commit_message:
            print(Colors.error("提交信息不能为空"))
            sys.exit(1)
        
        # 执行上传
        print_divider()
        if git_upload(commit_message, upload_all):
            print_divider()
            print(Colors.success("🎉 所有操作完成！"))
        else:
            print_divider()
            print(Colors.error("❌ 操作失败，请检查错误信息"))
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n" + Colors.warning("用户中断操作"))
        sys.exit(0)
    except Exception as e:
        print(Colors.error(f"发生严重错误：{e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
