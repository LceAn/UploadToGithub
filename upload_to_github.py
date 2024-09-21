import subprocess


def run_command(command):
    """运行一个命令并返回其输出。"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"执行命令出错：{command}")
        print(result.stderr)
        return None
    return result.stdout


def check_git_status():
    """检查当前Git仓库的状态信息。"""
    # 检查Git版本
    git_version = run_command("git --version")
    print(f"Git 版本: {git_version.strip()}")

    # 检查当前的Git状态
    git_status = run_command("git status")
    print("当前Git状态:")
    print(git_status)

    # 检查当前用户的配置信息
    user_name = run_command("git config user.name")
    user_email = run_command("git config user.email")
    print(f"当前Git用户名: {user_name.strip()}")
    print(f"当前Git用户邮箱: {user_email.strip()}")

    # 检查当前暂存区的内容
    staged_files = run_command("git diff --cached --name-only")
    if staged_files:
        print("暂存区中的文件:")
        print(staged_files)
    else:
        print("暂存区中没有文件。")

    # 检查远程仓库信息
    remote_info = run_command("git remote -v")
    print("远程仓库信息:")
    print(remote_info)


def git_update(commit_message):
    """添加、提交并推送更改到GitHub仓库。"""
    # 检查Git状态
    check_git_status()

    # Git 添加所有更改
    print("正在添加所有更改...")
    run_command("git add .")

    # Git 提交
    print(f"正在提交更改，提交信息：{commit_message}")
    run_command(f"git commit -m \"{commit_message}\"")

    # Git 推送
    print("正在推送更改到远程仓库...")
    push_result = run_command("git push")
    if push_result is None:  # 如果推送失败，可能没有上游分支
        print("推送失败，正在设置上游分支并重试...")
        run_command("git push --set-upstream origin main")


if __name__ == "__main__":
    # 先检查当前Git状态
    check_git_status()

    # 提交更改
    commit_message = input("请输入提交信息：")
    git_update(commit_message)