## global.R ##
library(dplyr)
library(ggplot2)
library(lazyeval)

soundcloud = read.csv('soundcloud.csv', header = TRUE)
soundcloud$genre = as.character(soundcloud$genre)
soundcloud$comment_content = as.character(soundcloud$comment_content)


#Save list of genres
genres = unique(soundcloud$genre)


