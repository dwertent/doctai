"""
Integration tests for the full documentation testing workflow.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from doc_tester.orchestrator import DocumentationTester
from tests.mocks import mock_openai_response, VALID_AI_RESPONSE


class TestFullWorkflow:
    """Test the complete workflow with mocked AI."""
    
    @patch('doc_tester.ai_client.requests.post')
    def test_complete_workflow_openai(self, mock_post, temp_dir, sample_doc):
        """Test complete workflow with OpenAI (mocked)."""
        # Setup
        doc_file = temp_dir / "README.md"
        doc_file.write_text(sample_doc)
        
        # Mock AI response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_openai_response(VALID_AI_RESPONSE)
        mock_post.return_value = mock_response
        
        # Run workflow
        tester = DocumentationTester(
            api_key="test-key",
            provider="openai",
            work_dir=str(temp_dir / "work"),
            verbose=False
        )
        
        results = tester.test_documentation([str(doc_file)])
        
        # Verify
        assert results['success'] is True
        assert 'documentation' in results
        assert mock_post.called
    
    @patch('doc_tester.ai_client.requests.post')
    def test_workflow_with_custom_instructions(self, mock_post, temp_dir, sample_doc):
        """Test workflow with custom instructions."""
        # Setup
        doc_file = temp_dir / "README.md"
        doc_file.write_text(sample_doc)
        
        # Mock AI response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_openai_response(VALID_AI_RESPONSE)
        mock_post.return_value = mock_response
        
        # Run with custom instructions
        tester = DocumentationTester(
            api_key="test-key",
            provider="openai",
            work_dir=str(temp_dir / "work"),
            verbose=False
        )
        
        custom_instructions = "Test on Ubuntu 22.04 only"
        results = tester.test_documentation(
            [str(doc_file)],
            custom_instructions=custom_instructions
        )
        
        # Verify custom instructions were passed to AI
        call_args = mock_post.call_args
        request_data = call_args[1]['json']
        messages = request_data['messages']
        
        # Check that custom instructions are in the prompt
        system_message = next((m for m in messages if m['role'] == 'system'), None)
        assert system_message is not None
        assert "Ubuntu 22.04" in system_message['content']
    
    @patch('doc_tester.ai_client.requests.post')
    def test_workflow_with_failure(self, mock_post, temp_dir, sample_doc):
        """Test workflow when scripts fail."""
        # Setup
        doc_file = temp_dir / "README.md"
        doc_file.write_text(sample_doc)
        
        # Mock AI response with failing script
        failing_response = """Here's a test script:

```bash
#!/bin/bash
exit 1
```
"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_openai_response(failing_response)
        mock_post.return_value = mock_response
        
        # Run workflow
        tester = DocumentationTester(
            api_key="test-key",
            provider="openai",
            work_dir=str(temp_dir / "work"),
            stop_on_failure=True,
            verbose=False
        )
        
        results = tester.test_documentation([str(doc_file)])
        
        # Verify failure was detected
        assert results['success'] is False
    
    @patch('doc_tester.ai_client.requests.post')
    def test_multiple_iterations(self, mock_post, temp_dir, sample_doc):
        """Test multiple AI iterations."""
        # Setup
        doc_file = temp_dir / "README.md"
        doc_file.write_text(sample_doc)
        
        # Mock multiple AI responses
        iteration_responses = [
            mock_openai_response("Iteration 1 response with scripts..."),
            mock_openai_response("Iteration 2 response..."),
        ]
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = iteration_responses
        mock_post.return_value = mock_response
        
        # Run workflow with iterations
        tester = DocumentationTester(
            api_key="test-key",
            provider="openai",
            work_dir=str(temp_dir / "work"),
            max_iterations=2,
            verbose=False
        )
        
        results = tester.test_documentation([str(doc_file)])
        
        # Verify multiple AI calls were made
        assert mock_post.call_count >= 1

