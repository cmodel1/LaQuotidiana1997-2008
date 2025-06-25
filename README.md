# Rumantsch Data from La Quotidiana, 1997–2008

### Table of Contents
- [Dataset Statistics](#dataset-statistics)
- [Data Directories in this Repository](#data-directories-in-this-repository)
- [Reproducing the Processed Data](#reproducing-the-processed-data)
    - [Installation and Setup](#installation-and-setup)
    - [Casting the original data into tsv files sorted by idiom](#casting-the-original-data-into-tsv-files-sorted-by-idiom)
    - [Generating Hugging Face Datasets](#generating-hugging-face-hf-datasets) 
- [Running Tests](#running-tests)
- [Legal Notice](#legal-notice)


## Dataset Statistics

| Idiom      | Split      | Samples | Total Tokens | Avg Tokens per Sample |
|------------|------------|---------|--------------|-----------------------|
| rm-rumgr | train | 28,730 | 5,595,308 | 194.75 |
| rm-sursilv | train | 64,233 | 13,549,505 | 210.94 |
| rm-vallader | train | 30,679 | 6,329,280 | 206.31 |
| rm-puter | train | 5,127 | 1,296,620 | 252.90 |
| rm-surmiran | train | 12,111 | 3,283,765 | 271.14 |
| rm-sutsilv | train | 4,827 | 1,255,978 | 260.20 |

## Data Directories in this Repository
There are three subdirectories containing data from 1997 to 2008 from <i>La Quotidiana</i>, a Rumantsch-language newspaper:
* ```la_quotidiana```: this directory contains the original data files from 1997 to 2008 provided by La Quotidiana under public domain, originally sourced from [ProSvizraRumantscha's](https://github.com/ProSvizraRumantscha) [Github corpora repository](https://github.com/ProSvizraRumantscha/corpora). To see a summary of the statistics pertaining to this data, have a look at the ```README``` file in the repository.  

* ```sorted_raw_data```: this directory represents the data in ```la_quotidiana``` sorted by idiom, where each idiom corresponds to a ```tsv``` file that compiles all articles written in that idiom across the data. This directory can be populated by using the ```sort_articles_by_idiom.py``` script, which is described in more detail [below](#casting-the-original-data-into-tsv-files-sorted-by-idiom).

* ```laQuotidiana1997-2008_dataset```: this directory contains the Hugging Face dataset for each idiom as ```jsonl``` files, which can be reproduced by running ```build_dataset.py```, again described in greater detail [below](#generating-hugging-face-hf-datasets). Since the idiom of the La Quotidiana articles from 1997 to 2008 were annotated automatically using [franc](https://www.npmjs.com/package/franc) (see the implementation [here](https://github.com/ProSvizraRumantscha/pledarix/blob/master/webExtension/app/lib/franc-all.js)), this data is less suited to be in a test split. As a result, you will only find training datasets for each idiom based on this data.

## Reproducing the Processed Data
### Installation and Setup
1. Clone this repository using the following command:
```
git clone <github_url>
```
2. Create a new Python virtual environment inside the repository and activate it - e.g. using venv:
```
python -m venv .venv
```
```
source .venv/bin/activate
```
3. Install the required packages and dev dependencies using:
```
pip install -r requirements.txt
```

### Casting the original data into tsv files sorted by idiom
1. Make sure there is a directory called ```sorted_raw_data``` in the root directory. 
2. To reproduce or overwrite the data in that directory, run: 
```
python sort_articles_by_idiom.py
```
This script goes through each file in the directory (```la-quotidiana```) containing the original La Quotidiana data from 1997-2008 provided by ProSvizraRumantscha (sorted by year) and organizes the data by idiom as a tsv files inside ```sorted_raw_data```.

### Generating Hugging Face (HF) Datasets
1. To create HF datasets for each idiom run the following:
```
python build_dataset.py
```
This will create only training sets, since this data is better suited as training data for the creation of a Rumantsch idiom identification system. To change this, feel free to edit the splits dictionary in ```build_dataset.py```. <br>
The code loads the dataset using: 
```
from datasets import load_dataset
dataset = load_dataset(
    "csv", 
    data_files="sorted_raw_data/rm-puter_articles.tsv", 
    delimiter='\t', 
    split={
        'train': 'train[:100%]',
    }
)
```
This follows the recommendations for loading a local dataset listed in the [Hugging Face Datasets documenation](https://huggingface.co/docs/datasets/en/package_reference/loading_methods).

Constants used in ```sort_articles_by_idiom.py``` and ```build_dataset.py``` can be found in the ```constants.py``` file.

## Running Dataset Statistics
To run a script that prints statistics for the HF dataset (number of samples and tokens per idiom and split) and saves them in the [Dataset Statistics table section](#dataset-statistics) at the beginning of this file, run the following command:
``` 
python stats.py
```


## Running Tests


## Legal Notice
Articles from the Romansh-language newspaper “La Quotidiana” between
1997 and 2008.

![Public Domain](https://licensebuttons.net/p/zero/1.0/88x31.png)

To the extent possible under law, the newspaper’s publisher
[Somedia](http://www.somedia.ch/) has
[waived](https://creativecommons.org/publicdomain/zero/1.0/deed)
all copyright and related or neighboring rights to this corpus.
This work is published from Switzerland.

