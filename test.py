from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import mimetypes

app = FastAPI()

class FileCheckResponse(BaseModel):
    is_video: bool
    file_type: str

def is_video(file_type):
    return file_type and file_type.startswith('video')

@app.post("/check_video/")
async def check_video(file: UploadFile = File(...)):
    content_type, _ = mimetypes.guess_type(file.filename)
    file_type = content_type.split('/')[0] if content_type else None
    is_video_file = is_video(file_type)

    response_data = {
        "is_video": is_video_file,
        "file_type": file_type
    }

    response_json = jsonable_encoder(FileCheckResponse(**response_data))
    return JSONResponse(content=response_json)
