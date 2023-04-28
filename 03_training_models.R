library(tidyverse)
library(tidymodels)

data <- read_delim("./data/processed_abstracts.csv", delim = "\t")

data_splits <- initial_split(data, prop = 0.8, strata = gene_type)
data_train <- training(data_splits)
data_test <- testing(data_splits)

library(textrecipes)
library(themis)

custom_filter <- function(word) {
  word = tolower(word)
  word = str_trim(word)
  len = str_length(word)
  
  # Keeping only words that contain at least one letter
  v1 <- str_detect(word, "[A-Za-z]")
  # Keeping words with three or more letters
  v2 <- len > 2
  # Removing words that start with a number
  v3 <- str_starts(word, "[0-9]", negate = TRUE)
  # Removing words that contain whitespace
  v4 <- str_detect(word, "\\s+", negate = TRUE)
  # Removing words containing specific pieces of punctuation
  v5 <- str_detect(word, "\\.", negate = TRUE)
  v6 <- str_detect(word, "\\_", negate = TRUE)
  v7 <- str_detect(word, "\\:", negate = TRUE)
  # Removing any words with 9 or more letters that contain a number
  v8 <- !(str_detect(word, "[0-9]") & (len > 8))
  
  all(v1, v2, v3, v4, v5, v6, v7)
}

data_recipe <- recipe(gene_type ~ abstract, data = data_train) %>%
  step_tokenize(all_predictors()) %>%
  step_stopwords(all_predictors()) %>%
  step_tokenfilter(all_predictors(), filter_fun = custom_filter) %>%
  step_stem(all_predictors()) %>%
  step_tokenfilter(all_predictors(), max_tokens = 1000) %>%
  step_tfidf(all_predictors()) %>%
  step_normalize(all_predictors()) %>%
  step_downsample(gene_type)

library(agua)

doParallel::registerDoParallel()

h2o_start()

auto_spec<- auto_ml() %>%
  set_engine("h2o", max_runtime_secs = 1800) %>%
  set_mode("classification")

auto_wf <- workflow() %>%
  add_model(auto_spec) %>%
  add_recipe(data_recipe)

auto_fit <- fit(auto_wf, data = data_train)