#!/usr/bin/env bash
# 把静态站点与最新数据组装到 _site/（GitHub Pages workflow 与本地预览共用）。
set -euo pipefail
cd "$(dirname "$0")/.."
out="${1:-_site}"
rm -rf "$out"
mkdir -p "$out"
cp -R site/index.html site/assets "$out/"
cp -R data reports "$out/"
python3 - "$out" <<'PY'
import json, pathlib, sys
out = pathlib.Path(sys.argv[1])
daily = sorted((p.stem for p in pathlib.Path("reports/daily").glob("*.md")), reverse=True)
(out / "reports" / "index.json").write_text(json.dumps({"daily": daily}, ensure_ascii=False))
PY
touch "$out/.nojekyll"
echo "Built $out ($(du -sh "$out" | cut -f1))"
