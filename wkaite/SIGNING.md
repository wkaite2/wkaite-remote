# 签名与 GitHub Secrets

## Android

已生成持久 Android 上传密钥：

```text
client-builder/secrets/wkaite-upload.jks
client-builder/secrets/android.properties
client-builder/secrets/ANDROID_SIGNING_KEY.base64
```

文件权限必须保持 `600`，不能提交到 Git、聊天或公共网盘。GitHub Actions 需要以下 Secrets：

| Secret | 来源 |
|---|---|
| `ANDROID_SIGNING_KEY` | `ANDROID_SIGNING_KEY.base64` 的全部单行内容 |
| `ANDROID_ALIAS` | `android.properties` 中的 `ANDROID_ALIAS` |
| `ANDROID_KEY_STORE_PASSWORD` | `android.properties` 中的 `ANDROID_KEY_STORE_PASSWORD` |
| `ANDROID_KEY_PASSWORD` | `android.properties` 中的 `ANDROID_KEY_PASSWORD` |

若已安装并登录 GitHub CLI：

```bash
repo=YOUR_GITHUB_USER/YOUR_REPO
gh secret set ANDROID_SIGNING_KEY --repo "$repo" < client-builder/secrets/ANDROID_SIGNING_KEY.base64
gh secret set ANDROID_ALIAS --repo "$repo" --body wkaite
gh secret set ANDROID_KEY_STORE_PASSWORD --repo "$repo" --body "$(awk -F= '$1=="ANDROID_KEY_STORE_PASSWORD"{print $2}' client-builder/secrets/android.properties)"
gh secret set ANDROID_KEY_PASSWORD --repo "$repo" --body "$(awk -F= '$1==\"ANDROID_KEY_PASSWORD\"{print $2}' client-builder/secrets/android.properties)"
```

## Windows

未签名 MSI/EXE 可以生成和安装，但可能触发 SmartScreen。正式发布需要 Authenticode 证书。Windows 证书的格式取决于证书提供商，接入前需要确认是否支持命令行签名和 CI 中的硬件令牌；大多数托管 CI 不直接支持 USB 令牌。

## macOS

未签名 DMG 可以生成，但用户首次打开时需要允许运行。无提示安装和分发需要：

- Apple Developer Program 成员资格
- Developer ID Application 证书
- App-specific password 或 App Store Connect API Key
- 公证工作流

该证书只能在 macOS 和 Apple 公证服务中使用，应通过 GitHub Actions Secrets 注入。

## Source License

本项目修改并分发 RustDesk 源代码，RustDesk 使用 GNU AGPL v3。公开二进制时，应同时公开对应源码和构建修改；仓库内的 `LICENCE`、`wkaite/` 修改和固定提交信息满足源码溯源要求。请勿把公开客户端源码仓库改成无法取得源码的私有仓库。
