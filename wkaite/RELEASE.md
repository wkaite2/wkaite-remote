# WKAite Remote 1.5.1 正式发布

- 下载页：https://wkaite.github.io/wkaite-remote/
- 发布页：https://github.com/wkaite/wkaite-remote/releases/tag/wkaite-v1.5.1.1
- SHA256：https://github.com/wkaite/wkaite-remote/releases/download/wkaite-v1.5.1.1/SHA256SUMS
- 源码：https://github.com/wkaite/wkaite-remote/tree/wkaite-v1.5.1.1

## 安装包

| 平台 | 用途 | 文件 |
|---|---|---|
| Windows 10/11 x64 | 推荐安装 | `rustdesk-1.5.1-x86_64.msi` |
| Windows 10/11 x64 | 便携自解压 | `rustdesk-1.5.1-x86_64.exe` |
| Windows ARM64 | 推荐安装 | `rustdesk-1.5.1-aarch64.msi` |
| Windows ARM64 | 便携自解压 | `rustdesk-1.5.1-aarch64.exe` |
| Ubuntu/Debian x64 | DEB 安装 | `rustdesk-1.5.1-x86_64.deb` |
| Ubuntu/Debian arm64 | DEB 安装 | `rustdesk-1.5.1-aarch64.deb` |
| Linux x64 | 免安装 AppImage | `rustdesk-1.5.1-x86_64.AppImage` |
| Linux arm64 | 免安装 AppImage | `rustdesk-1.5.1-aarch64.AppImage` |
| macOS Intel | DMG 安装 | `rustdesk-1.5.1-x86_64.dmg` |
| macOS Apple Silicon | DMG 安装 | `rustdesk-1.5.1-aarch64.dmg` |
| Android arm64 | 推荐 | `rustdesk-1.5.1-aarch64.apk` |
| Android armv7 | 32 位 ARM 设备 | `rustdesk-1.5.1-armv7.apk` |
| Android x86_64 | 模拟器/平板 | `rustdesk-1.5.1-x86_64.apk` |
| Android 通用 | 不确定架构时 | `rustdesk-1.5.1-universal.apk` |

## 已锁定配置

```text
产品名称: WKAite Remote
Android 包名: com.wkaite.remote
ID/中继服务器: 220.154.11.66
端口: 21116 / 21117
公钥: Bs0Kogt1I6aQfDvZFyqu3ZF7ZdRDW0evNRGO0DPX3hQ=
```

客户端已关闭 RustDesk 公共 API 注册、服务器设置修改和自动更新，安装后直接使用自建服务器。

## 验证结果

- GitHub Actions 四平台构建全部成功。
- Release 为公开正式版，19 个资产，无草稿或预发布标记。
- Windows MSI、Ubuntu DEB、macOS DMG、Android APK 已重新下载并通过 SHA256 比对。
- Ubuntu 成品运行时写入 `rendezvous_server = '220.154.11.66:21116'`，Key 已验证。
- Android APK 中确认存在 `WKAite Remote`、`com.wkaite.remote`、服务器地址和公钥。
- Android APK 使用固定发布密钥签名。

Android 上传签名密钥保存在本机 `client-builder/secrets/`，不可删除；否则后续版本无法覆盖升级。

Windows 当前未使用商业 Authenticode 证书，SmartScreen 可能显示未知发布者。macOS 当前为未公证 DMG，首次打开可能需要在“系统设置 -> 隐私与安全性”允许。完成证书配置后可消除对应系统提示，不需要修改客户端功能代码。
