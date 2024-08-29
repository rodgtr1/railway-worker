from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from rembg import remove

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.post("/removeBackground")
async def removeBackground(file: UploadFile = File(...)):
    # Ensure the images directory exists
    os.makedirs('images', exist_ok=True)

    name = file.filename
    input_path = os.path.join('images', name)
    output_path = os.path.join('images', name + '_bgremoved.png')

    # Save the uploaded file content to a temporary file
    with open(input_path, 'wb') as f:
        f.write(await file.read())

    # Process the file to remove the background
    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            o.write(output)

    return FileResponse(output_path, media_type='image/png', filename=output_path)