from metrics_functions.metrics_all import evaluate_files, save_results
from datetime import datetime

def main():
    generated_file = r"C:\desktopnoonedrive\docgenofficial\AIDocGen\metrics\input_docs\reference\fastapi-official.md"
    reference_file = r"C:\desktopnoonedrive\docgenofficial\AIDocGen\metrics\input_docs\generated\fastapi.md"

    print(f"Evaluating:\n  Generated: {generated_file}\n  Reference: {reference_file}")
    
    results = evaluate_files(generated_file, reference_file)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_file = f"metrics/evaluation_results/evaluation_{timestamp}.json"

    save_results(results, output_file)

if __name__ == "__main__":
    main()

