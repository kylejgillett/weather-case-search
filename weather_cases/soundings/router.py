from fastapi import APIRouter, HTTPException
import requests

from weather_cases.soundings.models import Profile


router = APIRouter(prefix="/soundings", tags=["soundings"])

BUCKET_BASE_URL = "https://chase-archive-soundings.nyc3.cdn.digitaloceanspaces.com"


@router.get("/{case_id}")
def get_sounding(case_id: str) -> Profile:
    url = f"{BUCKET_BASE_URL}/{case_id}.json"
    resp = requests.get(url)
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Sounding not found")
    elif resp.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching sounding")

    data = resp.json()
    return Profile(**data)
