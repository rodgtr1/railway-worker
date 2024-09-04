from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from rembg import remove
import logging
import os
import glob

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.post("/cleanup")
async def cleanup():
    folder_path = 'images'
    files = glob.glob(os.path.join(folder_path, '*'))

    for file in files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
                print(f"Error deleting {file}: {e}")
    return {"message": "Images cleaned up!"}

@app.post("/removeBackground")
async def removeBackground(thumbnail: UploadFile = File(...)):

    logger.info(f"processing ${thumbnail.filename}")
    try:
        # Ensure the images directory exists
        os.makedirs('images', exist_ok=True)
        logger.info("images folder created")

        name = thumbnail.filename
        input_path = os.path.join('images', name)
        output_path = os.path.join('images', name + '_bgremoved.png')

        # Save the uploaded file content to a temporary file
        with open(input_path, 'wb') as f:
            f.write(await thumbnail.read())
            logger.info("original image saved")

        # Process the file to remove the background
        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                input = i.read()
                output = remove(input)
                o.write(output)
                logger.info("background removed successfully")

        return FileResponse(output_path, media_type='image/png', filename=output_path)
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": "An error occurred while processing the file."}