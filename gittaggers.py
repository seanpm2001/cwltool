import subprocess
import sys
import time

import importlib.metadata

from typing import Any

from setuptools.command.egg_info import egg_info

SETUPTOOLS_VER = importlib.metadata.version("setuptools").split(".")

RECENT_SETUPTOOLS = (
    int(SETUPTOOLS_VER[0]) > 40
    or (int(SETUPTOOLS_VER[0]) == 40 and int(SETUPTOOLS_VER[1]) > 0)
    or (int(SETUPTOOLS_VER[0]) == 40 and int(SETUPTOOLS_VER[1]) == 0 and int(SETUPTOOLS_VER[2]) > 0)
)


class EggInfoFromGit(egg_info):
    """Tag the build with git commit timestamp.

    If a build tag has already been set (e.g., "egg_info -b", building
    from source package), leave it alone.
    """

    def git_timestamp_tag(self) -> str:
        gitinfo = subprocess.check_output(
            ["git", "log", "--first-parent", "--max-count=1", "--format=format:%ct", "."]
        ).strip()
        return time.strftime(".%Y%m%d%H%M%S", time.gmtime(int(gitinfo)))

    def tags(self) -> Any:
        if self.tag_build is None:
            try:
                self.tag_build = self.git_timestamp_tag()
            except subprocess.CalledProcessError:
                pass
        return egg_info.tags(self)  # type: ignore[no-untyped-call]

    if RECENT_SETUPTOOLS:
        vtags = property(tags)
