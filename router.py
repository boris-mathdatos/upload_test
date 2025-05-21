from fastapi.responses import StreamingResponse
from fastapi import UploadFile, File
from fastapi import (APIRouter,
                     Body,
                     Depends,
                     Header)
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import subprocess

import os
import base64

router = APIRouter()

@router.post("/subida_testaaaaaaaaaa")
async def chat(data: dict = Body(...), header: str = Header(default = "default")):

    ruta_del_ssh = "C:/Users/boris.prieto/Desktop/produccion/subida"
    archivo_ejecutar = "/test.sh"

    command_to_run = ["bash", ruta_del_ssh + archivo_ejecutar]

    # print(subprocess.run(
    #     command_to_run,
    #     text = True,
    #     check = False,
    #     timeout = 60
    # ))
    
    # return JSONResponse(
    #         content = {"response": "Error en la funcion de formateo."},
    #         status_code = 400
    #     )

# Crear directorio si no existe
os.makedirs("data", exist_ok=True)

@router.post("/uploads_and_clean")
async def upload_and_clean(file: UploadFile = File(...)):
    try:
        # Validación adicional del nombre de archivo
        if not file.filename or "/" in file.filename or ".." in file.filename:
            raise HTTPException(
                status_code=400,
                detail="Nombre de archivo inválido o potencial path traversal"
            )

        
        
        file_data = await file.read()
        
        # Guardar archivo
        
        file_path = os.path.join("data", file.filename)
        with open(file_path, "wb") as f:
            f.write(file_data)

        # ... (lógica de procesamiento)
        
        return {
            "status": "success",
            "filename": file.filename,
            "file_size": len(file_data)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))# Guardar archivo
        

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail=f"Error interno procesando el archivo: {str(e)}"
        )