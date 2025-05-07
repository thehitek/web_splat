from ast import In
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request

from src.helpers.splat_helper import SplatHelper

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("start.html", {"request": request})

class InputData(BaseModel):
    tx_lat: float
    tx_lon: float
    tx_height: int

    rx_lat: float
    rx_lon: float
    rx_height: int

    power: float
    frequency: int
    
    polarization_type: bool # True for vertical, False for horizontal
    
    situations_fraction: float
    time_fraction: float

    radioclimate: int
    atmospheric_bending_constant: float

global input_data
input_data: InputData = InputData(
    tx_lat=59.973858,
    tx_lon=30.316145,
    tx_height=50,
    rx_lat=59.902639,
    rx_lon=30.479671,
    rx_height=50,
    power=10.0,
    frequency=2400,
    polarization_type=False,
    situations_fraction=0.5,
    time_fraction=0.5,
    radioclimate=5,
    atmospheric_bending_constant=300.0)

@app.post("/input-data")
async def set_input_data(dt: InputData):
    global input_data
    input_data = dt

@app.get("/results", response_class=HTMLResponse)
async def read_results(request: Request):
    splat_instance = SplatHelper("./third_party/splat/splat", 
                                 "./third_party/splat/splat-hd", 
                                 use_hd=False)
    global input_data

    with open("third_party/splat/tx.qth", "w") as f:
        f.write(f"TX\n{input_data.tx_lat}\n{input_data.tx_lon}\n{input_data.tx_height}")
    
    with open("third_party/splat/rx.qth", "w") as f:
        f.write(f"RX\n{input_data.rx_lat}\n{input_data.rx_lon}\n{input_data.rx_height}")

    res = splat_instance.calculate_kml(
        "third_party/splat/tx.qth",
        "third_party/splat/rx.qth"
    )
    print(res.stderr, res.stdout, res.returncode)
    
    return templates.TemplateResponse("results.html", {"request": request})