# Local preview and publishing

The generated gallery lives in `site/`. Serve only that directory so repository material, source data, credentials, and operational logs cannot be reached through the preview server.

```bash
python3 scripts/validate.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8765/`. A temporary HTTPS tunnel may be used for a public review only when the material is appropriate to disclose. It must forward to the loopback server, not to the repository root; record its process, logs, expiry, and stop procedure outside this repository. Do not commit its URL, credentials, logs, or a tunnel client binary.

## GitHub Pages

The checked-in Pages workflow is intentionally manual (`workflow_dispatch`). It validates data, builds generated files, runs the full offline test suite, and rejects a deployment if generated outputs are uncommitted. After the maintainer creates a GitHub repository, select **GitHub Actions** as the Pages source and run `Publish catalogue page`.

For a project site, GitHub Pages serves `site/index.html` under `https://<owner>.github.io/<repository>/`. The gallery has no root-relative local assets: all data is inline and any verified image remains an absolute original-publisher URL. This keeps the page usable at a project subpath.

## Gallery media and language policy

English is the default. The page honors a saved manual language choice first, then a Chinese browser language preference, then English. `data/i18n.json` must provide an English title and summary for every project ID.

`data/media.json` may list only directly linkable, publicly visible media tied to an existing project source. Images are not copied into this repository. Missing or failed media uses an explicit fallback and retains the original entry link. `docs/MEDIA.md` is the generated provenance and omission ledger.
