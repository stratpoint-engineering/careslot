"""View-models shared by several apps. Templates read only these typed objects, never models,
so Day 1 can swap mock data for real queries without touching a template."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Option:
    """One entry of a select Field."""

    value: str
    label: str
    selected: bool = False


@dataclass(frozen=True)
class NavLink:
    url_name: str
    label: str
