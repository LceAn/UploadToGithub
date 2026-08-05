import subprocess
import unittest
from unittest.mock import patch

import upload_to_github as upload


class CommandTests(unittest.TestCase):
    @patch("upload_to_github.subprocess.run")
    def test_run_command_passes_arguments_without_a_shell(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout="ok\n", stderr="")

        output, error = upload.run_command(["git", "commit", "-m", 'message"; touch unsafe'])

        self.assertEqual((output, error), ("ok", None))
        run.assert_called_once_with(
            ["git", "commit", "-m", 'message"; touch unsafe'],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    @patch("upload_to_github.run_command")
    def test_commit_message_remains_one_argument(self, run):
        run.return_value = ("", None)

        self.assertTrue(upload.git_commit('fix: quote "message"; no shell'))

        run.assert_called_once_with(["git", "commit", "-m", 'fix: quote "message"; no shell'])

    @patch("upload_to_github.run_command")
    def test_add_modes_have_different_deletion_behavior(self, run):
        run.return_value = ("", None)

        upload.git_add(upload_all=False)
        upload.git_add(upload_all=True)

        self.assertEqual(
            run.call_args_list[0].args[0],
            ["git", "add", "--ignore-removal", "."],
        )
        self.assertEqual(run.call_args_list[1].args[0], ["git", "add", "-A"])


class HelperTests(unittest.TestCase):
    def test_semantic_version_comparison(self):
        self.assertTrue(upload.is_newer_version("v2.10.0", "v2.9.9"))
        self.assertFalse(upload.is_newer_version("v2.0.0", "v2.0.0"))
        self.assertFalse(upload.is_newer_version("v2.0.0", "v2.0"))

    def test_remote_credentials_are_redacted(self):
        remote = "https://user:token@github.com/example/project.git"
        self.assertEqual(
            upload.sanitize_remote_url(remote),
            "https://github.com/example/project.git",
        )


if __name__ == "__main__":
    unittest.main()
