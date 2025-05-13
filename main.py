import os
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

    erp: float
    frequency: int
    
    polarization_type: bool # True for vertical, False for horizontal
    
    situations_fraction: float
    time_fraction: float

    radioclimate: int
    atmospheric_bending_constant: float

@app.post("/input-data")
async def set_input_data(dt: InputData):
    global input_data
    input_data = dt

@app.get("/results", response_class=HTMLResponse)
async def read_results(request: Request):
    splat_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "third_party/splat")
    splat_instance = SplatHelper(os.path.join(splat_root, "splat"),
                                 os.path.join(splat_root, "splat-hd"),
                                 working_dir="static/splat",
                                 use_hd=False,
                                 sdf_path=os.path.join(splat_root, "sdf/"))
    global input_data

    with open("static/splat/tx.qth", "w") as f:
        f.write(f"TX\n{input_data.tx_lat}\n{input_data.tx_lon}\n{input_data.tx_height}")
    
    with open("static/splat/rx.qth", "w") as f:
        f.write(f"RX\n{input_data.rx_lat}\n{input_data.rx_lon}\n{input_data.rx_height}")

    with open("static/splat/splat.lrp", "w") as f:
        f.write("5\n")
        f.write("0.001\n")
        f.write(f"{input_data.atmospheric_bending_constant}\n")
        f.write(f"{input_data.frequency}\n")
        f.write(f"{input_data.radioclimate}\n")
        f.write(f"{int(input_data.polarization_type)}\n")
        f.write(f"{input_data.situations_fraction}\n")
        f.write(f"{input_data.time_fraction}\n")
        f.write(f"{input_data.erp}")

    res_calc_kml = splat_instance.calculate_kml()
    print(res_calc_kml.stderr, res_calc_kml.stdout, res_calc_kml.returncode)
    
    res_calc_trn = splat_instance.calculate_terrain_profile()
    print(res_calc_trn.stderr, res_calc_trn.stdout, res_calc_trn.returncode)
    
    res_calc_elev = splat_instance.calculate_elevation_profile()
    print(res_calc_elev.stderr, res_calc_elev.stdout, res_calc_elev.returncode)

    res_calc_hgt = splat_instance.calculate_height_profile()
    print(res_calc_hgt.stderr, res_calc_hgt.stdout, res_calc_hgt.returncode)

    res_calc_hgt_norm = splat_instance.calculate_height_profile_norm()
    print(res_calc_hgt_norm.stderr, res_calc_hgt_norm.stdout, res_calc_hgt_norm.returncode)

    res_calc_path_loss = splat_instance.calculate_path_loss_profile()
    print(res_calc_path_loss.stderr, res_calc_path_loss.stdout, res_calc_path_loss.returncode)

    res_calc_tx_rx_line_map = splat_instance.calculate_tx_rx_line_map()
    print(res_calc_tx_rx_line_map.stderr, res_calc_tx_rx_line_map.stdout, res_calc_tx_rx_line_map.returncode)

    res_calc_tx_cvrg = splat_instance.calculate_tx_coverage_map(25)
    print(res_calc_tx_cvrg.stderr, res_calc_tx_cvrg.stdout, res_calc_tx_cvrg.returncode)

    return templates.TemplateResponse("results.html", {"request": request})