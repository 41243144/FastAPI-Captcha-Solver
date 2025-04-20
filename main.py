from fastapi import FastAPI, UploadFile, File
from fastapi import FastAPI
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
async def predict_captcha(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = ocr.classification(contents)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
