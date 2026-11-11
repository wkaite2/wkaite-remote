# WKAite Remote

This repository is a modified RustDesk distribution for the WKAite Remote private
server. The original license remains in `LICENCE`.

- Upstream version: RustDesk 1.5.1
- Upstream commit: `23e5bb471a040d62f0a6ad52591fb30784265b73`
- ID and relay server: `220.154.11.66`
- Android package: `com.wkaite.remote`
- macOS bundle: `com.wkaite.remote`

The source profile is defined by `src/build_profile.rs` and applied from
`src/common.rs::load_custom_client()`. Run:

```bash
python3 -m unittest wkaite/tests/test_committed_profile.py -v
python3 wkaite/tests/test_configure_source.py -v
```

Release builds run from `.github/workflows/wkaite-client-release.yml`.
