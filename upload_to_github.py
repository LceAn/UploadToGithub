import subprocess
import texttable as tt  # 引入 texttable 库来生成表格（你需要安装它：pip install texttable）


def run_command(command):
    """运行一个命令并返回其输出。"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"执行命令出错：{command}")
        print(result.stderr)
        return None
    return result.stdout


def format_status_output(status_output):
    """格式化 git status 的输出信息为表格样式。"""
    table = tt.Texttable()
    table.set_cols_align(["l", "l"])
    table.set_cols_valign(["m", "m"])
    table.set_cols_width([20, 60])
    table.header(["状态", "文件/目录"])

    for line in status_output.splitlines():
        if line.startswith("new file:") or line.startswith("modified:"):
            parts = line.split(":", 1)
            table.add_row([parts[0].strip(), parts[1].strip()])

    return table.draw()


def check_git_status():
    """检查当前Git仓库的状态信息。"""
    # 检查Git版本
    git_version = run_command("git --version")
    print(f"\nGit 版本: {git_version.strip()}")

    # 检查当前的Git状态
    git_status = run_command("git status")
    print("\n当前Git状态:")
    print(format_status_output(git_status))

    # 检查当前用户的配置信息
    user_name = run_command("git config user.name")
    user_email = run_command("git config user.email")
    print(f"\n当前Git用户名: {user_name.strip()}")
    print(f"当前Git用户邮箱: {user_email.strip()}")

    # 检查当前暂存区的内容
    staged_files = run_command("git diff --cached --name-only")
    if staged_files:
        print("\n暂存区中的文件:")
        for file in staged_files.splitlines():
            print(f"- {file}")
    else:
        print("暂存区中没有文件。")

    # 检查远程仓库信息
    remote_info = run_command("git remote -v")
    print("\n远程仓库信息:")
    print(remote_info)


def git_update(commit_message):
    """添加、提交并推送更改到GitHub仓库。"""
    # 检查Git状态
    check_git_status()

    # Git 添加所有更改
    print("\n正在添加所有更改...")
    run_command("git add .")

    # Git 提交
    print(f"\n正在提交更改，提交信息：{commit_message}")
    run_command(f"git commit -m \"{commit_message}\"")

    # Git 推送
    print("\n正在推送更改到远程仓库...")
    push_result = run_command("git push")
    if push_result is None:  # 如果推送失败，可能没有上游分支
        print("\n推送失败，正在设置上游分支并重试...")
        push_result = run_command("git push --set-upstream origin main")

    # 推送完成后的回执信息
    if push_result:
        print("\n推送成功！详细信息如下：")
        print(push_result)
    else:
        print("\n推送失败，请检查错误信息。")


if __name__ == "__main__":
    # 先检查当前Git状态
    check_git_status()

    # 提交更改
    commit_message = input("\n请输入提交信息：")
    git_update(commit_message)