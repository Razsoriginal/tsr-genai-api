import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import Config

genai.configure(api_key=Config.VERTEX_API_KEY)

model = genai.GenerativeModel('models/gemini-2.0-flash-exp')

def genai_custom(prompt, audio_path=None): 
    try:
        safety_config = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }

        if audio_path is None:
            return model.generate_content(
                contents=[prompt],
                safety_settings=safety_config,
            ).to_dict()

        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        return model.generate_content(
            contents=[
                prompt,
                {
                    "mime_type": "audio/mp3",
                    "data": audio_bytes,
                },
            ],
            safety_settings=safety_config
        ).to_dict()

    except Exception as e:
        print(f"An error occurred: {e}")