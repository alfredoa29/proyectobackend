from fastapi import FastAPI, Request

from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import psutil_test as psutil_test
import database_model as database_model
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
origins = [
  #no se estan usando
    "http://localhost:8080",
    "http://localhost:4200"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






@app.get("/")
async def dashboard(request: Request):
    cpu_usage = [10, 15, 20, 25]  # Simulación de datos para el ejemplo
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "cpu_usage": cpu_usage
    })


@app.get("/v0/version")
async def version():
    return {"version": app.version}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/cpu-usage")
async def cpu_usage():
    cpu_percent = psutil_test.generate_cpu_usage()
    return JSONResponse(content={"CPU Usage": cpu_percent})

@app.get("/ram-usage")
async def ram_usage():
    ram_percent = psutil_test.generate_ram_usage()
    return JSONResponse(content={"RAM Usage": ram_percent})

@app.get("/tablespace")
async def tablespace():
    tablespace = database_model.tablespace_usage()
    return JSONResponse(content={"Tablespace Info": tablespace})

@app.get("/swapmemory")
async def swapmemory():
    swapmemory = psutil_test.generate_swap_usage()
    return {"message": swapmemory}

@app.get("/coneactivas")
async def cone_activas():
    coneactivas = database_model.conexiones_activas()
    return {"message": coneactivas}


@app.get("/backups")
async def backups():
    backups = database_model.estado_backups()
    return {"message": backups}

@app.get("/tablespaces")
async def  tablespaces():
    tablespaces = database_model.estado_tablespaces()
    return {"message": tablespaces}


@app.get("/alertas")
async def alertas():
    alerts = database_model.alertas_eventos_criticos()
    return {"message": alerts}

@app.get("/discos")
async def disco():
    disco = database_model.monitoreo_lectua_escritura_disco()
    return {"message": disco}
