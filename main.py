import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ddddocr

app = FastAPI()
ocr = ddddocr.DdddOcr()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict_captcha(file: UploadFile = File(None), base64_image: str = None):
    try:
        if file:
            contents = await file.read()
        elif base64_image:
            try:
                contents = base64.b64decode(base64_image)
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid Base64 image")
        else:
            raise HTTPException(status_code=400, detail="No file or Base64 image provided")

        result = ocr.classification(contents)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}