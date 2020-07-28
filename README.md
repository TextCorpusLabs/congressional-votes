# Repo Template

> You should think of GitHub as your modern research journal.
> It is a place to write down your observations, leave notes as to what worked and what didn't, and automate any process you may have.
> This repository template is intended to help collect your thoughts in a why to help others reproduce your work and learn from it.
> Describe the purpose of the project.
> What result does it demonstrate?
> What tools/techniques does it use?
> What are the key points others should learn.

## Tabula Rasa

> Any type of research process will have some amount of steps that are taken to produce the result.
> When a new researcher joins your team they should be able to read through the steps provided here and get up to speed with where the research stands.
> There might be other prior works they need, just link them.

The below steps can be taken to "re-play" the project's process.
Each step may refer to a different README.
In these cases, the step in that README will aslo be noted.
It is recommended you read the full README as sometimes a step may contain a shortcut or other prior assumed knowledge.

When the work is still _in-progress_ a note of TODO, DOING, DONE should be added to the front

01. Get the raw data.
    [Data instructions](./data/README.md)(step 1...N).
02. Describe some steps that need to be run
    [Code instructions](./code/README.md)(script 1...M).
03. Describe more steps that need to be run
    [Code instructions](./code/README.md)(script M+1...N).
04. Knit the paper.
    [Paper instructions](./paper/README.md)(script 1-2).


## Prerequisites

> I work primarily in Microsoft Windows.
> That bias shows through here.
> If you want to help others through specific processes for a different OS, feel free.

The following packages need to be installed.
You can use any method to install the prerequisites.
I recommend using [Chocolatey](https://chocolatey.org/install).
If you decide to use Chocolatey, open an _admin_ PowerShell prompt and run the code snipet below.

* [Python](https://www.python.org/downloads/)
* [R](https://cran.r-project.org/bin/windows/base/) + [R Studio](https://www.rstudio.com/products/rstudio/download/)
  
```{ps1}
if('Unrestricted' -ne (Get-ExecutionPolicy)) { Set-ExecutionPolicy Bypass -Scope Process -Force }
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
refreshenv
choco install python3 -y
refreshenv
choco install r.project -y
refreshenv
choco install r.studio -y
```

> While humans can't tell the difference, when working with Markdown (or R Markdown) make sure every sentence is on a single line and the last line in a document is empty.
> This will make any automatic diffing tool work a lot better.
