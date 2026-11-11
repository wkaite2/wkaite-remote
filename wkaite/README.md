# WKAite Remote 客户端构建

基于 RustDesk `1.5.1` 固定提交 `23e5bb471a040d62f0a6ad52591fb30784265b73` 生成 WKAite Remote 跨平台安装包。

## 产物

- Windows 10/11：x86_64 MSI 和便携 EXE
- Ubuntu/Debian：x86_64/arm64 DEB、x86_64 AppImage
- macOS：Intel/Apple Silicon DMG
- Android：arm64/x86_64 APK，并提供通用 APK
- `SHA256SUMS` 和下载页面

客户端构建时锁定以下配置：

```text
产品名称: WKAite Remote
应用包名: com.wkaite.remote
ID/中继服务器: 220.154.11.66
服务器公钥: Bs0Kogt1I6aQfDvZFyqu3ZF7ZdRDW0evNRGO0DPX3hQ=
```

自动更新检查、RustDesk 公共 API 设备注册和服务器设置修改均被关闭，避免客户端更新后脱离自建服务器。

## 本地测试

```bash
python3 -m unittest discover -s client-builder/tests -v
./client-builder/tests/test_fetch_upstream.sh
./client-builder/tests/test_verify_release.sh
```

实际四平台安装包由 [release-repo](release-repo/.github/workflows/wkaite-client-release.yml) 的 GitHub Actions 构建。发布仓库包含固定源代码和修改后的原生构建流程。

## 发布流程

1. 将 `client-builder/release-repo` 推送为 GitHub 仓库。
2. 按 [SIGNING.md](SIGNING.md) 写入 Android 签名 Secrets。
3. 运行 `WKAite Remote release` 工作流，填写例如 `wkaite-v1.5.1.1` 的标签。
4. 工作流生成各平台包、校验哈希，并发布为正式 GitHub Release。
5. 将 `download-site/release-config.js` 中的 `OWNER/REPO` 替换为实际仓库地址，再启用 GitHub Pages 或上传到下载服务器。

完整的 Windows Authenticode 与 macOS Developer ID/公证需要额外证书。没有证书时，安装包可生成并安装，但 Windows SmartScreen 和 macOS Gatekeeper 可能显示未验证来源提示。

## 安全

Android 上传密钥位于 `client-builder/secrets/`，已从 Git 排除且权限为 `600`。该密钥必须长期保留；丢失后，已安装 Android 客户端无法无卸载升级。其余凭据只放在 GitHub Actions Secrets。
