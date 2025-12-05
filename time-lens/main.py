from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Literal
import random

app = FastAPI(title="Time Lens – Life-Year Model v3")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


#   life year model
#   1 day = 1 life-year
#   1 hour = 1 life-month
#   1 minute = 1 life-day
#   1 second = 1 life-hour


UNIT_TO_SECONDS = {
    "seconds": 1,
    "minutes": 60,
    "hours": 3600,
    "days": 86400,
}

class TimeInput(BaseModel):
    value: float
    unit: Literal["seconds", "minutes", "hours", "days"]



def convert_to_life_model(value, unit):
    seconds = value * UNIT_TO_SECONDS[unit]

    return {
        "life_hours": round(seconds / 1, 2),
        "life_days": round(seconds / 60, 2),
        "life_months": round(seconds / 3600, 2),
        "life_years": round(seconds / 86400, 4),
    }


def generate_suggestion(model):
    d = model["life_days"]
    m = model["life_months"]
    y = model["life_years"]

    # Master suggestions bank
    base = []

    if d < 1:
        base = [
            {
                "window": "Micro Evolution Window",
                "why": "Small pockets of time control long-term identity direction.",
                "actions": [
                    "Fix one friction point in your setup or environment.",
                    "Reflect on one belief you want to strengthen.",
                    "Learn one microscopic insight that sharpens your thinking."
                ],
                "deep": "Identity changes begin in micro-moments — not dramatic events.",
                "warning": "If you waste this micro-day, your future self becomes 0.001% duller.",
                "become": "Someone who respects even the smallest window of life."
            }
        ]

    elif d < 10:
        base = [
            {
                "window": "Momentum Day Block",
                "why": "Day-sized pushes compound into unstoppable acceleration.",
                "actions": [
                    "Do one meaningful task even in small depth.",
                    "Advance one personal project by 1%.",
                    "Write or create something that improves your clarity."
                ],
                "deep": "Momentum is built by consistent nudges, not heroic effort.",
                "warning": "If you skip this block, your mind loses momentum and clarity.",
                "become": "A person who uses time like a sculptor — shaping outcomes day by day."
            }
        ]

    elif m < 6:
        base = [
            {
                "window": "Growth Month Window",
                "why": "A single hour here equals a life-month — that’s huge.",
                "actions": [
                    "Enter a deep work session (no interruptions).",
                    "Learn a concept deeply enough to teach it.",
                    "Create something meaningful: feature, chapter, logic, design."
                ],
                "deep": "Depth compresses progress. Shallow work stretches suffering.",
                "warning": "Wasting this means losing a full life-month of potential.",
                "become": "Someone capable of producing high-value work predictably."
            }
        ]

    else:
        base = [
            {
                "window": "Life-Year Transformation Window",
                "why": "A real day = a life-year in your world — identity-level opportunity.",
                "actions": [
                    "Design your identity for this 'year'.",
                    "Set one meaningful theme: mastery, discipline, clarity, creation.",
                    "Build a long-term project piece that shapes your future."
                ],
                "deep": "Transformation happens in focused cycles, not random attempts.",
                "warning": "Wasting this means your 'year' achieves nothing.",
                "become": "A person who evolves deliberately instead of accidentally drifting."
            }
        ]

    chosen = random.choice(base)

    return {
        "window": chosen["window"],
        "why": chosen["why"],
        "action_list": chosen["actions"],
        "deep": chosen["deep"],
        "warning": chosen["warning"],
        "become": chosen["become"]
    }




@app.post("/convert")
async def convert(data: TimeInput):
    model = convert_to_life_model(data.value, data.unit)
    sug = generate_suggestion(model)

    return {
        "input": f"{data.value} {data.unit}",
        "life_days": model["life_days"],
        "life_months": model["life_months"],
        "life_years": model["life_years"],
        "window": sug["window"],
        "why": sug["why"],
        "actions": sug["action_list"],
        "deep": sug["deep"],
        "warning": sug["warning"],
        "become": sug["become"]
    }



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
