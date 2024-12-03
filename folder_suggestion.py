import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import os

def suggest_top_folders(filename):
    # Load the folder structure from file_structure.txt
    with open("file_structure.txt", 'r') as f:
        folder_structure = [line.strip() for line in f if line.strip()]

    # Create a prompt to suggest folders based on the filename and available folders
    prompt = (
        "Given the filename '{filename}', suggest the top 10 folders from the following list: {folders}.\n"  # Changed to top 10
        "Provide only the JSON output with folder names and confidence percentages, without any additional text.\n"
        "Do not include codeblocks or language 'json' in the output."
    )
    
    example_output = (
        r"\nExample output:\n"
        r"[{'folderName': 'Folder1', 'confidencePercentage': 92}, "
        r"{'folderName': 'Folder2', 'confidencePercentage': 85}, "
        r"{'folderName': 'Folder3', 'confidencePercentage': 72}]"
    )
    
    full_prompt = prompt.format(filename=os.path.basename(filename), folders=', '.join(folder_structure)) + example_output
    
    model = OllamaLLM(model="qwen2.5:3b", temperature=0.2, context_length=32768)
    response = model.invoke(full_prompt)
    
    # Parse the response to extract folder suggestions and confidence
    suggestions = parse_suggestions(response)
    return suggestions

def parse_suggestions(response):
    # Strip backticks and 'json' from the response
    response = response.strip("```").replace("json", "").strip()
    
    # Parse the JSON response from the model to extract folder suggestions and confidence
    try:
        # Convert the string representation of the list to a Python object
        data = eval(response) #Use json.loads instead of eval
        if isinstance(data, list):  # Check if data is a list
            suggestions = [(item['folderName'], item['confidencePercentage']) for item in data]
            return suggestions[:10]  # Return top 10 suggestions
        else:
            return []  # Return an empty list if data is not in expected format
    except (json.JSONDecodeError, KeyError):
        return []  # Return an empty list if parsing fails
