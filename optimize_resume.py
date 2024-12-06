import os
import openai
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

        # Make API call
        try:
            response = openai.ChatCompletion.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ], 
                temperature=LLM_temperature
            )
        
        except Exception as e:
            print(f"An unexpected error occurred while calling openai.ChatCompletion.create(): {e}")
            return
        
        # Extract response
        resume = response.choices[0].message.content

        # Write optimized resume to file
        output_file_path = os.path.join(OUTPUT_FOLDER, f'resume-{filename}.md')
        write_to_text_file(output_file_path, resume)

    print(">>> END <<<")

if __name__ == "__main__":
    main()