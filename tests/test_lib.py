from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import spacy

from blacktape.lib import chunks
from blacktape.util import md5_file


@pytest.mark.parametrize(
    "filename, digest",
    [
        ("Crime_and_Punishment.txt", "389629230c0ad81871712db3c3843c4a"),
        ("The_History_of_Don_Quixote.txt", "3ca6ba13df859a9a8fb078c204356cb0"),
    ],
)
def test_chunks(en_core_web_sm_3_2_0, filename, digest):

    # https://spacy.io/models
    nlp = spacy.load(en_core_web_sm_3_2_0, disable=["parser"])  # can disable more?
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
