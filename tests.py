import os
import pytest
from unittest.mock import patch, MagicMock
import optimise_resume

# Mock environment variable
@pytest.fixture(autouse=True)
def mock_env_var(monkeypatch):
    monkeypatch.setenv('OPENAI_DEVKEY', 'test_api_key')
    monkeypatch.setenv('OPENAI_API_KEY', 'test_api_key')

# Mock read_text_file function
@pytest.fixture
def mock_read_text_file():
    with patch('optimise_resume.read_text_file', return_value="Mocked file content") as mock:
        yield mock

# Mock write_to_text_file function
@pytest.fixture
def mock_write_to_text_file():
    with patch('optimise_resume.write_to_text_file') as mock:
        yield mock

# Mock os.listdir function
@pytest.fixture
def mock_os_listdir():
    with patch('os.listdir', return_value=['job1.txt', 'job2.txt']) as mock:
        yield mock

# Mock OpenAI API call
@pytest.fixture
def mock_openai_api_call():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mocked optimized resume"))]
    with patch('openai.ChatCompletion.create', return_value=mock_response) as mock:
        yield mock

def test_optimise_resume(mock_env_var, mock_read_text_file, mock_write_to_text_file, mock_os_listdir, mock_openai_api_call):
    # Run the script
    optimise_resume.main()

    # Check if read_text_file was called correctly
    mock_read_text_file.assert_any_call('./william-resume.md')
    mock_read_text_file.assert_any_call('./input/job1.txt')
    mock_read_text_file.assert_any_call('./input/job2.txt')

    # Check if OpenAI API was called correctly
    assert mock_openai_api_call.called

    # Check if write_to_text_file was called correctly
    mock_write_to_text_file.assert_any_call('./output/resume-job1.txt', 'Mocked optimized resume')
    mock_write_to_text_file.assert_any_call('./output/resume-job2.txt', 'Mocked optimized resume')