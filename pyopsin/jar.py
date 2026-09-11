import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

RELEASES_API = "https://api.github.com/repos/dan2097/opsin/releases/latest"
JAR_FILENAME = "opsin_cli.jar"
_USER_AGENT = "pyopsin"


def default_jar_dir() -> Path:
    override = os.environ.get("PYOPSIN_JAR_DIR")
    if override:
        return Path(override)
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "pyopsin"
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        return Path(xdg) / "pyopsin"
    return Path.home() / ".cache" / "pyopsin"


def default_jar_path() -> Path:
    return default_jar_dir() / JAR_FILENAME


def packaged_jar_path() -> Path:
    from importlib.resources import files

    return Path(str(files("pyopsin").joinpath(JAR_FILENAME)))


def latest_cli_jar_asset() -> tuple[str, str]:
    request = urllib.request.Request(
        RELEASES_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": _USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    for asset in data.get("assets", []):
        name = asset.get("name", "")
        if name.startswith("opsin-cli-") and name.endswith("-jar-with-dependencies.jar"):
            url = asset.get("browser_download_url")
            if url:
                return url, name
    raise RuntimeError(
        "No opsin-cli-*-jar-with-dependencies.jar asset was found on the latest OPSIN release."
    )


def download_opsin_jar(dest: Path | None = None) -> Path:
    dest = Path(dest) if dest is not None else default_jar_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    url, name = latest_cli_jar_asset()
    request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        with tempfile.NamedTemporaryFile(delete=False, dir=dest.parent, suffix=".jar") as tmp:
            shutil.copyfileobj(response, tmp)
            tmp_path = Path(tmp.name)
    try:
        tmp_path.replace(dest)
    except OSError:
        shutil.copy2(tmp_path, dest)
        tmp_path.unlink(missing_ok=True)
    print(f"Downloaded {name} to {dest}", file=sys.stderr)
    return dest


def ensure_opsin_jar(dest: Path | None = None, force: bool = False) -> Path:
    dest = Path(dest) if dest is not None else default_jar_path()
    if dest.exists() and not force:
        return dest
    try:
        return download_opsin_jar(dest)
    except (urllib.error.URLError, TimeoutError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        raise FileNotFoundError(
            f"Could not download the OPSIN CLI JAR to {dest}. "
            "Set PyOpsin(path=...) to a local JAR, or check network access to "
            "https://github.com/dan2097/opsin/releases"
        ) from exc


def resolve_opsin_jar(path: str | None = None) -> Path:
    if path:
        resolved = Path(path)
        if resolved.exists():
            return resolved
        raise FileNotFoundError(
            f"No OPSIN .jar file was found at {path}, check your path to the file."
        )
    packaged = packaged_jar_path()
    if packaged.exists():
        return packaged
    cached = default_jar_path()
    if cached.exists():
        return cached
    return ensure_opsin_jar(cached)
