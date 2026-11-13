from fastapi import FastAPI
from pydantic import BaseModel, Field

from . import store

app = FastAPI(title="smoke-alerts")


class Settings(BaseModel):
    threshold: float = Field(gt=0, le=500)
    sites: list[str] = Field(min_length=1, max_length=10)


@app.get("/settings")
def read_settings():
    return store.get_settings(store.conn())


@app.put("/settings")
def write_settings(s: Settings):
    c = store.conn()
    store.set_setting(c, "threshold", s.threshold)
    store.set_setting(c, "sites", [x.upper() for x in s.sites])
    return store.get_settings(c)


@app.get("/readings")
def readings(n: int = 24):
    return store.recent(store.conn(), min(n, 500))
