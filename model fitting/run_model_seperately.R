library(hBayesDM)
library(dplyr)
library(rstan)
library(tidyverse)
library(brms)


df <- read.csv("non_anhedonic_cleaned_data.csv")


# tell me more details of the hBayesDM package
?hBayesDM

arjun.data <- 
  df %>%
  select(Participant.Public.ID, trial_nr,gain,loss, choice) %>% 
  rename(
    subjID = Participant.Public.ID,
    choice = choice,
    gain = gain,
    loss = loss
  ) %>%  # remove from here if full sample
  group_by(subjID) %>% 
  mutate(ID = cur_group_id(),
         trial_nr = trial_nr + 1) %>% 
  ungroup() %>%
  filter(ID %in% 1:5)



arjun.data$choice <-
  arjun.data$choice %>%
  dplyr::recode('0' = '1',
                '1' = '2',
                '2' = '3') %>%
  as.integer()

arjun.data$loss <-
  arjun.data$loss %>%
  dplyr::recode('1' = '-1',
                '0' = '0') %>%
  as.integer()


# check
arjun.data


# fit the Bayesian hierarchical reinforcement learning model

# rule of thumb:
# 1) nwarmup = 1/2 * niter
# 2) nchain = 4
# There are 24 cores on the FIL network
# There are 12 cores on my Mac

rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())
set.seed(1234)

arjun.model <- hBayesDM::banditNarm_4par(data = arjun.data, inc_postpred = TRUE,
                                         niter = 2000,
                                         nwarmup = 1000,
                                         nchain = 4,
                                         ncore = 10)


save(arjun.model,
     file = "arjun.model.Rdata")


df3 <- arjun.model[["allIndPars"]]
write.csv(df3, 'nonanhedonic_modelparameters.csv')
