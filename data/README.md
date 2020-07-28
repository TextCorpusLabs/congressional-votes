> In general, I like caching a local copy of the data up in releases (see below).
> Sometimes it makes more sense to refer to the original source and leave it at that.
> Choose what works best for your project.
> One of the nice things about working in GitHub is that you can also refer to other projects.
> It might be that you are using another researcher's data set, or even a prior data set that you made.
> In those cases, just link to their data sections and them use the rest of this document to describe what new efforts you bring to the party.

The original package can be downloaded by hand from [Kaggle](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge).
The original bill text _can_ be downloaded by hand from [congress.gov](https://www.congress.gov).
For convenience, we keep a 2nd copy of all the data gzip'ed in [releases][releases].
We need to source the data locally for everyone because GitHub has storage limits that we don't want to cross.

## Steps

> GitHub lets you keep up to a _total_ of 1 GB of files in your repository with a single file being no bigger than 100MB.
> However, it allows you to keep 100GB of data in your releases section.
> This artificial limit helps you in terms of data quality when you consider GitHub to be your research journal.
> As you are making your observations, they become fixed.
> You certainly don't want to commit data fraud by going back and updating the data.

> Because of this, I strongly recommend keeping all your data compressed and in the Releases section of your Repository.
> Each step below should tell you what file to bring down and place in _this_ folder.
> Using this process, you get around most of the slow bloated repository issues, while still being able to write your code with relative paths.
> Trust me, others will thank you for not referring to a particular directory on your personal computer.

> In general nothing (other than this file) should be stored in the `~/data` directory when viewed in GitHub.

1. Retrieve the dataset _by hand_.
   Click on the [download](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/download) link, saving the file to `~/data/raw`
2. Extract the data in-place
   1. right click the file, select '7-zip', select 'Extract Here'

## Shortcuts

[GitHub](https://github.com) has some issues when dealing with [large files](https://help.github.com/en/articles/working-with-large-files).
The [recommended method](https://help.github.com/en/articles/distributing-large-binaries) for dealing with large files is to store them in [releases][releases].
You can find the gzip'ed versions of the below there.
Any of the steps can be skipped by downloading the correct file from [releases][releases] and proceding from that point forward.

[releases]: https://github.com/MindMimicLabs/{project}/releases
