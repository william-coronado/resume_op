import os
import openai
from helper_lib import *

# OpenAI API Key is assumed to be in OS env variable
openai.api_key = os.getenv('OPENAI_DEVKEY')
job_pos_folder = './input/'
output_folder = './output'
resume_path = './william-resume.md'

md_resume = read_text_file(resume_path)

dir_list = os.listdir(job_pos_folder)
print(">>> START <<<")
for filename in dir_list:
    print("Processing %s" %filename)

    job_description = read_text_file(job_pos_folder + filename)
    prompt = getPrompt(md_resume, job_description)

    # make api call
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ], 
        temperature = 0.25
    )
        
    # extract response
    resume = response.choices[0].message.content

    write_to_text_file('%s/resume-%s.md' %(output_folder,filename), resume)

print(">>> END <<<")