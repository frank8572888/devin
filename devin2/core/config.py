import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration for the devin2 system."""
    
    # LLM Configuration
    model_name: str = "gpt-4"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    
    # Agent Configuration
    max_iterations: int = 100
    max_budget_per_task: Optional[float] = None
    
    # Runtime Configuration
    workspace_dir: str = "/tmp/devin2_workspace"
    enable_ipython: bool = True
    enable_bash: bool = True
    
    # Logging
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables."""
        return cls(
            model_name=os.getenv('DEVIN2_MODEL', 'gpt-4'),
            api_key=os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY'),
            base_url=os.getenv('DEVIN2_BASE_URL'),
            max_iterations=int(os.getenv('DEVIN2_MAX_ITERATIONS', '100')),
            max_budget_per_task=float(os.getenv('DEVIN2_MAX_BUDGET', '0')) or None,
            workspace_dir=os.getenv('DEVIN2_WORKSPACE', '/tmp/devin2_workspace'),
            enable_ipython=os.getenv('DEVIN2_ENABLE_IPYTHON', 'true').lower() == 'true',
            enable_bash=os.getenv('DEVIN2_ENABLE_BASH', 'true').lower() == 'true',
            log_level=os.getenv('DEVIN2_LOG_LEVEL', 'INFO')
        )