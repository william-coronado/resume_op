import os
from openai import OpenAI
import yaml
from helper_lib import read_text_file, write_to_text_file, getPrompt

# Load configuration from Config.yaml
try:
    with open('Config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    print("Error: Config.yaml file not found.")
    exit(1)
except yaml.YAMLError as e:
    print(f"Error: An error occurred while parsing Config.yaml: {e}")
    exit(1)

# Constants and configurations
OPENAI_API_KEY = config.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
if OPENAI_API_KEY is None:
    print("Error: OpenAI API key not found. Please set it in Config.yaml or as an environment variable 'OPENAI_API_KEY'.")
    exit(1)
client = OpenAI(api_key=OPENAI_API_KEY)

JOB_POS_FOLDER = config['JOB_POS_FOLDER']
OUTPUT_FOLDER = config['OUTPUT_FOLDER']
RESUME_PATH = config['RESUME_PATH']
LLM_MODEL = config['LLM_MODEL']
LLM_temperature = config['LLM_temperature']

def sendLLMRequest(prompt):
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=LLM_temperature
        )
    except Exception as e:
            print(f"An unexpected error occurred while calling openai.chat.completions.create(): {e}")
            return
    
    return response.choices[0].message.content  
def main():
    # Read original resume
    md_resume = read_text_file(RESUME_PATH)
    if md_resume is None:
            print("Error: Failed to read the resume.")
            return

    # List job description files
    try:
        dir_list = os.listdir(JOB_POS_FOLDER)
    except FileNotFoundError:
        print(f"Error: The directory {JOB_POS_FOLDER} was not found.")
        return
    except IOError:
        print(f"Error: An I/O error occurred while accessing the directory {JOB_POS_FOLDER}.")
        return
    
    print(">>> START <<<")
    for filename in dir_list:
        print(f"Processing {filename}")

        # Read job description
        job_description = read_text_file(os.path.join(JOB_POS_FOLDER, filename))
        if job_description is None:
                print(f"Error: Failed to read the job description file {filename}.")
                return
            
        prompt = getPrompt(md_resume, job_description)

        resume = sendLLMRequest(prompt)

        # Write optimized resume to file
        output_file_path = os.path.join(OUTPUT_FOLDER, f'resume-{filename}.md')
        write_to_text_file(output_file_path, resume)

    print(">>> END <<<")

if __name__ == "__main__":
    main()