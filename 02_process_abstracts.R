library(tidyverse)

raw_data <- read_delim("./data/mutation-abstracts.csv", delim = "\t") %>%
  select(pubmed_id, title, abstract, gene, gene_type)

data <- raw_data %>%
  group_by(pubmed_id, abstract) %>%
  summarise(
    GOF = sum(gene_type == "GOF"),
    LOF = sum(gene_type == "LOF"),
    log_score = log2(GOF/LOF)
  ) %>%
  filter(
    abs(log_score) >= 2
  ) %>%
  mutate(
    gene_type = ifelse(log_score > 0, "GOF", "LOF")
  ) %>%
  select(pubmed_id, abstract, gene_type)

write_delim(data, "./data/processed_abstracts.csv", delim = "\t")
