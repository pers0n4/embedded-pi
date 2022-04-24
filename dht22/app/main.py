import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel, create_engine, desc

from .models import Record
from .scheduler import Scheduler

logger = logging.getLogger("fastapi")

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}, echo=True
)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, session: Session = Depends(get_session)):
    records = session.query(Record).order_by(desc(Record.id)).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "records": records,
        },
    )


@app.on_event("startup")
async def startup_event():
    SQLModel.metadata.create_all(bind=engine)
    try:
        scheduler = Scheduler(engine)
        scheduler.start()
    except Exception as error:
        logger.debug(str(error))
