import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
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

@app.api_route("/", methods=["GET", "HEAD"])
async def root(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content=None, status_code=200)
    return {"message": "the server is running"}

@app.post("/predict")
async def predict_captcha(file: UploadFile = File(None), base64_image: str = Form(None)):
    try:
        if file:
            print("接收到檔案類型的圖片")
            contents = await file.read()
        elif base64_image:
            print("接收到 Base64 類型的圖片")
            try:
                contents = base64.b64decode(base64_image)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid Base64 image: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail="No file or Base64 image provided")

        if not contents:
            raise HTTPException(status_code=400, detail="Empty image data")

        try:
            result = ocr.classification(contents)
            return {"result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

    except HTTPException as http_err:
        return {"error": http_err.detail}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}