import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from src.helpers.splat_helper import SplatHelper

class NoCacheStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs):
        self.cachecontrol = "max-age=0, no-cache, no-store, , must-revalidate"
        self.pragma = "no-cache"
        self.expires = "0"
        super().__init__(*args, **kwargs)

    def file_response(self, *args, **kwargs):
        resp = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        resp.headers.setdefault("Pragma", self.pragma)
        resp.headers.setdefault("Expires", self.expires)
        return resp
    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")

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

    earth_dielectric_constant: int
    earth_conductivity: float


@app.post("/input-data")
async def set_input_data(dt: InputData):
    global input_data
    input_data = dt


@app.post("/upload-files")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Загружает файлы и сохраняет их в third_party/splat/sdf/ с заменой.
    """
    sdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "third_party/splat/sdf")
    os.makedirs(sdf_dir, exist_ok=True)
    # Очищаем директорию перед загрузкой новых файлов
    for f in os.listdir(sdf_dir):
        file_path = os.path.join(sdf_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    for upload in files:
        dest_path = os.path.join(sdf_dir, os.path.basename(upload.filename))
        with open(dest_path, "wb") as out_file:
            content = await upload.read()
            out_file.write(content)
    return {"status": "ok", "files_uploaded": len(files)}


@app.get("/results", response_class=HTMLResponse)
async def read_results(request: Request):
    splat_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "third_party/splat")
    splat_instance = SplatHelper(os.path.join(splat_root, "splat"),
                                 os.path.join(splat_root, "splat-hd"),
                                 working_dir="static/splat",
                                 use_hd=False,
                                 sdf_path=os.path.join(splat_root, "sdf/"))
    global input_data

    # shutil.rmtree("static/splat/*", ignore_errors=True)

    with open("static/splat/tx.qth", "w") as f:
        f.write(f"TX\n{input_data.tx_lat}\n{input_data.tx_lon}\n{input_data.tx_height}")
    
    with open("static/splat/rx.qth", "w") as f:
        f.write(f"RX\n{input_data.rx_lat}\n{input_data.rx_lon}\n{input_data.rx_height}")

    with open("static/splat/splat.lrp", "w") as f:
        f.write(f"{input_data.earth_dielectric_constant}\n")
        f.write(f"{input_data.earth_conductivity}\n")
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

    res_calc_tx_cvrg = splat_instance.calculate_tx_coverage_map(input_data.rx_height)
    print(res_calc_tx_cvrg.stderr, res_calc_tx_cvrg.stdout, res_calc_tx_cvrg.returncode)

    with open("static/splat/splat.lrp", "w") as f:
        f.write(f"{input_data.earth_dielectric_constant}\n")
        f.write(f"{input_data.earth_conductivity}\n")
        f.write(f"{input_data.atmospheric_bending_constant}\n")
        f.write(f"{input_data.frequency}\n")
        f.write(f"{input_data.radioclimate}\n")
        f.write(f"{int(input_data.polarization_type)}\n")
        f.write(f"{input_data.situations_fraction}\n")
        f.write(f"{input_data.time_fraction}\n")
    
    res_calc_tx_loss = splat_instance.calculate_tx_loss_map(input_data.rx_height)
    print(res_calc_tx_loss.stderr, res_calc_tx_loss.stdout, res_calc_tx_loss.returncode)

    res_calc_tx_field = splat_instance.calculate_tx_field_map(input_data.rx_height, input_data.erp)
    print(res_calc_tx_field.stderr, res_calc_tx_field.stdout, res_calc_tx_field.returncode)

    return templates.TemplateResponse("results.html", {"request": request})