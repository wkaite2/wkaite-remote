# 自建服务器下载站

固定下载页：

```text
http://220.154.11.66:21120/
```

服务器目录：

```text
/opt/rustdesk-selfhost/downloads/
```

页面包含 Windows、Ubuntu/Debian、macOS 和 Android 安装包，并提供 `SHA256SUMS`。Ubuntu x64 默认使用：

```text
http://220.154.11.66:21120/WKAite-Remote-1.5.1.4-ubuntu-x86_64-offline.deb
```

`TCP 21120` 已在云安全组放行。下载服务由 `wkaite-download` 和 `wkaite-download-tunnel` 两个 systemd 服务维持。

`wkaite-download` 使用线程化静态文件服务，支持并发下载、`Range` 断点续传和安装包专用 MIME 类型。服务脚本位于 `deploy/wkaite_download_server.py`，systemd 覆盖配置位于 `deploy/wkaite-download.service.d/override.conf`。
