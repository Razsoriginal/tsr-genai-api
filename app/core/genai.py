import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import Config
from app.utils.prompts import article_format, ref_format, transcribe_format

genai.configure(api_key=Config.VERTEX_API_KEY)

model = genai.GenerativeModel('models/gemini-2.0-flash-exp')

def genai_custom(prompt, config=None, audio_path=None, model=model): 
    try:
        safety_config = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }

        generation_config = genai.GenerationConfig(
            response_mime_type="text/plain", response_schema=None
        )

        if config == "article-json":
            generation_config = genai.GenerationConfig(
            response_mime_type="application/json", 
            response_schema=article_format
            )
        elif config == "article-html":
            generation_config = genai.GenerationConfig(
                response_mime_type="text/html",
                response_schema=None  
            )
        elif config == "references":
            generation_config = genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=ref_format
            )
        elif config == "transcribe":
            generation_config = genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=transcribe_format
            )

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
            safety_settings=safety_config,
            generation_config=generation_config
        ).to_dict()

    except Exception as e:
        print(f"An error occurred: {e}")