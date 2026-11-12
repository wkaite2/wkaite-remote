# WKAite Remote 1.5.1.4 正式发布

- 固定下载页：http://220.154.11.66:21120/
- GitHub 发布页：https://github.com/wkaite2/wkaite-remote/releases/tag/wkaite-v1.5.1.4
- 源码：https://github.com/wkaite2/wkaite-remote/tree/wkaite-v1.5.1.4
- 校验文件：http://220.154.11.66:21120/SHA256SUMS

## 安装包

| 平台 | 用途 | 文件 |
|---|---|---|
| Windows 10/11 x64 | 推荐安装 | `rustdesk-1.5.1-x86_64.msi` |
| Windows 10/11 x64 | 便携 EXE | `rustdesk-1.5.1-x86_64.exe` |
| Windows ARM64 | 推荐安装 | `rustdesk-1.5.1-aarch64.msi` |
| Windows ARM64 | 便携 EXE | `rustdesk-1.5.1-aarch64.exe` |
| Ubuntu 22.04 x64 | 推荐离线 DEB | `WKAite-Remote-1.5.1.4-ubuntu-x86_64-offline.deb` |
| Ubuntu/Debian x64 | 标准 DEB | `rustdesk-1.5.1-x86_64.deb` |
| Ubuntu/Debian arm64 | DEB | `rustdesk-1.5.1-aarch64.deb` |
| Linux x64 | 免安装 | `rustdesk-1.5.1-x86_64.AppImage` |
| Linux arm64 | 免安装 | `rustdesk-1.5.1-aarch64.AppImage` |
| macOS Intel | DMG | `rustdesk-1.5.1-x86_64.dmg` |
| macOS Apple Silicon | DMG | `rustdesk-1.5.1-aarch64.dmg` |
| Android arm64 | 推荐 | `rustdesk-1.5.1-aarch64.apk` |
| Android armv7 | 32 位 ARM | `rustdesk-1.5.1-armv7.apk` |
| Android x86_64 | 模拟器/平板 | `rustdesk-1.5.1-x86_64.apk` |
| Android 通用 | 不确定架构时 | `rustdesk-1.5.1-universal.apk` |
| Fedora/RHEL x64 | RPM | `rustdesk-1.5.1-0.x86_64.rpm` |
| Fedora/RHEL arm64 | RPM | `rustdesk-1.5.1-0.aarch64.rpm` |
| openSUSE x64 | RPM | `rustdesk-1.5.1-0.x86_64-suse.rpm` |
| openSUSE arm64 | RPM | `rustdesk-1.5.1-0.aarch64-suse.rpm` |
| Arch Linux x64 | 软件包 | `rustdesk-1.5.1-0-x86_64.pkg.tar.zst` |

## Ubuntu 安装

推荐下载离线 DEB 后安装：

```bash
sudo dpkg -i WKAite-Remote-1.5.1.4-ubuntu-x86_64-offline.deb
sudo gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
sudo update-desktop-database /usr/share/applications 2>/dev/null || true
```

也可以使用 `sudo apt install -y ./WKAite-Remote-1.5.1.4-ubuntu-x86_64-offline.deb`。离线包已包含 `libxdo.so.3`，不依赖 Ubuntu 软件源。

## 已锁定配置

```text
产品名称: WKAite Remote
Android 包名: com.wkaite.remote
ID/中继服务器: 220.154.11.66
端口: 21116 / 21117
公钥: Bs0Kogt1I6aQfDvZFyqu3ZF7ZdRDW0evNRGO0DPX3hQ=
```

客户端关闭了 RustDesk 公共 API 注册、服务器设置修改和自动更新，安装后直接连接自建服务器。

## 验证重点

- Windows、Linux、macOS、Android 由同一标签的 GitHub Actions 构建。
- Android APK 使用固定发布密钥签名，可覆盖升级。
- Ubuntu 离线包内置键鼠控制所需的 `libxdo.so.3`，并移除对 `libxdo3 | libxdo4` 的安装时依赖。
- Linux 桌面入口使用新版封面绝对图标路径，避免旧 `rustdesk.svg` 覆盖。
- 服务器 `hbbs`、`hbbr`、`wkaite-download`、`wkaite-download-tunnel` 均处于运行状态，端口 `21116/21117` 与下载页 `21120` 正常监听。

Windows 尚未配置商用 Authenticode 证书，可能出现 SmartScreen 提示；macOS 尚未公证，首次打开可能需要在“系统设置 -> 隐私与安全性”中允许。这不影响安装和连接。

## 凭据

Android 发布签名密钥保存在本机 `client-builder/secrets/`，服务器备份位于 `/root/wkaite-secrets/`。该密钥不可删除，否则已安装的 Android 客户端无法覆盖升级。
