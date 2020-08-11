# --- Load Required Packages ---

library(data.table)
library(readtext)
library(dplyr)
library(plyr)
library(stringr)
library(tm)
library(filenamer)
library(stringr)
library(R.utils)
library(udpipe)

rm(list = ls())
options(scipen = 999)

# --- List Data Files ---

list_of_txt <-
  list.files(
    path = "data/.",
    recursive = TRUE,
    pattern = "\\.txt$",
    full.names = TRUE) %>%
  data.frame(txtfile = ., stringsAsFactors = F) %>%
  mutate(
    path = sapply(txtfile, function(z){paste0(as.filename(z)$path, collapse = '/')})
  )

list_of_csv <-
  list.files(
    path = "data/.",
    recursive = TRUE,
    pattern = "\\.csv$",
    full.names = TRUE) %>%
  data.frame(csvfile = ., stringsAsFactors = F) %>%
  mutate(
    path = sapply(csvfile, function(z){paste0(as.filename(z)$path, collapse = '/')})
  )

list_of_files <-
  list_of_txt %>%
  left_join(list_of_csv)

rm(list_of_txt, list_of_csv)

# --- Load Data ---

text <- lapply(list_of_files$txtfile, readtext::readtext)
csv <- lapply(list_of_files$csvfile, read.csv, header = T, sep = ",", skip = 1, stringsAsFactors = F)
path <- list_of_files$path
rm(list_of_files)

# --- classify data ---

class <- vector(mode = 'numeric', length = length(csv))
for(i in seq_along(csv)) {
  data <- csv[[i]]
  data <-
    data %>%
    mutate(vote = tolower(vote)) %>%
    mutate(vote = ifelse(vote %in% c('yea', 'aye'), 1, 0))
  class[i] <- sum(data$vote)/nrow(data) > .5
  rm(data)
}
rm(csv, i)

# --- frame data ---

tmp <- vector(mode = 'character', length = length(text))
for(i in seq_along(text)) {
  data <- text[[i]]
  tmp[i] <- data$text[1]
  rm(data)
}
text <- tmp
rm(tmp, i)

data.full <- data.frame(class, path, text, stringsAsFactors = F)
rm(class, path, text)

# -- balance classes --


# Create an equal number of 1 and 0 classes in the dataset. 
# Splitting Subsets to 
split_0 <- data.full %>% filter(class == 0)
split_1 <- data.full %>% filter(class == 1)
rm(data.full)

mn <- min(nrow(split_0), nrow(split_1))

set.seed(1)

data.balanced <-
  rbind(
    split_0 %>% sample_n(mn),
    split_1 %>% sample_n(mn)) %>%
  sample_n(mn * 2)

rm(split_0, split_1, mn)

# --- Annotate Text ---

## Data pre-processing text for annotation process.

data.preprocessed <-
  data.balanced %>%
  mutate(text = tolower(text)) %>%
  mutate(text = iconv(text, "latin1", "ASCII", sub = " ")) %>%
  mutate(text = gsub("^NA| NA ", " ", text)) %>%
  mutate(text = tm::stripWhitespace(text))

## Add document id for aggregating to the annotated data. 
data.preprocessed = cbind(data.preprocessed,c(1:length(data.preprocessed$text)))
colnames(data.preprocessed) = c('class','path','text','doc_id')
str(data.preprocessed)

# - [4] - Annotation of the texts ----
dl = udpipe_download_model(language = "english-ewt") #download the language model required...
annotate = udpipe(data.preprocessed$text, "english-ewt") #annotate the texts...
ann.df = as.data.frame(annotate) #store as a dataframe...
str(ann.df) #structure of dataframe...

## Loop through to concatenate token + upos into unique sentences...
p <- function(v) {
  Reduce(f=paste0, x = v)
}

for(i in seq_along(length(ann.df$sentence_id))) {
  lab.tok = (c(paste(ann.df$token, ann.df$upos))) #combine tokens and upos...
  mod.df = data.frame(ann.df, lab.tok) #convert into a df...
  colnames(mod.df) = c('doc_id','paragraph_id',"sentence_id",'sentence','start','end','term_id','token_id',"token",'lemma', 
                       "upos",'xpos','feats','head_token_id',"dep_rel","deps","misc","upos.labels") #relabel columns of df...
  mod.df$upos.labels = as.character(mod.df$upos.labels) #convert token_upos to characters...
  mod.df1 = aggregate(upos.labels~sentence_id, data = mod.df, paste0, collapse=" ") #aggregate df
  mod.df2 = merge(mod.df, mod.df1, by = "sentence_id", all = T) #merge mod.df and mod.df1 into 1 df... 
  colnames(mod.df2) = c('doc_id','paragraph_id',"sentence_id",'sentence','start','end','term_id','token_id',"token",'lemma', 
                        "upos",'xpos','feats','head_token_id',"dep_rel","deps","misc","token_upos", "sent_upos") #relabel columns of df...
}
str(mod.df2)

# --- Data Pre-processing ---

data.preprocessed <-
  data.preprocessed %>%
  mutate(text = tm::removeWords(text, stopwords(kind = "SMART"))) %>%
  mutate(text = tm::removePunctuation(text)) %>%
  mutate(text = tm::removeNumbers(text)) %>%
  mutate(text = tm::stemDocument(text))
str(data.preprocessed)

# --- Aggregate the Datasets together
data.final = data.preprocessed %>% inner_join(mod.df2, by=c("doc_id","doc_id"))
data.final = data.final[,-c(5:21)]
data.final = na.omit(data.final)
data.final = unique(data.final, by = 'text')
str(data.final)

# ---- clean up sent.upos text 
data.save <-
  data.final  %>%
  mutate(sent_upos = tolower(sent_upos)) %>%
  mutate(sent_upos = iconv(sent_upos, "latin1", "ASCII", sub = " ")) %>%
  mutate(sent_upos = gsub("^NA| NA ", " ", sent_upos)) %>%
  mutate(sent_upos = gsub('[_]+', " ", sent_upos)) %>%
  mutate(sent_upos = tm::stripWhitespace(sent_upos)) %>%
  mutate(sent_upos = tm::removeWords(sent_upos, stopwords(kind = "SMART"))) %>%
  mutate(sent_upos = tm::removePunctuation(sent_upos)) %>%
  mutate(sent_upos = tm::removeNumbers(sent_upost)) %>%
  mutate(sent_upos = tm::stemDocument(sent_upos))
str(data.save)


write.csv(data.save, "results/cong.roll.call.data.csv", row.names = F)