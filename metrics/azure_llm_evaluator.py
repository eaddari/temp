import os
import json
from datetime import datetime
from typing import Dict, List, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("C:/desktopnoonedrive/docgenofficial/AIDocGen/.env", override=True)

class AzureLLMEvaluator:
    """Minimal evaluator using Azure AI Foundry models to compare documents"""
    
    def __init__(self):
        self.models = {
            "deepseek": {
                "endpoint": os.getenv("DEEPSEEK_ENDPOINT"),
                "model": "DeepSeek-V3-0324",
                "deployment_name": os.getenv("DEEPSEEK_DEPLOYMENT_NAME", "DeepSeek-V3-0324"),
                "api_key": os.getenv("DEEPSEEK_API_KEY")
            },
            "phi4": {
                "endpoint": os.getenv("PHI4_ENDPOINT"), 
                "model": "phi-4",
                "deployment_name": os.getenv("PHI4_DEPLOYMENT_NAME", "Phi-4"),
                "api_key": os.getenv("PHI4_API_KEY")
            },
            "grok3": {
                "endpoint": os.getenv("GROK3_ENDPOINT"),
                "model": "grok-3",
                "deployment_name": os.getenv("GROK3_DEPLOYMENT_NAME", "grok-3"),
                "api_key": os.getenv("GROK3_API_KEY")
            }
        }
        
        # Validation prompt for document comparison
        self.system_prompt = """You are an expert document evaluator. Compare two documents and determine which one is better.

Evaluate based on:
1. Content quality and accuracy
2. Completeness and coverage  
3. Clarity and organization
4. Technical accuracy
5. Usefulness to readers

If the content appears truncated, evaluate what is present.

CRITICAL: You MUST respond with ONLY a valid JSON object. Do not include any text before or after the JSON.

Use this EXACT format:
{
    "better_document": "A",
    "confidence": 0.8,
    "reasoning": "Document A has better technical accuracy and clearer organization",
    "scores": {
        "document_A": 8.5,
        "document_B": 6.2
    }
}

Remember: 
- better_document must be either "A" or "B"
- confidence must be between 0.0 and 1.0
- scores must be between 0.0 and 10.0
- Return ONLY the JSON object, nothing else"""

    def load_document(self, filepath: str) -> str:
        """Load document content from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def evaluate_with_model(self, model_name: str, doc_a: str, doc_b: str) -> Dict[str, Any]:
        """Evaluate documents using a specific Azure AI Foundry model with OpenAI SDK"""
        model_config = self.models[model_name]
        
        user_prompt = f"""
Document A:
{doc_a[:3000]}...

Document B:
{doc_b[:3000]}...

