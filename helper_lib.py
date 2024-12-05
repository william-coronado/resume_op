def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except IOError:
        print(f"Error: An I/O error occurred while reading the file {file_path}.")

def write_to_text_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError:
        print(f"Error: An I/O error occurred while writing to the file {file_path}.")

def getPrompt(md_resume, job_description):
    prompt = f"""
    I have a resume formatted in Markdown and a job description. \
    Please adapt my resume to better align with the job requirements while \
    maintaining a professional tone. Tailor my skills, experiences, and \
    achievements to highlight the most relevant points for the position. \
    Ensure that my resume still reflects my unique qualifications and strengths \
    but emphasizes the skills and experiences that match the job description.

    ### Here is my resume in Markdown:
    {md_resume}

    ### Here is the job description:
    {job_description}

    Please modify the resume to:
    - Use keywords and phrases from the job description.
    - Adjust the bullet points under each role to emphasize relevant skills and achievements.
    - Make sure my experiences are presented in a way that matches the required qualifications.
    - Maintain clarity, conciseness, and professionalism throughout.

    Return the updated resume in Markdown format.
    """
    
    return prompt