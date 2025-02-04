library(dplyr)
library(tidyr)

# Read the csv file
df <- read.csv("data_exp_136114-v2_task-knqe.csv")

# Identify Participant Public ID with more than 20 NAs in any of the columns
filter_ids <- df %>%
  group_by(`Participant.Public.ID`) %>%
  summarise(across(c(t_response, choice, rt, gain, loss, score.tally), ~sum(is.na(.)) > 20), .groups = "drop") %>%
  rowwise() %>%
  mutate(exclude = any(c_across(-1))) %>% # exclude the first column (Participant Public ID)
  filter(exclude) %>%
  pull(`Participant.Public.ID`)

# Remove these participants from the original dataframe
df_cleaned <- df %>%
  filter(!(Participant.Public.ID %in% filter_ids))

# Now, for participants with fewer than 20 NAs, we remove only those rows where NA appears
df_cleaned <- df_cleaned %>%
  drop_na(t_response, choice, rt, gain, loss, score.tally)

# Write the cleaned data into a csv file
write.csv(df_cleaned, "cleaned_data.csv", row.names = FALSE)



