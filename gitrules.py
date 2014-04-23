import os
import re
import subprocess
import logging

from gns import env
from gns import service


##### Private objects #####
_logger = logging.getLogger(__name__)


##### Public methods #####
def get_head_path():
    git_path = os.path.join(
        env.get_config(service.S_CORE, service.O_RULES_DIR),
        env.get_config(service.S_CORE, service.O_RULES_HEAD),
    )
    return git_path

def get_local_head():
    version = _shell_exec("git rev-parse HEAD", cwd=get_head_path()).strip()
    return version

def get_remote_head():
    repo_url = env.get_config("git", "repo-url")
    proc_output = _shell_exec("git ls-remote {} HEAD".format(repo_url))
    version_match = re.match(r"^([0-9a-fA-F]{40})[ \t]+HEAD$", proc_output.strip())
    assert version_match is not None, "Unexpected git-ls-remote output:\n{}".format(proc_output)
    version = version_match.group(0)
    return version


##### Private methods #####
def _shell_exec(command, cwd=None):
    proc_stdout = subprocess.check_output(
        command,
        env={ "LC_ALL": "C" },
        universal_newlines=True,
        shell=True,
        cwd=cwd,
    )
    _logger.debug("Command '{}' stdout:\n{}".format(command, proc_stdout))
    return proc_stdout
