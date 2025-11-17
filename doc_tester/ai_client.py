"""
AI client module.

Handles communication with various AI providers (OpenAI, Anthropic, etc.)
"""

import os
import json
import requests
from typing import List, Dict, Optional, Any
from enum import Enum


class AIProvider(Enum):
    """Supported AI providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    CUSTOM = "custom"


class AIClient:
    """Client for interacting with AI providers."""
    
    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        provider: str = "openai",
        model: Optional[str] = None,
        timeout: int = 120
    ):
        """
        Initialize AI client.
        
        Args:
            api_key: API key for the AI provider
            api_url: Custom API URL (optional, uses provider default if not set)
            provider: AI provider name (openai, anthropic, gemini, custom)
            model: Model name to use (optional, uses provider default)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.provider = self._parse_provider(provider)
        self.timeout = timeout
        
        # Set API URL based on provider
        if api_url:
            self.api_url = api_url
        elif self.provider == AIProvider.OPENAI:
            self.api_url = "https://api.openai.com/v1/chat/completions"
        elif self.provider == AIProvider.ANTHROPIC:
            self.api_url = "https://api.anthropic.com/v1/messages"
        elif self.provider == AIProvider.GEMINI:
            # Gemini API URL will include the model and key in the URL
            # Format: https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
            self.api_url = None  # Set in _send_gemini_message
        else:
            raise ValueError("api_url must be provided for custom provider")
        
        # Set default model based on provider
        if model:
            self.model = model
        elif self.provider == AIProvider.OPENAI:
            self.model = "gpt-4o"
        elif self.provider == AIProvider.ANTHROPIC:
            self.model = "claude-3-5-sonnet-20241022"
        elif self.provider == AIProvider.GEMINI:
            self.model = "gemini-1.5-pro-latest"
        else:
            raise ValueError("model must be provided for custom provider")
        
        self.conversation_history: List[Dict[str, str]] = []
    
    def _parse_provider(self, provider: str) -> AIProvider:
        """Parse provider string to enum."""
        provider_lower = provider.lower()
        for p in AIProvider:
            if p.value == provider_lower:
                return p
        return AIProvider.CUSTOM
    
    def send_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a message to the AI and get a response.
        
        Args:
            message: User message to send
            system_prompt: Optional system prompt to set context
            
        Returns:
            AI response text
        """
        if self.provider == AIProvider.OPENAI:
            return self._send_openai_message(message, system_prompt)
        elif self.provider == AIProvider.ANTHROPIC:
            return self._send_anthropic_message(message, system_prompt)
        elif self.provider == AIProvider.GEMINI:
            return self._send_gemini_message(message, system_prompt)
        else:
            return self._send_custom_message(message, system_prompt)
    
    def _send_openai_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Send message using OpenAI API."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add new message
        messages.append({"role": "user", "content": message})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4096
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise RuntimeError(f"OpenAI API authentication failed. Please check your API key.")
            elif e.response.status_code == 429:
                raise RuntimeError(f"OpenAI rate limit exceeded. Please wait and try again.")
            elif e.response.status_code == 400:
                try:
                    error_msg = e.response.json().get('error', {}).get('message', str(e))
                except:
                    error_msg = e.response.text
                raise RuntimeError(f"OpenAI API error: {error_msg}")
            else:
                raise RuntimeError(f"OpenAI API error ({e.response.status_code}): {e.response.text}")
        except requests.exceptions.Timeout:
            raise RuntimeError(f"OpenAI API request timed out after {self.timeout} seconds. Try increasing --timeout.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to communicate with OpenAI: {str(e)}")
    
    def _send_anthropic_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Send message using Anthropic API."""
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Build messages from history
        messages = self.conversation_history.copy()
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": messages
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            ai_response = result["content"][0]["text"]
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise RuntimeError(f"Anthropic API authentication failed. Please check your API key.")
            elif e.response.status_code == 429:
                raise RuntimeError(f"Anthropic rate limit exceeded. Please wait and try again.")
            elif e.response.status_code == 400:
                try:
                    error_msg = e.response.json().get('error', {}).get('message', str(e))
                except:
                    error_msg = e.response.text
                raise RuntimeError(f"Anthropic API error: {error_msg}")
            else:
                raise RuntimeError(f"Anthropic API error ({e.response.status_code}): {e.response.text}")
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Anthropic API request timed out after {self.timeout} seconds. Try increasing --timeout.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to communicate with Anthropic: {str(e)}")
    
    def _send_gemini_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Send message using Google Gemini API."""
        # Build the API URL with model and key
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Build contents from conversation history
        contents = []
        
        # Gemini doesn't have a separate system message field, so we prepend it to the first user message
        first_message = message
        if system_prompt and not self.conversation_history:
            first_message = f"{system_prompt}\n\n{message}"
        
        # Add conversation history
        for msg in self.conversation_history:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        # Add new message
        contents.append({
            "role": "user",
            "parts": [{"text": first_message}]
        })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4096,
            }
        }
        
        try:
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract response text from Gemini format
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    ai_response = candidate["content"]["parts"][0]["text"]
                else:
                    raise ValueError("Unexpected response format from Gemini API")
            else:
                raise ValueError("No candidates in Gemini API response")
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401 or e.response.status_code == 403:
                raise RuntimeError(f"Gemini API authentication failed. Please check your API key.")
            elif e.response.status_code == 429:
                raise RuntimeError(f"Gemini rate limit exceeded. Please wait and try again.")
            elif e.response.status_code == 400:
                try:
                    error_msg = e.response.json().get('error', {}).get('message', str(e))
                except:
                    error_msg = e.response.text
                raise RuntimeError(f"Gemini API error: {error_msg}")
            else:
                raise RuntimeError(f"Gemini API error ({e.response.status_code}): {e.response.text}")
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Gemini API request timed out after {self.timeout} seconds. Try increasing --timeout.")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to communicate with Gemini: {str(e)}")
    
    def _send_custom_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Send message using custom API (OpenAI-compatible format)."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": message})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4096
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            # Try OpenAI format first
            if "choices" in result:
                ai_response = result["choices"][0]["message"]["content"]
            # Try Anthropic format
            elif "content" in result:
                ai_response = result["content"][0]["text"]
            else:
                raise ValueError("Unexpected response format from custom API")
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
        
        except Exception as e:
            raise RuntimeError(f"Failed to communicate with custom AI: {str(e)}")
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []

