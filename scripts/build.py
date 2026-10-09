#!/usr/bin/env python3
"""Validate the plugin manifests and build one zip per harness into dist/.

  dist/firmbase-claude-<version>.zip   Claude (Cowork, Desktop, org upload)
  dist/firmbase-openai-<version>.zip   ChatGPT and Codex (platform.openai.com/plugins)

The checks mirror the OpenAI submission rules
(developers.openai.com/plugins/deploy/submission-errors), which are stricter
than Claude's; `claude plugin validate .` covers the Claude side.
"""

import json
import re
import struct
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

COMMON = ["README.md", "LICENSE", ".mcp.json", "skills", "assets"]
PACKAGES = {
    "claude": COMMON + [".claude-plugin/plugin.json"],
    "openai": COMMON + [".codex-plugin/plugin.json"],
}

CATEGORIES = {
    "Productivity", "Creativity", "Developer Tools", "Business & Operations",
    "Data & Analytics", "Communication", "Education & Research", "Security",
    "Finance", "Healthcare", "Travel", "Entertainment", "Other",
}

errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def load(rel):
    return json.loads((ROOT / rel).read_text())


def check_https(value, field):
    check(isinstance(value, str) and value.startswith("https://") and len(value) <= 1024,
          f"{field} must be an HTTPS URL of at most 1024 characters")


def check_image(rel, field):
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"{field}: {rel} does not exist")
        return
    check(path.stat().st_size <= 5 * 1024 * 1024, f"{field}: {rel} is larger than 5 MiB")
    if path.suffix == ".png":
        w, h = struct.unpack(">II", path.read_bytes()[16:24])
        check(w == h and 48 <= w <= 4096, f"{field}: {rel} is {w}x{h}, must be square, 48-4096 px")
    elif path.suffix == ".svg":
        m = re.search(r'viewBox="\s*[\d.]+\s+[\d.]+\s+([\d.]+)\s+([\d.]+)', path.read_text())
        check(m is not None and m[1] == m[2] and float(m[1]) >= 48,
              f"{field}: {rel} needs a square numeric viewBox of at least 48")
    else:
        errors.append(f"{field}: {rel} must be .png or .svg")


def relative_luminance(hex_color):
    def channel(c):
        c = int(c, 16) / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(hex_color[i:i + 2]) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def validate():
    claude = load(".claude-plugin/plugin.json")
    codex = load(".codex-plugin/plugin.json")
    mcp = load(".mcp.json")

    version = codex.get("version", "")
    check(re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?", version), f"version {version!r} is not semver")
    check(claude.get("version") == version,
          f"version mismatch: .claude-plugin {claude.get('version')} vs .codex-plugin {version}")

    for m, label in ((claude, ".claude-plugin"), (codex, ".codex-plugin")):
        check(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", m.get("name", "")), f"{label}: invalid name")
        check(0 < len(m.get("description", "")) <= 1024, f"{label}: description must be 1-1024 characters")

    ui = codex.get("interface", {})
    for field, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000),
                         ("developerName", 80)):
        check(0 < len(ui.get(field, "")) <= limit, f"interface.{field} must be 1-{limit} characters")
    check(ui.get("category") in CATEGORIES, f"interface.category {ui.get('category')!r} is not allowed")
    caps = ui.get("capabilities", [])
    check(len(caps) <= 20 and all(len(c) <= 120 for c in caps), "interface.capabilities: max 20 x 120 chars")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        check_https(ui.get(field), f"interface.{field}")
    prompts = ui.get("defaultPrompt", [])
    check(len(prompts) <= 3 and all(len(p) <= 128 and "@" not in p for p in prompts),
          "interface.defaultPrompt: max 3 prompts of 128 chars, no @mentions")
    check(len(set(prompts)) == len(prompts), "interface.defaultPrompt: duplicates")
    if "brandColor" in ui:
        check(re.fullmatch(r"#[0-9A-Fa-f]{6}", ui["brandColor"]) and contrast(ui["brandColor"], "#FFFFFF") >= 2,
              "interface.brandColor must be #RRGGBB with 2:1 contrast against white")
    if "brandColorDark" in ui:
        check(re.fullmatch(r"#[0-9A-Fa-f]{6}", ui["brandColorDark"]) and contrast(ui["brandColorDark"], "#212121") >= 2,
              "interface.brandColorDark must be #RRGGBB with 2:1 contrast against #212121")
    check_image(ui.get("logo", ""), "interface.logo")
    check_image(ui.get("composerIcon", ""), "interface.composerIcon")
    check_image(claude.get("icon", ""), ".claude-plugin icon")
    check(codex.get("mcpServers") == "./.mcp.json", ".codex-plugin: mcpServers must be ./.mcp.json")

    servers = mcp.get("mcpServers", {})
    check(len(servers) == 1, ".mcp.json: exactly one MCP server expected")
    for name, s in servers.items():
        check(s.get("url", "").startswith("https://"), f".mcp.json: {name} must use an HTTPS url")

    names = set()
    for skill in sorted((ROOT / "skills").iterdir()):
        if not skill.is_dir():
            errors.append(f"skills/{skill.name}: files directly under skills/ are ignored")
            continue
        md = skill / "SKILL.md"
        if not md.is_file():
            errors.append(f"skills/{skill.name}: missing SKILL.md")
            continue
        m = re.match(r"---\n(.*?)\n---\n", md.read_text(), re.S)
        if not m:
            errors.append(f"skills/{skill.name}: missing front matter")
            continue
        meta = dict(re.findall(r"^(\w+):\s*(.*)$", m[1], re.M))
        check(meta.get("name") == skill.name, f"skills/{skill.name}: name must match the folder")
        check(0 < len(meta.get("description", "")) <= 1024, f"skills/{skill.name}: description must be 1-1024 chars")
        check(len(codex["name"]) + 1 + len(skill.name) <= 64, f"skills/{skill.name}: plugin+skill name over 64 chars")
        check(skill.name not in names, f"skills/{skill.name}: duplicate name")
        names.add(skill.name)

    return version


def files_for(entries):
    for entry in entries:
        path = ROOT / entry
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*") if p.is_file() and not p.name.startswith("."))
        else:
            yield path


def build(version):
    DIST.mkdir(exist_ok=True)
    for harness, entries in PACKAGES.items():
        out = DIST / f"firmbase-{harness}-{version}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in files_for(entries):
                # Fixed timestamp so the same commit always gives the same zip.
                info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), (2020, 1, 1, 0, 0, 0))
                info.external_attr = 0o644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, path.read_bytes())
        print(f"built {out.relative_to(ROOT)}")


if __name__ == "__main__":
    version = validate()
    if errors:
        print("validation failed:", *errors, sep="\n  - ", file=sys.stderr)
        sys.exit(1)
    print(f"manifests ok (version {version})")
    if "--check" not in sys.argv:
        build(version)
