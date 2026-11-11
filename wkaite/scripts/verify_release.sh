#!/usr/bin/env bash
set -euo pipefail
release_dir="${1:-}"
[[ -n "${release_dir}" && -d "${release_dir}" ]] || {
  printf 'usage: %s RELEASE_DIR\n' "$0" >&2
  exit 2
}
failures=0
require_any() {
  local label="$1" pattern="$2"
  local matches
  matches="$(find "${release_dir}" -maxdepth 1 -type f -name "${pattern}" -print -quit)"
  if [[ -n "${matches}" ]]; then
    printf '[通过] %s: %s\n' "${label}" "$(basename -- "${matches}")"
  else
    printf '[失败] %s: 缺少 %s\n' "${label}" "${pattern}" >&2
    failures=$((failures + 1))
  fi
}

require_any "Windows x86_64 MSI" '*-x86_64.msi'
require_any "Windows x86_64 EXE" '*-x86_64.exe'
require_any "Ubuntu x86_64 DEB" '*-x86_64.deb'
require_any "Ubuntu arm64 DEB" '*-aarch64.deb'
require_any "Linux x86_64 AppImage" '*-x86_64.AppImage'
require_any "macOS Intel DMG" '*-x86_64.dmg'
require_any "macOS Apple Silicon DMG" '*-aarch64.dmg'
require_any "Android arm64 APK" '*-aarch64.apk'
require_any "Android x86_64 APK" '*-x86_64.apk'

sums="${release_dir}/SHA256SUMS"
if [[ ! -f "${sums}" ]]; then
  printf '[失败] 缺少 SHA256SUMS\n' >&2
  failures=$((failures + 1))
else
  if (cd "${release_dir}" && sha256sum --check --quiet SHA256SUMS); then
    printf '[通过] SHA-256 校验\n'
  else
    printf '[失败] SHA-256 校验失败\n' >&2
    failures=$((failures + 1))
  fi
fi

if [[ ${failures} -ne 0 ]]; then
  printf '发布资产契约检查失败: %d 项\n' "${failures}" >&2
  exit 1
fi
printf '发布资产契约通过。\n'
