from fastapi.responses import StreamingResponse
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
def upload_and_clean(data: dict = Body(...)):
    try:
        # Validación adicional del nombre de archivo
        if not data.filename or "/" in data.filename or ".." in data.filename:
            raise HTTPException(
                status_code=400,
                detail="Nombre de archivo inválido o potencial path traversal"
            )

        # Decodificar contenido base64
        try:
            file_data = base64.b64decode(data.file_content)
        except (base64.binascii.Error, TypeError):
            raise HTTPException(
                status_code=400,
                detail="Contenido de archivo no válido (debe ser base64 válido)"
            )

        # Construir ruta segura
        file_path = os.path.join("data", data.filename)
        
        # Guardar archivo
        with open(file_path, "wb") as f:
            f.write(file_data)

        # === Aquí iría tu lógica de limpieza/processing ===
        # Por ejemplo:
        # 1. Limpiar metadatos
        # 2. Verificar tipo de archivo
        # 3. Escanear virus
        # 4. Procesamiento específico
        # clean_file(file_path)
        
        return {
            "status": "success",
            "message": "Archivo guardado y procesado perris no me la conteis",
            "filename": data.filename,
            "file_size": len(file_data),
            "clean_operations": []  # Puedes añadir detalles del cleaning
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail=f"Error interno procesando el archivo: {str(e)}"
        )