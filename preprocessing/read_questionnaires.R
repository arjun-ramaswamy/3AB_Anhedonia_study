library(tidyverse)
library(ggpubr)
library(GGally)
library(cowplot)
library(ggplot2)
theme_set(theme_pubclean())
theme_update(panel.grid.major.y = element_blank())

## GAD score calculation ##
gad = read.csv('gad_questionnaire.csv')


gad$Response <-
  gad$Response %>%
  dplyr::recode('1'='0',
                '2'= '1',
                '3'='2',
                '4'='3') %>%
  as.integer()

gad_scores <- gad %>% 
  filter(str_detect(Question.Key, "quantised")) %>% 
  filter(!str_detect(Question.Key, "GAD_8")) %>% 
  mutate(Response = as.numeric(Response)) %>% 
  group_by(Participant.Public.ID) %>% 
  summarise(gad_score = ifelse(any(str_detect(Question.Key, "GAD_attention") & Response == 1), 
                               NA, 
                               sum(ifelse(!str_detect(Question.Key, "GAD_attention"), 
                                          Response, 
                                          0))))

#filter(!str_detect(Question.Key, "GAD_attention")) %>% 
## end of section ##

## SHAPS score calculation ##
shaps = read.csv('shaps_questionnaire.csv')

shaps$Response <-
  shaps$Response %>%
  dplyr::recode('1'='1',
                '2'= '1',
                '3'='0',
                '4'='0') %>%
  as.integer()

shaps_scores <- shaps %>% 
  filter(str_detect(Question.Key, "quantised")) %>% 
  mutate(Response = as.numeric(Response)) %>% 
  group_by(Participant.Public.ID) %>% 
  summarise(shaps_score = ifelse(any(str_detect(Question.Key, "SHAPS_attention") & (Response == 1 | Response == 2)), 
                                 NA, 
                                 sum(ifelse(!str_detect(Question.Key, "SHAPS_attention"), 
                                            Response, 
                                            0))))

## end of section ##

## ZUNG score calculation ##

zung = read.csv('zung_questionnaire.csv')

zung_scores <- zung %>% 
  filter(str_detect(Question.Key, "quantised")) %>% 
  mutate(Response = as.numeric(Response)) %>% 
  group_by(Participant.Public.ID) %>% 
  summarise(zung_score = ifelse(any(str_detect(Question.Key, "SDS_attention") & (Response == 3 | Response == 4)), 
                                 NA, 
                                 sum(ifelse(!str_detect(Question.Key, "SDS_attention"), 
                                            Response, 
                                            0))))

## end of section ##


## DARS score  calculation ##

dars = read.csv('dars_questionnaire.csv')

dars$Response <-
  dars$Response %>%
  dplyr::recode('1'='0',
                '2'='1',
                '3'='2',
                '4'='3',
                '5'='4') %>%
  as.integer()

dars_scores = dars %>%
  filter(str_detect(`Question.Key`, 'quantised')) %>%
  group_by(`Participant.Public.ID`) %>%
  summarise(dars_score = Response %>% as.numeric %>% sum)

## end of section ##

## combine all questionnaire scores ##

df_list <- list(dars_scores, gad_scores, shaps_scores, zung_scores)
df <- df_list %>% reduce(full_join, by='Participant.Public.ID')
write.csv(df, 'all_questionnaire_scores.csv')

## Visualization ##
df <- read.csv('all_questionnaire_scores.csv')
ggpairs(df[,3:6])

my_func <- function(data, mapping, ...) {
  
  ggplot(data, mapping) + 
    geom_point(size = 1) +
    geom_smooth(formula = y~x, method = loess, fill="skyblue", color = "skyblue") +
    geom_smooth(formula = y~x, method = lm, fill="salmon", color = "salmon")
    
}
  
ggpairs(df[, 3:6], lower = list(continuous = my_func))

#ggpairs(df[, 3:6], upper = list(continuous = wrap("cor", size = 5)), lower = list(continuous = "smooth"))


#########Dont forget to remove people with NA (i.e. failed attention checks) scores for any of the questionnaires#######


#stats between SHAPS and DARS
data <- read.csv('all_questionnaire_scores.csv')
subset <- data[, c("Participant.Public.ID","dars_score","shaps_score")]
View(subset)
subset <- subset(data, shaps_score > 2  & dars_score < 46, 
                 select = c("Participant.Public.ID","dars_score","shaps_score"))

#num_participants <- sum(subset$shaps_score == 0 & subset$dars_score > 55)
num_participants <- sum(subset$shaps_score > 2 & subset$dars_score < 46)
cat("Number of participants satisfying both conditions:", num_participants)
