import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = (
    "res/mac-tray-dark-x2.png",
    "res/mac-tray-light-x2.png",
    "res/icon.png",
    "res/128x128.png",
    "flutter/assets/icon.svg",
    "flutter/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png",
)


class RequiredAssetTests(unittest.TestCase):
    def test_release_assets_exist(self):
        for relative in REQUIRED:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_ignored_assets_are_tracked(self):
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--", *REQUIRED],
            check=True,
            text=True,
            capture_output=True,
        )
        tracked = set(result.stdout.splitlines())
        self.assertEqual(set(REQUIRED), tracked)


if __name__ == "__main__":
    unittest.main()
