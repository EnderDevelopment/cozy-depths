"""Download the Rainy Hearth Fabric 1.21.1 pack from Modrinth.

Run with Python 3.9+ and an internet connection:
    python download_rainy_hearth.py
"""
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import json

GAME_VERSION = "1.21.1"
LOADER = "fabric"
ROOT = Path("Rainy-Hearth-1.21.1")
MODS = [
    "fabric-api", "sodium", "iris", "lithium", "ferrite-core",
    "immediatelyfast", "entityculling", "ambientsounds",
    "sound-physics-remastered", "fallingleaves", "continuity", "appleskin",
    "travelersbackpack", "jade", "waystones", "xaeros-minimap",
    "xaeros-world-map", "emi", "friends-and-foes", "naturalist", "mouse-tweaks",
    "shulkerboxtooltip", "inventory-profiles-next", "simple-voice-chat",
]
SHADERS = ["complementary-reimagined"]


def get_json(url):
    request = Request(url, headers={"User-Agent": "Rainy-Hearth-Pack/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def download(url, destination):
    request = Request(url, headers={"User-Agent": "Rainy-Hearth-Pack/1.0"})
    with urlopen(request, timeout=120) as response:
        destination.write_bytes(response.read())


def latest_version(slug, loaders):
    query = quote(json.dumps({"game_versions": [GAME_VERSION], "loaders": loaders}))
    versions = get_json(f"https://api.modrinth.com/v2/project/{slug}/version?filters={query}")
    if not versions:
        raise RuntimeError(f"No compatible {GAME_VERSION} {loaders[0]} release found for {slug}")
    return versions[0]


def install_project(slug, folder, loaders):
    version = latest_version(slug, loaders)
    files = [item for item in version["files"] if item.get("primary")]
    if not files:
        files = version["files"]
    selected = files[0]
    destination = folder / selected["filename"]
    print(f"Downloading {selected['filename']}")
    download(selected["url"], destination)


def main():
    mods_folder = ROOT / "mods"
    shaders_folder = ROOT / "shaderpacks"
    mods_folder.mkdir(parents=True, exist_ok=True)
    shaders_folder.mkdir(parents=True, exist_ok=True)
    for slug in MODS:
        install_project(slug, mods_folder, [LOADER])
    for slug in SHADERS:
        install_project(slug, shaders_folder, ["iris"])
    print(f"Done. Copy the contents of {ROOT} into your Fabric 1.21.1 instance folder.")
    print("Install Fabric Loader first, then launch once so the instance folders exist.")


if __name__ == "__main__":
    main()
