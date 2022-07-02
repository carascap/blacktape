import re
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory, gettempdir

import pytest
import spacy
from spacy_model_manager.lib import get_installed_model_version

from blacktape.db import db_init, db_session
from blacktape.lib import chunks, get_entities_for_spacy_model, match_patterns_in_text
from blacktape.models import FileReport, Match
from blacktape.pipeline import Pipeline
from blacktape.util import md5_file, record_workflow_config

SQLITE3_FILENAME_TEMPLATE = "{}_{}.sqlite3"


@pytest.mark.parametrize(
    "filename, digest",
    [
        ("Crime_and_Punishment.txt", "389629230c0ad81871712db3c3843c4a"),
        ("The_History_of_Don_Quixote.txt", "3ca6ba13df859a9a8fb078c204356cb0"),
    ],
)
def test_chunks(en_core_web_sm_3_3_0, filename, digest):

    # https://spacy.io/models
    nlp = spacy.load(en_core_web_sm_3_3_0, disable=["parser"])  # can disable more?
    nlp.enable_pipe("senter")

    test_dir = Path(__file__).parent.resolve()
    test_file = test_dir / "data" / filename

    assert md5_file(test_file) == digest

    file_read_options = {
        "nlp": nlp,
        "max_chunk_size": 500,
        "encoding": "UTF-8",
        # 'errors': "strict",  # Some PG test files give decoding errors with UTF-8
        "errors": "ignore",
        "newline": "",  # To preserve line endings
    }

    # Check that by putting the chunks together we get an identical file
    with TemporaryDirectory() as tmpdir:
        reconstructed_file = Path(tmpdir) / filename

        with reconstructed_file.open("w") as f:
            for chunk in chunks(test_file, **file_read_options):
                f.write(chunk)

        assert md5_file(reconstructed_file) == digest


@pytest.mark.parametrize(
    "filename, expected_matches",
    [("birds_and_bees.txt", 251)],
)
def test_pipeline(en_core_web_sm_3_3_0, filename, expected_matches):
    model = en_core_web_sm_3_3_0

    target_entities = {"PERSON", "ORG", "DATE", "GPE"}

    patterns = [(r"[0-9]+", "number"), (r"\b[A-Z][a-zA-Z]*\b", "capitalized word")]

    test_dir = Path(__file__).parent.resolve()
    test_file = test_dir / "data" / filename
    text = test_file.read_text(encoding="UTF-8")

    # DB file timestamped for this pipeline run
    db_file = Path(gettempdir()) / SQLITE3_FILENAME_TEMPLATE.format(
        test_file.name,
        datetime.now()
        .isoformat(timespec="seconds")
        .translate(str.maketrans({"-": "", ":": ""})),
    )
    session_factory = db_init(db_file)

    # Pipeline with DB session
    with Pipeline(spacy_model=model) as pipeline, db_session(
        session_factory
    ) as session:

        # Record source file info
        file_report = FileReport(path=str(test_file))
        session.add(file_report)

        # Record workflow parameters
        record_workflow_config(
            session,
            source=str(test_file),
            spacy_model=model,
            spacy_model_version=get_installed_model_version(model),
        )

        # Submit entities job
        pipeline.submit_ner_job(text, target_entities)

        # Submit regex jobs
        for pattern, label in patterns:
            pipeline.submit_regex_job(text, pattern, label)

        # Make ORM objects from job results
        for result in pipeline.results():
            for match in result:
                session.add(Match(**match))

    # Check DB output
    with db_session(session_factory) as session:

        assert session.query(Match).count() == expected_matches

        assert str(session.query(Match).first())


def test_get_entities_for_spacy_model(en_core_web_sm_3_3_0):
    assert len(get_entities_for_spacy_model(en_core_web_sm_3_3_0)) == 18


@pytest.mark.parametrize(
    "filename, patterns, expected_matches",
    [
        (
            "birds_and_bees.txt",
            [
                (r"\d+", "number"),
                (r"\b[A-Z][a-zA-Z]*\b", "capitalized word"),
            ],
            203,
        ),
        (
            "birds_and_bees.txt",
            [
                (re.compile(r"\d+"), "number"),
                (re.compile(r"\b[A-Z][a-zA-Z]*\b"), "capitalized word"),
            ],
            203,
        ),
    ],
)
def test_match_patterns_in_text(filename, patterns, expected_matches):
    test_dir = Path(__file__).parent.resolve()
    test_file = test_dir / "data" / filename
    text = test_file.read_text(encoding="UTF-8")

    matches = list(match_patterns_in_text(text, patterns))

    assert len(matches) == expected_matches
