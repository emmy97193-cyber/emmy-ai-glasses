# EMMY AI SERVER - FastAPI Brain for Glasses
# Runs on PythonAnywhere: https://emmy97193.pythonanywhere.com
from fastapi import FastAPI, File, UploadFile
from openai import OpenAI
import base64

app = FastAPI()
client = OpenAI() # Put your API key in .env

@app.post("/ai-glasses/see")
async def see_what_glasses_see(file: UploadFile = File(...)):
    # Get image from ESP32-S3 glasses
    image_data = await file.read()
    b64_image = base64.b64encode(image_data).decode('utf-8')
    
    # Send to GPT-4o Vision - Emmy AI brain
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are Emmy AI, smart glasses assistant from Nigeria. Answer briefly, like talking in someone's ear."},
            {"role": "user", "content": [
                {"type": "text", "text": "What do you see? Tell me in 1 short sentence."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
            ]}
        ],
        max_tokens=100
    )
    answer = response.choices[0].message.content
    print(f"EMMY AI Saw: {answer}")
    return {"emmy_ai_says": answer}

@app.get("/")
def home():
    return {"status": "EMMY AI Glasses Server is LIVE - Bonny, Nigeria!"}
