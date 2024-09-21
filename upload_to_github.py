import subprocess
import texttable as tt  # 引入 texttable 库来生成表格（需要：pip install texttable）


def run_command(command):
    """运行一个命令并返回其输出。"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None


def get_git_info():
    """获取并返回所有 Git 信息，组成一个大的表格。"""
    table = tt.Texttable()
    table.set_deco(tt.Texttable.HEADER | tt.Texttable.VLINES | tt.Texttable.HLINES)
    table.set_chars(['-', '|', '+', '='])  # 设置边框样式
    table.set_cols_align(["l", "l"])
    table.set_cols_valign(["m", "m"])
    table.set_cols_width([25, 75])
    table.header(["项", "状态"])

    # Git 版本
    git_version, _ = run_command("git --version")
    table.add_row(["Git 版本", git_version])

    # Git 状态信息
    git_status, _ = run_command("git status")
    status_lines = git_status.splitlines()
    current_section = None
    for line in status_lines:
        line = line.strip()
        if line.startswith("On branch"):
            current_section = "当前分支"
            table.add_row([current_section, line])
        elif line.startswith("Your branch"):
            current_section = "分支状态"
            table.add_row([current_section, line])
        elif line.startswith("Changes to be committed:"):
            current_section = "暂存区的更改"
        elif line.startswith("Changes not staged for commit:"):
            current_section = "未暂存的更改"
        elif line.startswith("Untracked files:"):
            current_section = "未跟踪的文件"
        elif line.startswith("(use "):
            continue
        elif line and current_section:
            table.add_row([current_section, line])

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
    table.add_row(["远程仓库信息", remote_info])

    return table.draw()


def check_staged_files():
    """只检查暂存区文件并显示。"""
    staged_files, _ = run_command("git diff --cached --name-only")
    if staged_files:
        print("\n暂存区中的文件:")
        for file in staged_files.splitlines():
            print(f"- {file}")
    else:
        print("暂存区中没有文件。")


def git_update(commit_message):
    """添加、提交并推送更改到GitHub仓库。"""
    # 添加所有更改
    print("\n正在添加所有更改...")
    run_command("git add .")

    # 提交更改
    print(f"\n正在提交更改，提交信息：{commit_message}")
    commit_result, commit_error = run_command(f"git commit -m \"{commit_message}\"")
    if commit_error:
        print(f"\n提交失败：{commit_error}")
        return

    # 显示提交后的暂存区状态
    print("\n提交后的暂存区文件:")
    check_staged_files()

    # 推送更改
    print("\n正在推送更改到远程仓库...")
    push_result, push_error = run_command("git push")
    if push_error:
        print(f"\n推送失败：{push_error}")
        print("\n请检查错误信息，确保远程仓库配置正确。")
    elif push_result:
        print("\n推送成功！详细信息如下：")
        print(push_result)
    else:
        print("\n推送成功！但没有返回任何详细信息。")


if __name__ == "__main__":
    # 打印所有Git信息
    git_info = get_git_info()
    print(git_info)

    # 提交更改
    commit_message = input("\n请输入提交信息：")

    # 只显示暂存区文件状态（避免重复输出所有状态信息）
    check_staged_files()

    # 提交并推送更改
    git_update(commit_message)