Which document is better overall? Provide your assessment in the required JSON format.
"""
        
        try:
            # Create OpenAI client for Azure endpoint
            client = OpenAI(
                base_url=model_config["endpoint"],
                api_key=model_config["api_key"]
            )
            
            response = client.chat.completions.create(
                model=model_config["deployment_name"],
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user", 
                        "content": user_prompt
                    }
                ],
                temperature=1,
                max_completion_tokens=1000  # Use max_completion_tokens for newer models
            )
            
            # Debug: Check if response is valid
            if not response or not response.choices or len(response.choices) == 0:
                raise ValueError("Empty response from API")
            
            message_content = response.choices[0].message.content
            if message_content is None:
                raise ValueError("Response content is None")
            
            # Parse JSON response
            response_text = message_content.strip()
            print(f"🔍 {model_name} raw response: {response_text[:200]}...")  # Debug output
            
            # Extract JSON from response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError(f"No valid JSON found in response: {response_text[:100]}")
            
            json_str = response_text[start_idx:end_idx]
            
            try:
                result = json.loads(json_str)
            except json.JSONDecodeError as json_err:
                print(f"⚠️ {model_name} JSON parse error: {json_err}")
                print(f"   Raw JSON: {json_str}")
                # Try to create a fallback result by analyzing the text
                result = {
                    "better_document": "A" if "document a" in response_text.lower() else "B",
                    "confidence": 0.5,
                    "reasoning": f"JSON parse error, fallback analysis from: {response_text[:100]}",
                    "scores": {"document_A": 5.0, "document_B": 5.0}
                }
            
            # Validate result structure
            required_keys = ["better_document", "confidence", "reasoning", "scores"]
            if not all(key in result for key in required_keys):
                raise ValueError(f"Response missing required keys. Got: {list(result.keys())}")
            
            result['model'] = model_name
            result['model_full_name'] = model_config["model"]
            
            print(f"✅ {model_name} evaluation completed")
            return result
            
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)}")
            return {
                "model": model_name,
                "model_full_name": model_config["model"],
                "error": str(e),
                "better_document": "A",  # default fallback
                "confidence": 0.0,
                "reasoning": f"Error occurred: {str(e)}",
                "scores": {"document_A": 5.0, "document_B": 5.0}
            }

    def evaluate_documents(self, doc_a_path: str, doc_b_path: str) -> Dict[str, Any]:
        """Evaluate documents using all three models and average results"""
        
        # Load documents
        doc_a = self.load_document(doc_a_path)
        doc_b = self.load_document(doc_b_path)
        
        print(f"Evaluating:\n  Document A: {doc_a_path}\n  Document B: {doc_b_path}")
        print("Using models: DeepSeek-V3-0324, phi-4, grok-3\n")
        
        # Evaluate with each model
        results = []
        for model_name in self.models.keys():
            print(f"Evaluating with {model_name}...")
            result = self.evaluate_with_model(model_name, doc_a, doc_b)
            results.append(result)
        
        # Calculate averages
        avg_score_a = sum(r["scores"]["document_A"] for r in results) / len(results)
        avg_score_b = sum(r["scores"]["document_B"] for r in results) / len(results)
        avg_confidence = sum(r["confidence"] for r in results) / len(results)
        
        # Determine winner based on average scores
        winner = "A" if avg_score_a > avg_score_b else "B"
        
        # Count votes
        votes_a = sum(1 for r in results if r["better_document"] == "A")
        votes_b = sum(1 for r in results if r["better_document"] == "B")
        
        # Compile final results
        final_result = {
            "evaluation_timestamp": datetime.now().isoformat(),
            "document_A": doc_a_path,
            "document_B": doc_b_path,
            "individual_results": results,
            "summary": {
                "winner_by_average_score": winner,
                "winner_by_votes": "A" if votes_a > votes_b else "B",
                "votes": {"A": votes_a, "B": votes_b},
                "average_scores": {
                    "document_A": round(avg_score_a, 2),
                    "document_B": round(avg_score_b, 2)
                },
                "average_confidence": round(avg_confidence, 2),
                "score_difference": round(abs(avg_score_a - avg_score_b), 2)
            }
        }
        
        return final_result

    def save_results(self, results: Dict[str, Any], output_path: str = None):
        """Save evaluation results to JSON file"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"metrics/evaluation_results/azure_llm_evaluation_{timestamp}.json"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {output_path}")
        return output_path


def main():
    """Example usage"""
    evaluator = AzureLLMEvaluator()
    
    # Example file paths - adjust these to your actual files
    doc_a = r"C:\desktopnoonedrive\docgenofficial\AIDocGen\metrics\input_docs\generated\fastapi.md"
    doc_b = r"C:\desktopnoonedrive\docgenofficial\AIDocGen\metrics\input_docs\reference\fastapi-official.md"
    
    # Run evaluation
    results = evaluator.evaluate_documents(doc_a, doc_b)
    
    # Print summary
    summary = results["summary"]
    print(f"\n{'='*50}")
    print("EVALUATION SUMMARY")
    print(f"{'='*50}")
    print(f"Winner by votes: Document {summary['winner_by_votes']} ({summary['votes'][summary['winner_by_votes']]}/3 votes)")
    print(f"Winner by average score: Document {summary['winner_by_average_score']}")
    print(f"Average scores: A={summary['average_scores']['document_A']}, B={summary['average_scores']['document_B']}")
    print(f"Average confidence: {summary['average_confidence']}")
    print(f"Score difference: {summary['score_difference']}")
    
    # Save results
    evaluator.save_results(results)


if __name__ == "__main__":
    main()