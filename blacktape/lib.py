import re
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Union

import spacy


# match types
ENTITY = "entity"
PATTERN = "pattern"


def get_entities_for_spacy_model(model: str) -> List[str]:
    return spacy.load(model).meta["labels"]["ner"]


def match_entities_in_text(
    text: str, spacy_model: str, entity_types: Optional[Iterable[str]] = None, **kwargs
) -> List[Dict[str, Union[str, int]]]:
    res = []

    for entity in spacy.load(spacy_model)(text).ents:
        if entity_types and entity.label_ not in entity_types:
            continue

        res.append(
            {
                "type": ENTITY,
                "text": entity.text,
                "label": entity.label_,
                "offset": entity.start_char,
                **kwargs,
            }
        )

    return res


def match_pattern_in_text(
    text: str, pattern: str, **kwargs
) -> List[Dict[str, Union[str, int]]]:
    return [
        {
            "type": PATTERN,
            "pattern": pattern,
            "text": match.group(),
            "offset": match.start(),
            **kwargs,
        }
        for match in re.finditer(pattern, text)
    ]


def match_patterns_in_text(
    text: str, patterns: [Iterable[str]], **kwargs
) -> List[Dict[str, Union[str, int]]]:
    return [
        match
        for pattern in patterns
        for match in match_pattern_in_text(text, pattern, **kwargs)
    ]


def match_entities_in_file(
    path: Union[Path, str],
    spacy_model_name: str,
    entity_types: Optional[Iterable[str]] = None,
    **kwargs,
) -> List[Dict[str, Union[str, int]]]:
    return match_entities_in_text(
        Path(path).read_text(encoding="UTF-8"), spacy_model_name, entity_types, **kwargs
    )


def match_patterns_in_file(
    path: Union[Path, str], patterns: [Iterable[str]], **kwargs
) -> List[Dict[str, Union[str, int]]]:
    return match_patterns_in_text(
        Path(path).read_text(encoding="UTF-8"), patterns, **kwargs
    )


def chunks(
    file_path: Path, nlp: spacy.Language, max_chunk_size: int = 500_000, **kwargs
) -> Iterator[str]:
    """
    Tries to break a text file into chunks of at most max_chunk_size characters without splitting sentences.
    """

    with file_path.open(mode="r", **kwargs) as f:

        carryover = ""

        while chunk := f.read(max_chunk_size - len(carryover)):
            # Add possibly truncated sentence from previous block
            chunk = carryover + chunk

            # Parse sentences in current block
            doc = nlp(chunk)
            sentences = list(doc.sents)

            # Try to return a block of complete sentences
            if len(sentences) > 1 and (offset := sentences[-1].start_char) > 0:

                # Return up to the beginning of the last sentence
                yield chunk[:offset]
                carryover = chunk[offset:]

            else:
                yield chunk
                carryover = ""
