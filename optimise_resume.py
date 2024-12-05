import os
import openai
import yaml
from helper_lib import read_text_file, write_to_text_file, getPrompt

# Load configuration from Config.yaml
with open('Config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Constants and configurations
OPENAI_API_KEY = os.getenv('OPENAI_DEVKEY')
JOB_POS_FOLDER = config['JOB_POS_FOLDER']
OUTPUT_FOLDER = config['OUTPUT_FOLDER']
RESUME_PATH = config['RESUME_PATH']
LLM_MODEL = config['LLM_MODEL']
LLM_temperature = config['LLM_temperature']

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
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ], 
            temperature=LLM_temperature
        )
        
        # Extract response
        resume = response.choices[0].message.content

        # Write optimized resume to file
        output_file_path = os.path.join(OUTPUT_FOLDER, f'resume-{filename}.md')
        write_to_text_file(output_file_path, resume)

    print(">>> END <<<")

if __name__ == "__main__":
    main()