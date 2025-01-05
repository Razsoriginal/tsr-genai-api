### To Do:

- stream response for all ai endpoints
- try this thing in a notebook first and then update it here


Use this method to speed up uploads
print(f"File uploaded: {file_name}")

model = genai.GenerativeModel("gemini-1.5-flash")
result = model.generate_content([myfile, "Describe this audio clip"])

for chunk in result:
        print(chunk.text, end="")

### if you want to delete file
myfile.delete()