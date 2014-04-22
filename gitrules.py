import os
import re

from gns import env
from gns import service
from gns.fetchers import fmod_git


##### Public methods #####
def get_head_path():
    git_path = os.path.join(
        env.get_config(service.S_CORE, service.O_RULES_DIR),
        env.get_config(service.S_CORE, service.O_RULES_HEAD),
    )
    return git_path

def get_local_head():
    version = fmod_git._shell_exec("git rev-parse HEAD", cwd=get_head_path()).strip() # pylint: disable=W0212
    return version

def get_remote_head():
    repo_url = env.get_config(fmod_git.S_GIT, fmod_git.O_REPO_URL)
    proc_output = fmod_git._shell_exec("git ls-remote {} HEAD".format(repo_url)) # pylint: disable=W0212
    version_match = re.match(r"^([0-9a-fA-F]{40})[ \t]+HEAD$", proc_output.strip())
    assert version_match is not None, "Unexpected git-ls-remote output:\n{}".format(proc_output)
    version = version_match.group(0)
    return version
