import os
import openai
from helper_lib import read_text_file, write_to_text_file, getPrompt

# Constants and configurations
OPENAI_API_KEY = os.getenv('OPENAI_DEVKEY')
JOB_POS_FOLDER = './input/'
OUTPUT_FOLDER = './output'
RESUME_PATH = './william-resume.md'

def main():
    # Set OpenAI API key
    openai.api_key = OPENAI_API_KEY

    # Read original resume
    md_resume = read_text_file(RESUME_PATH)

    # List job description files
    dir_list = os.listdir(JOB_POS_FOLDER)
    print(">>> START <<<")
    for filename in dir_list:
        print(f"Processing {filename}")

        # Read job description
        job_description = read_text_file(os.path.join(JOB_POS_FOLDER, filename))
        prompt = getPrompt(md_resume, job_description)

        # Make API call
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ], 
            temperature=0.25
        )
        
        # Extract response
        resume = response.choices[0].message.content

        # Write optimized resume to file
        output_file_path = os.path.join(OUTPUT_FOLDER, f'resume-{filename}.md')
        write_to_text_file(output_file_path, resume)

    print(">>> END <<<")

if __name__ == "__main__":
    main()