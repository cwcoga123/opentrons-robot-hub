from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="hub/templates")
router = APIRouter()

robot_data = {
    "id": "robot-001",
    "name": "robot-001",
    "status": "online",
    "last_seen_at": "just now",
    "agent_version": "0.1.0"
}

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "robot": robot_data})

@router.post("/upload-protocol")
async def upload_protocol(protocolFile: UploadFile):
    return RedirectResponse("/", status_code=302)

@router.post("/start-run")
async def start_run(protocol_id: str = Form(...)):
    return RedirectResponse("/", status_code=302)
