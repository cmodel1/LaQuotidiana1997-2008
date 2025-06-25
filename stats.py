import os
import re
from datasets import load_dataset
from constants import CONFIGS, SPLITS, SORTED_RAW_DATA_DIR

def run_stats():
    stats = []
    for config in CONFIGS:
        dataset = load_dataset(
            'csv', 
            data_files=f"{SORTED_RAW_DATA_DIR}/{config}_articles.tsv", 
            delimiter='\t',
            split={
                'train': 'train[:100%]', # this data is best suited as training data
            }
        )        

        for split in SPLITS:
            ds = dataset[split]
            num_samples = len(ds)
            total_tokens = sum(len(sample["text"].split()) for sample in ds)
            avg_tokens = total_tokens / num_samples if num_samples > 0 else 0
            stats.append((config, split, num_samples, total_tokens, avg_tokens))
            print(f"{config} - {split}: {num_samples} samples, {total_tokens} tokens, avg {avg_tokens:.2f} tokens/sample") # sanity check
    return stats


def generate_markdown(stats):
    md_lines = []
    md_lines.append("# Dataset Statistics\n")
    md_lines.append("| Idiom      | Split      | Samples | Total Tokens | Avg Tokens per Sample |")
    md_lines.append("|------------|------------|---------|--------------|-----------------------|")
    for config, split, samples, total_tokens, avg_tokens in stats:
        md_lines.append(f"| {config} | {split} | {samples:,} | {total_tokens:,} | {avg_tokens:,.2f} |")
    md_content = "\n".join(md_lines)
    return md_content


def main():
    stats = run_stats()
    md_content = generate_markdown(stats)
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to replace only the specific section
    updated_content = re.sub(
        rf"(## Dataset Statistics\n(?:.*\n)*?)(?=\n#|\Z)",  # Match until next H2 or EOF
        md_content + "\n",
        content,
        flags=re.MULTILINE
    )
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)


if __name__ == "__main__":
    main()
