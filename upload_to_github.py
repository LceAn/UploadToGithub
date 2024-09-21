import subprocess
import texttable as tt  # 引入 texttable 库来生成表格（需要：pip install texttable）


def run_command(command):
    """运行一个命令并返回其输出。"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None


def format_status_output(status_output):
    """格式化 git status 的输出信息为表格样式。"""
    table = tt.Texttable()
    table.set_deco(tt.Texttable.HEADER)
    table.set_cols_align(["l", "l"])
    table.set_cols_valign(["m", "m"])
    table.set_cols_width([25, 60])
    table.header(["状态", "文件/目录"])

    status_section = None
    for line in status_output.splitlines():
        line = line.strip()
        if line.startswith("Changes to be committed:"):
            status_section = "暂存区的更改"
        elif line.startswith("Changes not staged for commit:"):
            status_section = "未暂存的更改"
        elif line.startswith("Untracked files:"):
            status_section = "未跟踪的文件"
        elif line.startswith("(use "):
            continue  # 跳过提示信息
        elif status_section and line:
            if line.startswith("new file:") or line.startswith("modified:"):
                parts = line.split(":", 1)
                table.add_row([status_section, parts[1].strip()])
            else:
                table.add_row([status_section, line])

    return table.draw()


def check_git_status(full_status=True):
    """检查当前Git仓库的状态信息。"""
    # 检查Git版本
    git_version, _ = run_command("git --version")
    print(f"Git 版本: {git_version}")

    # 检查当前的Git状态
    git_status, _ = run_command("git status")
    print("\n当前Git状态:")
    if full_status:
        print(format_status_output(git_status))

    # 检查当前用户的配置信息
    user_name, _ = run_command("git config user.name")
    user_email, _ = run_command("git config user.email")
    print(f"\n当前Git用户名: {user_name}")
    print(f"当前Git用户邮箱: {user_email}")

    # 检查当前暂存区的内容
    staged_files, _ = run_command("git diff --cached --name-only")
    if staged_files:
        print("\n暂存区中的文件:")
        for file in staged_files.splitlines():
            print(f"- {file}")
    else:
        print("暂存区中没有文件。")

    # 检查远程仓库信息
    remote_info, _ = run_command("git remote -v")
    print("\n远程仓库信息:")
    print(remote_info)


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
    staged_files, _ = run_command("git diff --cached --name-only")
    if staged_files:
        print("\n已提交的文件:")
        for file in staged_files.splitlines():
            print(f"- {file}")
    else:
        print("暂存区中没有文件。")

    # 推送更改
    print("\n正在推送更改到远程仓库...")
    push_result, push_error = run_command("git push")
    if push_error:
        print(f"\n推送失败：{push_error}")
        print("\n请检查错误信息，确保远程仓库配置正确。")
    else:
        print("\n推送成功！详细信息如下：")
        print(push_result)


if __name__ == "__main__":
    # 先检查当前Git状态（全量显示）
    check_git_status(full_status=True)

    # 提交更改
    commit_message = input("\n请输入提交信息：")

    # 检查当前暂存区状态（仅显示暂存文件）
    check_git_status(full_status=False)

    # 提交并推送更改
    git_update(commit_message)