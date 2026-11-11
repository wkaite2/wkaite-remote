import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PROFILE = {
    "product_name": "WKAite Remote",
    "package_id": "com.wkaite.remote",
    "upstream_version": "1.5.1",
    "upstream_commit": "23e5bb471a040d62f0a6ad52591fb30784265b73",
    "server_host": "220.154.11.66",
    "relay_host": "220.154.11.66",
    "key": "Bs0Kogt1I6aQfDvZFyqu3ZF7ZdRDW0evNRGO0DPX3hQ=",
}


def load_patcher():
    path = REPO / "scripts" / "configure_source.py"
    spec = importlib.util.spec_from_file_location("configure_source", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConfigureSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "src").mkdir()
        (self.root / "src" / "lib.rs").write_text(
            "mod version;\nmod updater;\n", encoding="utf-8"
        )
        (self.root / "src" / "common.rs").write_text(
            "pub fn load_custom_client() {\n"
            "    #[cfg(debug_assertions)]\n"
            "    if let Ok(data) = std::fs::read_to_string(\"./custom.txt\") {\n"
            "        return;\n"
            "    }\n"
            "}\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_applies_profile_and_is_idempotent(self):
        patcher = load_patcher()
        patcher.configure_source(PROFILE, self.root)
        patcher.configure_source(PROFILE, self.root)

        lib = (self.root / "src" / "lib.rs").read_text(encoding="utf-8")
        common = (self.root / "src" / "common.rs").read_text(encoding="utf-8")
        profile = (self.root / "src" / "build_profile.rs").read_text(encoding="utf-8")

        self.assertEqual(lib.count("mod build_profile;"), 1)
        self.assertEqual(common.count("crate::build_profile::apply();"), 1)
        self.assertIn('PRODUCT_NAME: &str = "WKAite Remote"', profile)
        self.assertIn('SERVER_HOST: &str = "220.154.11.66"', profile)
        self.assertIn('RELAY_HOST: &str = "220.154.11.66"', profile)
        self.assertIn(PROFILE["key"], profile)
        self.assertIn('OPTION_ENABLE_CHECK_UPDATE.into(), "N".into()', profile)
        self.assertIn('OPTION_ALLOW_AUTO_UPDATE.into(), "N".into()', profile)
        self.assertIn('OPTION_REGISTER_DEVICE.into(), "N".into()', profile)

    def test_updates_platform_branding_and_package_id(self):
        files = {
            "flutter/android/app/src/main/AndroidManifest.xml": 'android:label="RustDesk"\n',
            "flutter/android/app/build.gradle": 'applicationId "com.carriez.flutter_hbb"\n',
            "flutter/macos/Runner/Configs/AppInfo.xcconfig": 'PRODUCT_BUNDLE_IDENTIFIER = com.carriez.flutterHbb\n',
            "flutter/windows/runner/Runner.rc": 'VALUE "ProductName", "RustDesk" "\\0"\n',
            "res/rustdesk.desktop": 'Name=RustDesk\n',
            "res/rustdesk-link.desktop": 'Name=RustDesk\n',
        }
        for relative, content in files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        patcher = load_patcher()
        patcher.configure_source(PROFILE, self.root)
        patcher.configure_source(PROFILE, self.root)

        self.assertEqual(
            (self.root / "flutter/android/app/src/main/AndroidManifest.xml").read_text(),
            'android:label="WKAite Remote"\n',
        )
        self.assertIn(
            'applicationId "com.wkaite.remote"',
            (self.root / "flutter/android/app/build.gradle").read_text(),
        )
        self.assertIn(
            'PRODUCT_BUNDLE_IDENTIFIER = com.wkaite.remote',
            (self.root / "flutter/macos/Runner/Configs/AppInfo.xcconfig").read_text(),
        )
        self.assertIn(
            'VALUE "ProductName", "WKAite Remote"',
            (self.root / "flutter/windows/runner/Runner.rc").read_text(),
        )
        self.assertIn(
            'Name=WKAite Remote',
            (self.root / "res/rustdesk.desktop").read_text(),
        )
        self.assertIn(
            'Name=WKAite Remote',
            (self.root / "res/rustdesk-link.desktop").read_text(),
        )

    def test_rejects_server_url_with_scheme(self):
        patcher = load_patcher()
        invalid = dict(PROFILE, server_host="http://bad.example")
        with self.assertRaises(patcher.ProfileError):
            patcher.configure_source(invalid, self.root)

    def test_fails_closed_when_anchor_is_missing(self):
        (self.root / "src" / "common.rs").write_text("fn other() {}\n", encoding="utf-8")
        patcher = load_patcher()
        with self.assertRaises(patcher.PatchError):
            patcher.configure_source(PROFILE, self.root)


if __name__ == "__main__":
    unittest.main()
