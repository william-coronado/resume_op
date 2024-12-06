# test_optimize_resume.py

import pytest
from unittest.mock import patch, MagicMock, ANY
import optimize_resume

@pytest.fixture
def mock_config(monkeypatch):
    config = {
        'LLM_MODEL': 'gpt-4',
        'LLM_temperature': 0.7,
        'RESUME_PATH': 'test_resume.md',
        'JOB_POS_FOLDER': 'test_jobs',
        'OUTPUT_FOLDER': 'test_output'
    }
    # Monkeypatch config values
    for key, value in config.items():
        monkeypatch.setattr(f'optimize_resume.{key}', value)
    return config

def test_sendLLMRequest_success():
    with patch('optimize_resume.client.chat.completions.create') as mock_create:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Optimized content"
        mock_create.return_value = mock_response

        result = optimize_resume.sendLLMRequest("test prompt")
        assert result == "Optimized content"
        
        mock_create.assert_called_once_with(
            model=optimize_resume.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "test prompt"}
            ],
            temperature=optimize_resume.LLM_temperature
        )

def test_sendLLMRequest_exception(capsys):
    with patch('optimize_resume.client.chat.completions.create', side_effect=Exception("API Error")):
        result = optimize_resume.sendLLMRequest("test prompt")
        assert result is None
        
        captured = capsys.readouterr()
        assert "An unexpected error occurred while calling openai.chat.completions.create(): API Error" in captured.out

def test_main_success(mock_config):
    with patch('optimize_resume.read_text_file') as mock_read, \
        patch('optimize_resume.os.listdir') as mock_listdir, \
        patch('optimize_resume.sendLLMRequest') as mock_send, \
        patch('optimize_resume.write_to_text_file') as mock_write, \
        patch('optimize_resume.getPrompt') as mock_prompt:

        mock_read.return_value = "Original resume"
        mock_listdir.return_value = ["job1.txt"]
        mock_send.return_value = "Optimized resume"
        mock_prompt.return_value = "Generated prompt"

        optimize_resume.main()

        mock_read.assert_called()
        mock_send.assert_called_once_with("Generated prompt")
        mock_write.assert_called_once_with(ANY, "Optimized resume")

def test_main_missing_resume(mock_config, capsys):
    with patch('optimize_resume.read_text_file', return_value=None):
        optimize_resume.main()
        captured = capsys.readouterr()
        assert "Error: Failed to read the resume." in captured.out

def test_main_missing_job_folder(mock_config, capsys):
    with patch('optimize_resume.read_text_file', return_value="resume"), patch('optimize_resume.os.listdir', side_effect=FileNotFoundError):
        optimize_resume.main()
        captured = capsys.readouterr()
        assert f"Error: The directory {mock_config['JOB_POS_FOLDER']} was not found." in captured.out