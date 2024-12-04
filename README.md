# Resume Optimizer

## Purpose
This project was designed to tailor a resume for a given job description.
The main scrips reads an original resume and multiple job descriptions, uses OpenAI's GPT model to tailor the resume for each job description, and saves the optimized resumes to an output folder. The helper functions facilitate reading and writing files and generating the prompt for the AI.

## Detail
Here's a detailed breakdown of what the script and associated library functions do:

### optimise_resume.py

1. **Imports and Setup**:
    - Imports necessary modules: *os* for file operations and *openai* for interacting with the OpenAI API.
    - Imports helper functions from **helper_lib.py**
2. **API Key Setup**:
    - Retrieves the OpenAI API key from an environment variable `OPENAI_DEVKEY` and sets it for use with the OpenAI API.
3. **Folder and File Paths**:
    - Defines the folder paths for job descriptions (`job_pos_folder`) and output resumes (`output_folder`).
    - Specifies the path to the original resume in Markdown format (`resume_path`).
4. **Read Original Resume**:
    - Reads the content of the original resume file using the ***read_text_file()*** function from **helper_lib.py**
5. **Process Job Descriptions**:
    - Lists all files in the job descriptions folder (`job_pos_folder`).
    - Iterates over each file in the folder:
        - Reads the job description from the file.
        - Generates a prompt by combining the resume and job description using the ***getPrompt()*** function from **helper_lib.py**
6. **Generate Optimized Resume**:
    - Makes an API call to OpenAI's GPT model with the generated prompt.
    - Extracts the optimized resume from the API response.
7. **Write Optimized Resume**:
    - Writes the optimized resume to a new file in the output folder, naming it based on the job description file name.
8. **Print Start and End Messages**:
    - Prints messages to indicate the start and end of the process.

### helper_lib.py
1. **`read_text_file(file_path)`**:
    - Reads the content of a text file specified by `file_path` and returns it as a string.

2. **`write_to_text_file(file_path, content)`**:
    - Writes the given content to a text file specified by `file_path`

3. **`getPrompt(md_resume, job_description)`**:
    - Generates a prompt string for the OpenAI API by combining the Markdown resume (*md_resume*) and the job description (`job_description`).
    - The prompt instructs the AI to adapt the resume to better align with the job description while maintaining a professional tone and emphasizing relevant skills and experiences.
