from fastapi import FastAPI, UploadFile, File
import ddddocr

app = FastAPI()
ocr = ddddocr.DdddOcr()

@app.post("/predict")
async def predict_captcha(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = ocr.classification(contents)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
