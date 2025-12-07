import asyncio
from typing import Dict, Any, Optional, List
import litellm
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.state import Metrics


class LLM:
    """LLM interface using litellm."""
    
    def __init__(self, model: str = "gpt-4", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.metrics = Metrics()
        
        # Set API key if provided
        if api_key:
            litellm.api_key = api_key
        if base_url:
            litellm.api_base = base_url
    
    async def complete(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Complete a chat conversation."""
        try:
            # Use litellm for completion
            response = await asyncio.to_thread(
                litellm.completion,
                model=self.model,
                messages=messages,
                **kwargs
            )
            
            # Update metrics
            if hasattr(response, 'usage') and response.usage:
                self.metrics.prompt_tokens += response.usage.prompt_tokens or 0
                self.metrics.completion_tokens += response.usage.completion_tokens or 0
                self.metrics.total_tokens += response.usage.total_tokens or 0
                
                # Estimate cost (rough approximation)
                if 'gpt-4' in self.model.lower():
                    cost = (response.usage.prompt_tokens * 0.03 + response.usage.completion_tokens * 0.06) / 1000
                elif 'gpt-3.5' in self.model.lower():
                    cost = (response.usage.prompt_tokens * 0.001 + response.usage.completion_tokens * 0.002) / 1000
                else:
                    cost = 0.01  # Default small cost
                
                self.metrics.accumulated_cost += cost
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"LLM Error: {e}")
            return f"Error: {str(e)}"