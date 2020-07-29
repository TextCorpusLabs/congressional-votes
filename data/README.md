The origional links and vote tallies can be downloaded by hand from [govtrack.us](https://www.govtrack.us/).
The origional bill text can be downloaded by hand from [congress.gov](https://www.congress.gov/).
For convience, we keep a 2nd copy of all the data gzip'ed in releases.

# Steps

1. Get the [list of votes](../code/get_list_of_votes.py)
   ```{shell}
   python get_list_of_votes.py
   ```

# Shortcuts

[GitHub](https://github.com) has some issues when dealing with [large files](https://help.github.com/en/articles/working-with-large-files).
The [recomended method](https://help.github.com/en/articles/distributing-large-binaries) for dealing with large files is to store them in [releases][releases].
You can find the gzip'ed versions of the below there.
Any of the steps above can be skipped by downloading the correct file and proceding from that point forward.

* [List of Votes](https://github.com/MindMimicLabs/data-congressional-votes/releases/download/1.0/list_of_votes.csv.gz)
  * Download to `~/data` and extract in place
* Vote tally
* Bill text