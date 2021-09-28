from docusign_integration.models.envelope import IncludeTypeEnum
import fitz

from docusign_integration.api.envelope import EnvelopeApi
import pytest
from os import getenv
import pydash

skip_by_env = pytest.mark.skip_by_env("BASE_URL", "ENVELOP_ID", "ACCOUNT_ID")


@skip_by_env
def test_get_envelope_data(envelope_api: EnvelopeApi):
    envelope_data = envelope_api.get_envelope_data(
        getenv("ACCOUNT_ID"),
        getenv("ENVELOP_ID"),
        advanced_update=False,
        include=[IncludeTypeEnum.CUSTOM_FIELDS],
    )
    assert envelope_data is not None


@skip_by_env
def test_list_envelope_documents(envelope_api: EnvelopeApi):
    envelope_data = envelope_api.list_envelope_documents(
        getenv("ACCOUNT_ID"), getenv("ENVELOP_ID"), only_content=False
    )

    assert envelope_data is not None

    envelope_data = envelope_api.list_envelope_documents(
        getenv("ACCOUNT_ID"), getenv("ENVELOP_ID"), only_content=True
    )
    only_content_documents = pydash.filter_(
        envelope_data.get("envelopeDocuments", []),
        lambda x: x.get("type") != "content",
    )
    assert len(only_content_documents) == 0


@skip_by_env
def test_download_envelope_document(envelope_api: EnvelopeApi):
    envelope_data = envelope_api.list_envelope_documents(
        getenv("ACCOUNT_ID"),
        getenv("ENVELOP_ID"),
    )

    envelope_documents = envelope_data.get("envelopeDocuments", [])
    assert len(envelope_documents) > 0
    document = envelope_documents.pop()

    document_id = document.get("documentId")
    assert document_id is not None
    document_file = envelope_api.download_envelope_document(
        getenv("ACCOUNT_ID"), getenv("ENVELOP_ID"), document_id
    )

    assert isinstance(document_file, fitz.Document)


@skip_by_env
def test_list_document_recipients(envelope_api: EnvelopeApi):
    envelope_data = envelope_api.list_document_recipients(
        getenv("ACCOUNT_ID"),
        getenv("ENVELOP_ID"),
    )

    assert envelope_data is not None
    assert len(envelope_data.get("signers", [])) > 0
