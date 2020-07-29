Below can be found a list of data manulipation scripts that help make this work posible.

## Packages/Modules

All scripts have been tested on Python 3.8.5.
The below modules are needed to run the scripts.
The scripts were tested on the noted versions, so YMMV.
**Note**: not all modules are required for all scripts.
If this it the first time running the scripts, the modules will need to be installed.
They can be installed by navigating to the `~/code` folder, then using the below code.

* bs4 = 0.0.1
* lxml = 4.5.0
* progressbar2 = 3.47.0

```{shell}
pip install -r requirments.txt
```

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

## Scripts

Below is a brief summary of each of the scripts.
If you want to fully regenerate the results, clean out the `~/data` and `~results` folders then run the scripts in the order listed.

1. [get_list_of_votes.py](./get_list_of_votes.py).
   This script will get the list of votes from [govtrack.us](govtrack.us) starting in 1990 and ending in 2020.
   This script will produce the temporary folder `~/data/raw/list_of_votes` necessary for ofline processing.
