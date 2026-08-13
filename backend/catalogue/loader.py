from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import yaml

from catalogue.models import CardDefinition, RuleSet


class CatalogueError(ValueError):
    pass


@dataclass(frozen=True)
class LoadedCard:
    card: CardDefinition
    rules: tuple[RuleSet, ...]


@dataclass(frozen=True)
class Catalogue:
    cards: tuple[LoadedCard, ...]


def _read_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise CatalogueError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise CatalogueError(f"Expected a YAML object in {path}")
    return data


def _validate_rule_ranges(card_id: str, rules: list[RuleSet]) -> None:
    for previous, current in zip(rules, rules[1:]):
        if previous.effective_to is None:
            raise CatalogueError(
                f"{card_id}: rule {previous.version} must have effective_to "
                f"before rule {current.version} starts"
            )
        if previous.effective_to >= current.effective_from:
            raise CatalogueError(
                f"{card_id}: rule periods {previous.version} and {current.version} overlap"
            )


def _load_catalogue(cards_root_value: str) -> Catalogue:
    cards_root = Path(cards_root_value)
    if not cards_root.exists():
        raise CatalogueError(f"Catalogue directory does not exist: {cards_root}")

    loaded_cards: list[LoadedCard] = []
    seen_ids: set[str] = set()

    for card_path in sorted(cards_root.glob("**/card.yaml")):
        card = CardDefinition.model_validate(_read_yaml(card_path))
        if card.id in seen_ids:
            raise CatalogueError(f"Duplicate card ID: {card.id}")
        seen_ids.add(card.id)

        rule_paths = sorted((card_path.parent / "rules").glob("*.yaml"))
        if not rule_paths:
            raise CatalogueError(f"{card.id}: no rule files found")

        rules = [RuleSet.model_validate(_read_yaml(path)) for path in rule_paths]
        for path, rule in zip(rule_paths, rules):
            if path.stem != rule.version:
                raise CatalogueError(
                    f"{card.id}: {path.name} must match rule version {rule.version}"
                )

        rules.sort(key=lambda rule: rule.effective_from)
        _validate_rule_ranges(card.id, rules)
        loaded_cards.append(LoadedCard(card=card, rules=tuple(rules)))

    loaded_cards.sort(key=lambda loaded: (loaded.card.issuer, loaded.card.name))
    return Catalogue(cards=tuple(loaded_cards))


@lru_cache(maxsize=8)
def _load_catalogue_cached(cards_root_value: str) -> Catalogue:
    return _load_catalogue(cards_root_value)


def load_catalogue(cards_root: Path, *, use_cache: bool = True) -> Catalogue:
    resolved = str(cards_root.resolve())
    if use_cache:
        return _load_catalogue_cached(resolved)
    return _load_catalogue(resolved)
