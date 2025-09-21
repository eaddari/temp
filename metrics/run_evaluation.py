"""
Azure AI Foundry Document Evaluator - Quick Start

This script evaluates two documents using your three deployed Azure AI Foundry models:
- DeepSeek-V3-0324
- gpt-5-mini  
- grok-3

The script will ask each model which document is better and average the results.
"""

from azure_llm_evaluator import AzureLLMEvaluator

def main():
    print("Azure AI Foundry Document Evaluator")
    print("=" * 40)
    
    # Initialize evaluator
    evaluator = AzureLLMEvaluator()
    
    # Get document paths from user or use defaults
    print("\nEnter document paths (or press Enter for default example):")
    
    doc_a = input("Document A path: ").strip()
    
    doc_b = input("Document B path: ").strip() 

    # Run evaluation
    try:
        results = evaluator.evaluate_documents(doc_a, doc_b)
        
        # Print detailed results
        print(f"\n{'='*60}")
        print("DETAILED RESULTS")
        print(f"{'='*60}")
        
        for i, result in enumerate(results["individual_results"], 1):
            print(f"\nModel {i}: {result['model_full_name']}")
            print(f"  Winner: Document {result['better_document']}")
            print(f"  Confidence: {result['confidence']}")
            print(f"  Scores: A={result['scores']['document_A']}, B={result['scores']['document_B']}")
            print(f"  Reasoning: {result['reasoning']}")
        
        # Print summary
        summary = results["summary"]
        print(f"\n{'='*60}")
        print("FINAL SUMMARY")
        print(f"{'='*60}")
        print(f"🏆 Winner by votes: Document {summary['winner_by_votes']} ({summary['votes'][summary['winner_by_votes']]}/3 votes)")
        print(f"📊 Winner by average score: Document {summary['winner_by_average_score']}")
        print(f"📈 Average scores: A={summary['average_scores']['document_A']}, B={summary['average_scores']['document_B']}")
        print(f"🎯 Average confidence: {summary['average_confidence']}")
        print(f"📏 Score difference: {summary['score_difference']}")
        
        # Save results
        output_file = evaluator.save_results(results)
        print(f"\n💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}")
        print("\nPlease check:")
        print("1. Your .env file has all the required endpoints and API keys")
        print("2. Your Azure AI Foundry models are deployed and accessible")
        print("3. The document paths exist and are readable")

if __name__ == "__main__":
    main()