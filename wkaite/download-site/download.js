const config = window.WKAITE_RELEASE;
for (const link of document.querySelectorAll("[data-asset]")) {
  const asset = config.assets[link.dataset.asset];
  if (asset) {
    link.href = `${config.baseUrl}/${asset}`;
    link.setAttribute("download", asset);
  }
}
