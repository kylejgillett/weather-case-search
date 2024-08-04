from fastapi import FastAPI

from weather_cases.lifecycle import lifespan, case_registry
from weather_cases.models import WeatherCase

app = FastAPI(lifespan=lifespan)


@app.get("/cases/search/")
def search_cases(q: str, limit: int) -> list[WeatherCase]:
    items = case_registry.search(q, limit=limit)
    sorted_items = sorted(items, key=_sort_by_score_and_date, reverse=True)
    return [case for case, _ in sorted_items]


def _sort_by_score_and_date(item):
    case, score = item
    return score, case.datetime
