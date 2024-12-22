import google.generativeai as genai
from app.config import Config

genai.configure(api_key=Config.VERTEX_API_KEY)

model = genai.GenerativeModel('models/gemini-1.5-flash')

def genai_custom(prompt, audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        response = model.generate_content([
            prompt,
            {
                "mime_type": "audio/mp3",
                "data": audio_bytes
            }
        ])

        return response.to_dict()

    except Exception as e:
        print(f"An error occurred: {e}")