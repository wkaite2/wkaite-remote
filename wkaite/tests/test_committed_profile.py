import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class CommittedProfileTests(unittest.TestCase):
    def test_source_entrypoints_apply_profile(self):
        self.assertIn("mod build_profile;", (ROOT / "src/lib.rs").read_text(encoding="utf-8"))
        self.assertIn(
            "crate::build_profile::apply();",
            (ROOT / "src/common.rs").read_text(encoding="utf-8"),
        )

    def test_locked_profile_values(self):
        profile = (ROOT / "src/build_profile.rs").read_text(encoding="utf-8")
        self.assertIn('PRODUCT_NAME: &str = "WKAite Remote"', profile)
        self.assertIn('SERVER_HOST: &str = "220.154.11.66"', profile)
        self.assertIn('RELAY_HOST: &str = "220.154.11.66"', profile)
        self.assertIn('OPTION_REGISTER_DEVICE.into(), "N".into()', profile)
        self.assertIn('OPTION_HIDE_SERVER_SETTINGS.into(), "Y".into()', profile)

    def test_android_public_identity(self):
        gradle = (ROOT / "flutter/android/app/build.gradle").read_text(encoding="utf-8")
        manifest = (ROOT / "flutter/android/app/src/main/AndroidManifest.xml").read_text(
            encoding="utf-8"
        )
        self.assertIn('applicationId "com.wkaite.remote"', gradle)
        self.assertIn('android:label="WKAite Remote"', manifest)


if __name__ == "__main__":
    unittest.main()
