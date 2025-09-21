# microservices.transforming_pipeline.components.anonimization.tests.test_anonimizator

Source file: `microservices\transforming_pipeline\components\anonimization\tests\test_anonimizator.py`

## Source Code

```python
import sys
import os
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'source')))
from anonimizator_azure import AnonimizatorAzure

class TestAnonimizatorAzure:
    """Test class for AnonimizatorAzure functionality."""
    
    @pytest.fixture
    def test_real_env_vars(self):
        """Real test of initialization of environment variables."""
        return {
            "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
            "AZURE_OPENAI_VERSION": os.getenv("AZURE_OPENAI_VERSION"),
            "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "AZURE_OPENAI_DEPLOYMENT": os.getenv("AZURE_OPENAI_DEPLOYMENT")
        }
    
    def test_vars_initialization(self):
        """Real test that AnonimizatorAzure initializes correctly with environment variables."""
        anonimizator = AnonimizatorAzure()
        
        assert anonimizator.subscription_key == os.getenv("AZURE_OPENAI_API_KEY")
        assert anonimizator.api_version == os.getenv("AZURE_OPENAI_VERSION")
        assert anonimizator.azure_endpoint == os.getenv("AZURE_OPENAI_ENDPOINT")
        assert anonimizator.azure_model_deployment == os.getenv("AZURE_OPENAI_DEPLOYMENT")
        assert "You are a data anonymization assistant" in anonimizator.SYSTEM_PROMPT

    def test_llm_parquet_anonimizer_real_call(self):
        """Real test of the llm_parquet_anonimizer function on text containing PII."""
        anonimizator = AnonimizatorAzure()
        input_text = "My name is John Doe. My email is john.doe@example.com. My password is superSecret123."
        result = anonimizator.llm_parquet_anonimizer(input_text)

        assert isinstance(result, str)
        assert "<EMAIL>" in result or "example.com" not in result
        assert "<PASSWORD>" in result or "superSecret123" not in result
        assert "<PERSON>" in result or "John Doe" not in result
        assert "<API_KEY>" in result or "akd1239u8190ue101jodjakn1090123098dyq" not in result

    def test_parallel_anonimization_real_call(self):
        """Real test of the parallel_anonimization function on a DataFrame containing PII."""
        anonimizator = AnonimizatorAzure()
        df = pd.read_parquet(anonimizator.input_file)
        anonimizator.parallel_anonimization(df)
        assert anonimizator.output_file is not None 

if __name__ == "__main__":
    pytest.main([__file__])

```
