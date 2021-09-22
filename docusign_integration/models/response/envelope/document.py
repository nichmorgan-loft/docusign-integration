from typing import List
from pydantic import BaseModel


class EnvelopeDocumentAvailableType(BaseModel):
    type: str
    isDefault: bool


class EnvelopeDocumentPage(BaseModel):
    pageId: str
    sequence: int
    height: int
    width: int
    dpi: int


class EnvelopeDocument(BaseModel):
    documentId: int
    documentIdGuid: str
    name: str
    type: str
    uri: str
    order: int
    pages: List[EnvelopeDocumentPage]
    availableDocumentTypes: List[EnvelopeDocumentAvailableType]
    display: str
    includeInDownload: bool
    signerMustAcknowledge: str
    templateRequired: bool
    authoritativeCopy: bool


class EnvelopeListDocumentsResponse(BaseModel):
    envelopeId: str
    envelopeDocuments: List[EnvelopeDocument]
