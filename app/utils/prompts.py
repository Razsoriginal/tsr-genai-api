ref_out = {
    "references": {
      "hadiths": [
        {
          "book_name": "str",      
          "volume": "int",        
          "page": "int",        
          "hadith_number": "int", 
          "text": "str"            
        }
      ],
      "quranic_verses": [
        {
          "surah_name": "str",     
          "verse_number": "str",   
          "text": "str"          
        }
      ]
    }
  }

ref_prompt = """
  Please extract all Islamic references from the video at the following URL: '{video_url}'. 
  Don't include any external sources or references not mentioned in the video. Nor search online for any additional references.
  Specifically, identify and provide the complete references for:

  Hadiths: Include the full book name, volume, page number, and Hadith number wherever possible.
  Quranic Verses: Provide the Surah name and verse number.
  Ensure accuracy and completeness in the references. 
  
  References: {ref_out}
  return: References
"""


article_format = {
    "blog_post": {
      "title": "str",
      "content": {
        "introduction": "str",
        "key_takeaways": [
          "str"
        ],
        "deep_dive": "str",
        "benefits_and_applications": "str",
        "quranic_and_hadith_references": {
          "hadiths": [
            {
              "book_name": "str",        
              "volume": "int",         
              "page": "int",          
              "hadith_number": "int",  
              "text": "str"            
            }
          ],
          "quranic_verses": [
            {
              "surah_name": "str",    
              "verse_number": "str",    
              "text": "str"            
            }
          ]
        },
        "conclusion": "str",
        "keywords": [
          "str"
        ],
        "additional_resources": [
          "str"
        ]
      }
    }
  }

sys_prompt = """ 

  You are an expert AI assistant specialized in creating comprehensive and professional blog articles from YouTube videos. Based on the provided video title, link, transcription, and summary, your task is to craft a polished and detailed blog article. 

  **Input Details:**  
  - **Video Title:** {yt_title}  
  - **Video Link:** {video_url}  
  - **Video Transcription:** {transcription_genai}  
  - **References:** {references_genai}
  - **Video Summary:** {summary_genai}  

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

  Use this JSON schema:

  Article = {article_format}
  Return: Article
"""