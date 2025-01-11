import dataclasses as dc
import datetime


@dc.dataclass(kw_only=True)
class RecommendRequest:
    songs: list[str]

@dc.dataclass(kw_only=True)
class RecommendResponse:
    songs: list[str]
    version: str
    model_date: datetime.datetime
