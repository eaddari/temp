from source.judge import Judge
import pandas as pd
import os, re, json
from tqdm import tqdm

from prompts.coherence_prompt import SYSTEM_PROMPT as coherence
from prompts.relevance_prompt import SYSTEM_PROMPT as relevance
from prompts.consistency_prompt import SYSTEM_PROMPT as consistency
from prompts.fluency_prompt import SYSTEM_PROMPT as fluency


class EvaluatorClass():
    def __init__(self, path_file_script_to_text: str, defendats: list[str], judges: list[str]):
        self.file_path = path_file_script_to_text
        self.defendats, self.judges = defendats, judges
        os.makedirs("standalone_converter/data", exist_ok=True)
        self.__create_file_score()
    
    def __dataset_partion(self, defendant: str):
        df = pd.read_parquet(self.file_path)
        return df[["name", "content", defendant]]
    
    def __create_file_score(self):
        for judge in self.judges:
            print("Giudice: ", judge)
            coherence_judge = Judge(model=judge, system_prompt=coherence)
            relevance_judge = Judge(model=judge, system_prompt=relevance)
            fluency_judge = Judge(model=judge, system_prompt=fluency)
            consistency_judge = Judge(model=judge, system_prompt=consistency)

            for defendat in self.defendats: 
                dataframe = self.__dataset_partion(defendat)

                df_evaluated = []

                for _, row in tqdm(dataframe.iterrows(), total=len(dataframe)):
                    df_evaluated.append({
                        "name": row["name"], 
                        "content": row["content"], 
                        defendat: row[defendat], 
                        "coherence": coherence_judge.start_evaluation(row["content"], row[defendat]),
                        "relevance": relevance_judge.start_evaluation(row["content"], row[defendat]),
                        "fluency": fluency_judge.start_evaluation(row["content"], row[defendat]),
                        "consistency": consistency_judge.start_evaluation(row["content"], row[defendat])
                    })

                pd.DataFrame(df_evaluated).to_parquet(f"standalone_converter/data/score_{defendat}_by_{judge}.parquet")
    
    def __filter_text(self, content: str) -> int:
        match = re.search(r'\d+(?:\.\d+)?', content)
        return int(match.group())
    
    def __save_to_json(self, data: dict, file_name: str) -> None:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4) 

    def create_final_df(self) -> dict:
        final_df = {}

        for defendat in self.defendats:
            score_judges = {}
            for judge in self.judges:
                df = pd.read_parquet(f"standalone_converter/data/score_{defendat}_by_{judge}.parquet")
                score_judges[judge] = {
                    "coherence": df["coherence"].apply(self.__filter_text).astype(int).mean(), 
                    "relevance": df["relevance"].apply(self.__filter_text).astype(int).mean(),
                    "fluency:": df["fluency"].apply(self.__filter_text).astype(int).mean(), 
                    "consistency": df["consistency"].apply(self.__filter_text).astype(int).mean()
                }
            final_df[defendat] = score_judges
        os.makedirs("standalone_converter/results", exist_ok=True)
        self.__save_to_json(final_df, "standalone_converter/results/all_score.json")
        return final_df
    
    def average_metrics(self, data: dict) -> dict:
        result = {}
        for main_key, models in data.items():
            metrics_sum = {}
            count = 0
            
            for model, metrics in models.items():
                count += 1
                for metric, value in metrics.items():
                    if metric not in metrics_sum:
                        metrics_sum[metric] = 0.0
                    metrics_sum[metric] += value
            
            result[main_key] = {metric: value / count for metric, value in metrics_sum.items()}
        os.makedirs("standalone_converter/results", exist_ok=True)
        self.__save_to_json(result, "standalone_converter/results/avg_score.json")
        return result