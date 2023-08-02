# coding=UTF-8
import datetime
from typing import List, Tuple, Union

from keybert import KeyBERT

from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from content_size_limit_asgi import ContentSizeLimitMiddleware

import logging
import warnings

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('kb')

router: APIRouter = APIRouter(prefix="/kb", tags=["kb"])

kw_model: KeyBERT = KeyBERT()


class KbDoc(BaseModel):
    doc: str


class KbKeyword(BaseModel):
    keyword: str
    distance: float


class EventPayload(BaseModel):
    clientName: str
    trackNumber: str
    routeName: Union[str, None] = Field(default=None)
    oldOrderStatus: Union[str, None] = Field(default=None)
    newOrderStatus: Union[str, None] = Field(default=None)
    statusReason: Union[str, None] = Field(default=None)
    destCity: Union[str, None] = Field(default=None)
    destProv: Union[str, None] = Field(default=None)
    createdOnMilliseconds: Union[int, None] = Field(default=None)
    podUrl: Union[str, None] = Field(default=None)
    podUrls: Union[List[str], None] = Field(default=None)
    estimatedDeliveryDate: Union[datetime.date, None] = Field(default=None)


class WebhookEvent(BaseModel):
    token: str
    type: str
    createdOn: datetime.datetime
    clientName: str
    payload: EventPayload


@router.post("/extract")
async def extract_keywords(body: KbDoc) -> List[KbKeyword]:
    result = kw_model.extract_keywords(body.doc)
    keywords = [KbKeyword(keyword=kw[0], distance=kw[1]) for kw in result]
    return keywords


@router.post("/WebhookEvent")
async def enqueue(body: WebhookEvent) -> dict[str, str]:
    log.info("event enqueued: \n{}".format(body))
    return {"enqueuedEvent": body.token}


app: FastAPI = FastAPI(docs_url="/kb/docs", redoc_url="/kb/redoc", openapi_url="/kb/openapi.json")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )
app.add_middleware(ContentSizeLimitMiddleware, max_content_size=2048)
app.include_router(router)
