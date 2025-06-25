import os
from datasets import load_dataset
from constants import CONFIGS, SORTED_RAW_DATA_DIR

def main():

    for config_name in CONFIGS:
        print(f"{SORTED_RAW_DATA_DIR}/{config_name}_articles.tsv")
        dataset = load_dataset(
            'csv', 
            data_files=f"{SORTED_RAW_DATA_DIR}/{config_name}_articles.tsv", 
            delimiter='\t',
            split={
                'train': 'train[:100%]', # this data is best suited as training data
                #'test': 'train[80%:]', 
            }
        )
        
        save_path = f"laQuotidiana1997-2008_dataset/{config_name}"
        os.makedirs(save_path, exist_ok=True) # to ensure the directory exists

        for split in dataset.keys():
            # Convert the split to a list of dictionaries
            split_save_path = os.path.join(save_path, f"{split}.jsonl")
            dataset[split].to_json(split_save_path)

if __name__ == "__main__":
    main()
