#!/usr/bin/env bash
set -euo pipefail

BASE_DEB="${1:-}"
OUTPUT="${2:-}"
VERSION="1.5.1.4"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
LIBXDO_DEB="${LIBXDO_DEB:-}"

[[ -n "${BASE_DEB}" && -f "${BASE_DEB}" ]] || {
  printf '用法: %s BASE_DEB [OUTPUT_DEB]\n' "$0" >&2
  exit 2
}
[[ -n "${OUTPUT}" ]] || OUTPUT="WKAite-Remote-${VERSION}-ubuntu-x86_64-offline.deb"
for command in dpkg-deb md5sum curl; do
  command -v "${command}" >/dev/null 2>&1 || { echo "缺少命令: ${command}" >&2; exit 1; }
done

tmp="$(mktemp -d)"
trap 'rm -rf -- "${tmp}"' EXIT
root="${tmp}/root"
dpkg-deb -R "${BASE_DEB}" "${root}"
[[ -x "${root}/usr/share/rustdesk/rustdesk" ]] || { echo '基础包不是 Ubuntu/Debian RustDesk 客户端' >&2; exit 1; }

if [[ -z "${LIBXDO_DEB}" ]]; then
  LIBXDO_DEB="${tmp}/libxdo3.deb"
  curl -fsSL --retry 3 --max-time 60 -o "${LIBXDO_DEB}" \
    'https://mirrors.tuna.tsinghua.edu.cn/ubuntu/pool/universe/x/xdotool/libxdo3_3.20160805.1-4_amd64.deb'
fi
mkdir -p "${tmp}/libxdo"
dpkg-deb -x "${LIBXDO_DEB}" "${tmp}/libxdo"
xdo_so="$(find "${tmp}/libxdo/usr/lib" -type f -name 'libxdo.so.3' -print -quit)"
[[ -n "${xdo_so}" ]] || { echo '找不到 libxdo.so.3' >&2; exit 1; }
cp -a "${xdo_so}" "${root}/usr/share/rustdesk/lib/"
mkdir -p "${root}/usr/share/rustdesk/licenses"
cp "${tmp}/libxdo/usr/share/doc/libxdo3/copyright" "${root}/usr/share/rustdesk/licenses/libxdo3.copyright"

install -m 0644 "${REPO_ROOT}/res/scalable.svg" \
  "${root}/usr/share/icons/hicolor/scalable/apps/rustdesk.svg"
install -m 0644 "${REPO_ROOT}/flutter/assets/icon.svg" \
  "${root}/usr/share/rustdesk/data/flutter_assets/assets/icon.svg"
install -m 0644 "${REPO_ROOT}/res/rustdesk.desktop" \
  "${root}/usr/share/applications/rustdesk.desktop"
install -m 0644 "${REPO_ROOT}/res/rustdesk-link.desktop" \
  "${root}/usr/share/applications/rustdesk-link.desktop"

python3 - "${root}/DEBIAN/control" "${VERSION}" <<'PY'
from pathlib import Path
import re, sys
path = Path(sys.argv[1])
version = sys.argv[2]
text = path.read_text()
text = re.sub(r"^Version: .*$", f"Version: {version}", text, count=1, flags=re.M)
text = text.replace("libxdo3 | libxdo4, ", "")
path.write_text(text)
PY

(
  cd "${root}"
  find . -path './DEBIAN' -prune -o -type f -printf '%P\0' | sort -z | xargs -0 md5sum > DEBIAN/md5sums
)
dpkg-deb --build --root-owner-group "${root}" "${OUTPUT}" >/dev/null
printf '已生成: %s\n' "${OUTPUT}"
sha256sum "${OUTPUT}"
