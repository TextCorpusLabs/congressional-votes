Below can be found a list of data manulipation scripts that help make this work posible.
Both R and Python were used.
Python for the data collection and manuliption.
R for the analysis and paper generation.

# Python

All scripts have been tested on Python 3.8.5.
The external modules that were used can be found in the `requirments.txt` file along with their versions.
**Note**: not all modules are required for all scripts.
If any of the modules are not alreasy installed the normal `pip install -r requirments.txt` process should be followed.

## Scripts

Below is a brief summary of each of the scripts.
In order to fully regenerate the results run the scripts in the order listed.
Any folder result will be deleted, including subfolders, then recreated.
Any file result will first be overwritten.
The pathing can be changed to any desired location.
Some script results need to be stored in the `~/results` folder in order for the [code written in R](./#r) to be run without path updates.
When this is the case, the script will note as such.
These paths can still be changed, but the R code will need to be adjusted internally.

1. [get_list_of_votes.py](./get_list_of_votes.py).
   This script will get the list of votes from [Congress](https://www.congress.gov).
   The script needs to know which congress (I.E. 101st)
   ```{shell}
   python -O get_list_of_votes.py -out d:/temp/list_of_votes -c 101
   ```
2. [process_list_of_votes.py](./process_list_of_votes.py).
   This script converts the raw `JSON` downloaded in step 1 into an easy to consume `CSV`.
   This is a [**core result**](./#core-results).
   It needs to be stored in the `~/results` folder for further processing.
   It needs to be compressed and uploaded to [releases][releases].
   ```{shell}
   python -O process_list_of_votes.py -in d:/temp/list_of_votes -out d:/temp/list_of_votes.csv
   ```
3. [get_vote_details.py](./get_vote_details.py).
   This script will get the details of each vote from [govtrack.us](https://govtrack.us) based on the prior result.
   ```{shell}
   python -O get_vote_details.py -in d:/temp/list_of_votes.csv -out d:/temp/vote_details
   ```
4. [process_vote_details.py](./process_vote_details.py)
   This script combines the raw `CSV` downloaded in step 3 into a single easy to consume `CSV`.
   This is a [**core result**](./#core-results).
   It needs to be stored in the `~/results` folder for further processing.
   It needs to be compressed and uploaded to [releases][releases].
   ```{shell}
   python -O process_vote_details.py -in d:/temp/vote_details -out d:/temp/vote_details.csv
   ```
5. [get_vote_text.py](./get_vote_text.py)
   This script will get the plain text of measure voted upon from [congress.gov](https://congress.gov) based on the prior result.
   ```{shell}
   python -O get_vote_text.py -in d:/temp/list_of_votes.csv -out d:/temp/vote_details
   ```

# R

All scripts have been tested on R/R Studio 3.6.2/1.2.5019.
The below packages are needed to run the scripts.
The scripts were tested on the noted versions, so YMMV.
**Note**: not all packages are required for all scripts.
If this it the first time running the scripts, the packages will need to be installed.
They can be installed using the below code then re-starting RStudio.

* dplyr 0.8.5
* ggpubr 0.2.5

```{r}
install.packages(c('dplyr', 'ggpubr'))
```

# Core Results

Some [scripts](./#scripts) produce data that is considered temporary while others produce core features of the dataset.
When the result is a **core result**, the result needs copied to the `~/results` folder as well as compressed and uploaded to [GitHub](https://github.com) for long term storage.
This two part aproach is taken because GitHub has some issues when dealing with [large files](https://help.github.com/en/articles/working-with-large-files).
The [recomended method](https://help.github.com/en/articles/distributing-large-binaries) for dealing with large files is to store them in [releases][releases].
You can find the gzip'ed versions of the below there.
Any of the steps above can be skipped by downloading the correct file and proceding from that point forward.

The below list represents the **core results** in this dataset.

1. [List of Votes](https://github.com/MindMimicLabs/data-congressional-votes/releases/download/1.0/list_of_votes.csv.gz)
   * Download to the `~/results` folder and extract in place
2. [Vote Details](https://github.com/MindMimicLabs/data-congressional-votes/releases/download/1.0/vote_details.csv.gz)
   * Download to the `~/results` folder and extract in place
3. Bill text

[releases]: https://github.com/MindMimicLabs/data-congressional-votes/releases
