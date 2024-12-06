import os
import pytest
from unittest.mock import patch, MagicMock
import optimize_resume

# Mock configuration data
mock_config = {
    'OPENAI_API_KEY': 'test_api_key',
    'JOB_POS_FOLDER': './input/',
    'OUTPUT_FOLDER': './output/',
    'RESUME_PATH': './william-resume.md',
    'LLM_MODEL': 'gpt-4o-mini',
    'LLM_temperature': 0.25
}

# Mock data for read_text_file
mock_resume_content = "This is a test resume."
mock_job_description_content = "This is a test job description."

@patch.dict(os.environ, {'OPENAI_DEVKEY': 'test_api_key'})
@patch('optimize_resume.yaml.safe_load', return_value=mock_config)
@patch('optimize_resume.os.listdir', return_value=['job1.txt', 'job2.txt'])
@patch('optimize_resume.write_to_text_file')
@patch('optimize_resume.read_text_file', side_effect=[
    mock_resume_content,
    mock_job_description_content,
    mock_job_description_content
])
@patch('openai.ChatCompletion.create')
def test_optimize_resume(
    mock_openai_create,
    mock_read_text_file,
    mock_write_to_text_file,
    mock_os_listdir,
    mock_yaml_safe_load
):
    # Set up the mock for OpenAI API call
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mocked optimized resume"))]
    mock_openai_create.return_value = mock_response

    # Run the script
    optimize_resume.main()

    # Check if read_text_file was called correctly
    mock_read_text_file.assert_any_call('./william-resume.md')
    mock_read_text_file.assert_any_call('./input/job1.txt')
    mock_read_text_file.assert_any_call('./input/job2.txt')

    # Check if os.listdir was called correctly
    mock_os_listdir.assert_called_with('./input/')

    # Check if OpenAI API was called
    assert mock_openai_create.called

    # Check if write_to_text_file was called correctly
    mock_write_to_text_file.assert_any_call(
        './output/resume-job1.txt.md', 'Mocked optimized resume'
    )
    mock_write_to_text_file.assert_any_call(
        './output/resume-job2.txt.md', 'Mocked optimized resume'
    )

if __name__ == "__main__":
    pytest.main()