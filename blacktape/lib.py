import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

import spacy


def get_entities_for_spacy_model(model: str) -> List[str]:
    return spacy.load(model).meta["labels"]["ner"]


def match_entities_in_text(
    text: str, spacy_model: str, entity_types: Optional[Iterable[str]] = None
) -> List[Dict[str, Union[str, int]]]:
    res = []

    for entity in spacy.load(spacy_model)(text).ents:
        if entity_types and entity.label_ not in entity_types:
            continue

        res.append(
            {
                "text": entity.text,
                "label": entity.label_,
                "offset": entity.start_char,
            }
        )

    return res


def match_pattern_in_text(text: str, pattern: str) -> List[Dict[str, Union[str, int]]]:
    return [
        {
            "pattern": pattern,
            "text": match.group(),
            "offset": match.start(),
        }
        for match in re.finditer(pattern, text)
    ]


def match_patterns_in_text(
    text: str, patterns: [Iterable[str]]
) -> List[Dict[str, Union[str, int]]]:
    return [match for pattern in patterns for match in match_pattern_in_text(text, pattern)]


def match_entities_in_file(
    path: Union[Path, str],
    spacy_model_name: str,
    entity_types: Optional[Iterable[str]] = None,
) -> List[Dict[str, Union[str, int]]]:
    return match_entities_in_text(
        Path(path).read_text(encoding="UTF-8"), spacy_model_name, entity_types
    )


def match_patterns_in_file(
    path: Union[Path, str], patterns: [Iterable[str]]
) -> List[Dict[str, Union[str, int]]]:
    return match_patterns_in_text(Path(path).read_text(encoding="UTF-8"), patterns)
