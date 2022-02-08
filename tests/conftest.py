import pytest
from spacy_model_manager.lib import (
    SPACY_MODELS,
    get_installed_model_version,
    install_spacy_model,
)


@pytest.fixture(scope="function")
def en_core_web_sm_3_2_0() -> None:
    model, version = SPACY_MODELS.en_core_web_sm, "3.2.0"

    # Check for already installed version
    existing_version = get_installed_model_version(model)

    # Install version 3.2.0
    if existing_version != version:
        assert (
            install_spacy_model(model=SPACY_MODELS.en_core_web_sm, version="3.2.0") == 0
        )

    yield model

    # Reinstall previous version
    if existing_version and existing_version != version:
        assert install_spacy_model(model, existing_version) == 0
