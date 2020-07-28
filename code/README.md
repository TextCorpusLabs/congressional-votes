Below can be found a list of data manulipation scripts that help make this work posible.

## Packages/Modules

> Describe what programing language you use.
> Is it R, Python, both?
> Also add in the version.
> Make sure you add in the version of packages/modules you are using then add the install script to setup the enviorment. 

All scripts have been tested on Python 3.8.2.
The below modules are needed to run the scripts.
The scripts were tested on the noted versions, so YMMV.
**Note**: not all modules are required for all scripts.
If this it the first time running the scripts, the modules will need to be installed.
They can be installed by navigating to the `~/code` folder, then using the below code.

> I recomend using the `requirments.txt` when you write in Python.

> I like listing out requirements in alpha sort order.
> I find it is easer to see if they are already in the list that way.

* nltk 3.4.5
* progressbar2 3.47.0

```{shell}
pip install -r requirments.txt
python -c "import nltk;nltk.download('punkt')"
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

> List out and number all the files found in this folder.
> Give a brief discription of what there intended effects are.
> Do they cleanup data or perform an analysis?
> What files will they generate?
> They need not be in any particular order, but if you change the number, remember to update the main `~/README.md` file.

1. Run the [Analysis](./analysis_1_of_n.rmd).
   This will produce the table `~/results/analysis_1_of_n.RMD` and figure `~/results/analysis_1_of_n.jpg`.
