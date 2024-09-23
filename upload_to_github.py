import subprocess
from prettytable import PrettyTable


def run_command(command):
    """运行一个命令并返回其输出。"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None


def get_git_info():
    """获取并返回所有 Git 信息，组成一个大的表格。"""
    table = PrettyTable()
    table.title = "Git 仓库信息汇总"
    table.field_names = ["项", "状态"]
    table.align["项"] = "l"  # 左对齐
    table.align["状态"] = "l"  # 左对齐
    table.max_width = 60  # 设置列的最大宽度，适当减少列宽避免过长内容
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
    git_info_table = get_git_info()
    print(git_info_table)

    # 提交更改
    commit_message = input("\n请输入提交信息：")

    # 只显示暂存区文件状态（避免重复输出所有状态信息）
    check_staged_files()

    # 提交并推送更改
    git_update(commit_message)