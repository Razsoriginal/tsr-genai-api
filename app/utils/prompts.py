transcribe_format = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
            },
        },
        "required": ["text"],
    },
}

article_html_prompt = """
You are a web developer skilled in converting JSON data into HTML for a web blog. Below is the JSON data containing an article with attributes. Generate a well-structured HTML format for a web blog based on the provided JSON data.

Requirements:
The HTML should include a <header>, <main>, and <footer> structure.
Ensure the title of the article is styled prominently within an <h1> tag.
Render any metadata like author, date, or tags in an organized manner (e.g., in a <div> with class metadata).
Ensure a clean and responsive layout using basic inline CSS or Bootstrap classes.
Use appropriate HTML tags for the article content:
  Headings (<h2>, <h3>).
  Video (<video>).
  Paragraphs (<p>).
  Lists (<ul>, <ol>).
  Hyperlinks (<a>).

yotube_url: {video_url}
JSON Data: {article_json}

Desired Output:
Generate the HTML using the structure mentioned above and ensure it renders the article in a web-friendly layout.
Ensure all content is semantic and visually appealing for a blog.
"""


ref_format = {
    "type": "object",
    "properties": {
        "references": {
            "type": "object",
            "properties": {
                "hadiths": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "reference": {"type": "string"},
                            "text": {"type": "string"}
                        },
                        "required": ["reference", "text"]
                    }
                },
                "quranic_verses": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "surah_name": {"type": "string"},
                            "verse_number": {"type": "string"},
                            "text": {"type": "string"}
                        },
                        "required": ["surah_name", "verse_number", "text"]
                    }
                }
            },
            "required": ["hadiths", "quranic_verses"]
        }
    },
    "required": ["references"]
}

ref_prompt = """
  Please extract all Islamic references mentioned in the video at the following URL: '{video_url}'. 
  Don't include any external sources or references not mentioned in the video. Nor search online for any additional references.
  Specifically, identify and provide the complete references for:

  Hadiths: Include the full book name, volume, page number, and Hadith number wherever possible.
  Quranic Verses: Provide the Surah name and verse number.
  Ensure accuracy and completeness in the references. 

"""

article_format = {
    "type": "object",
    "properties": {
        "blog_post": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {
                    "type": "object",
                    "properties": {
                        "introduction": {"type": "string"},
                        "key_takeaways": {
                            "type": "array",
                            "items":  {"type": "string"}
                        },
                        "deep_dive": {"type": "string"},
                        "benefits_and_applications": {"type": "string"},
                        "quranic_and_hadith_references": {
                            "type": "object",
                            "properties": {
                                "hadiths": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "reference": {"type": "string"},
                                            "text": {"type": "string"}
                                        },
                                        "required": ["reference", "text"]
                                    }
                                },
                                "quranic_verses": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "surah_name": {"type": "string"},
                                            "verse_number": {"type": "string"},
                                            "text": {"type": "string"}
                                        },
                                        "required": ["surah_name", "verse_number", "text"]
                                    }
                                }
                            },
                           "required":["hadiths","quranic_verses"]
                        },
                        "conclusion": {"type": "string"},
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "additional_resources": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["introduction", "key_takeaways", "deep_dive", "benefits_and_applications", "conclusion", "keywords", "additional_resources"]
                }
            },
            "required": ["title", "content"]
        }
    },
    "required": ["blog_post"]
}

sys_prompt = """ 

  You are an expert AI assistant specialized in creating comprehensive and professional blog articles from YouTube videos. Based on the provided video title, link, transcription, and summary, your task is to craft a polished and detailed blog article. 

  **Input Details:**  
  - **Video Title:** {yt_title}  
  - **Video Link:** {video_url}  
  - **Video Transcription:** {transcription_genai}  

  ### **Guidelines for Writing:**

  1. **Detailed Analysis:** Go beyond summarizing the video. Extract every meaningful insight, example, and explanation from the transcript to create an in-depth article. Ensure no significant detail is missed. 

  2. **Hadiths and Quranic Verses:** Identify and include any Islamic Hadiths or Quranic verses mentioned in the video. Provide their full references, including:  
    - For Hadiths: Book name, volume, page number, and Hadith number.  
    - For Quranic verses: Surah name and verse number(s).  
    Incorporate them into the article wherever relevant to support or enhance the content.

  3. **Enrich with Context:** Add context where necessary to ensure the reader understands the broader implications or background of the content.  

  4. **Professional and Engaging Tone:** Write in a professional tone, but keep the language engaging and easy to read. Avoid overly technical jargon unless the target audience demands it.  

  5. **Refined Structure:**  
    - Start with a captivating **introduction** summarizing the article's focus and why it is valuable.  
    - Use well-organized **headings and subheadings** to break the content into digestible sections.  
    - Provide a concise **conclusion** summarizing the key takeaways.  

  6. **Originality and Value:** Reorganize and synthesize information creatively to deliver new value. Do not rephrase the transcript verbatim.  

  7. **Actionable Insights:** Highlight actionable takeaways, practical advice, or key lessons where applicable.  

  8. **SEO Optimization:**  
    - Identify and incorporate keywords related to the topic.  
    - Use headings, subheadings, and meta-descriptions optimized for search engines.  

  9. **Call to Action:** Encourage readers to explore further (e.g., watch the video, engage with related resources, subscribe to the channel).  

  10. **Interactive Elements:** Suggest including visuals, infographics, or bullet points for key concepts to improve readability.  

  Return the article without any explnation.
"""