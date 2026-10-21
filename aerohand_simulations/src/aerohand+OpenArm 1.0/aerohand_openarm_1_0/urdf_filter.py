"""Small, deterministic transforms applied to expanded URDF XML."""

from collections.abc import Collection
import xml.etree.ElementTree as ET


def remove_link_visuals(urdf_xml: str, link_names: Collection[str]) -> str:
    """Remove visual geometry from selected links while preserving the URDF tree."""
    root = ET.fromstring(urdf_xml)
    targets = set(link_names)
    found = set()

    for link in root.findall("link"):
        name = link.get("name")
        if name not in targets:
            continue
        found.add(name)
        for visual in list(link.findall("visual")):
            link.remove(visual)

    missing = targets - found
    if missing:
        raise ValueError(
            "URDF target links not found: " + ", ".join(sorted(missing))
        )

    return ET.tostring(root, encoding="unicode")

