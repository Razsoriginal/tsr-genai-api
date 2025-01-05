import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from app.config import Config
from app.utils.prompts import article_format, ref_format, transcribe_format

try:
  genai.configure(api_key=Config.VERTEX_API_KEY)
except Exception as e:
  print(f"An error occurred during configuration: {e}")
  raise  

model = genai.GenerativeModel('models/gemini-2.0-flash-exp')

def genai_custom(prompt, config=None, audio_path=None):

  safety_config = {
      HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
  }

  generation_config = genai.GenerationConfig(
      response_mime_type="text/plain", response_schema=None
  )

  if config:
    if config == "article-json":
      generation_config = genai.GenerationConfig(
          response_mime_type="application/json",
          response_schema=article_format
      )
    elif config == "article-html":
      generation_config = genai.GenerationConfig(
          response_mime_type="text/plain",
          response_schema=None
      )
    elif config == "references":
      generation_config = genai.GenerationConfig(
          response_mime_type="application/json",
          response_schema=ref_format
      )

  contents = [prompt]
  if audio_path:
    with open(audio_path, "rb") as audio_file:
      audio_bytes = audio_file.read()
    contents.append({
        "mime_type": "audio/mp3",
        "data": audio_bytes,
    })

  try:
    return model.generate_content(
        contents=contents,
        safety_settings=safety_config,
        generation_config=generation_config
    ).to_dict()
  except Exception as e:
    print(f"An error occurred during generation: {e}")
    return None