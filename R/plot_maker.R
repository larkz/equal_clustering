require(ggplot2)

# setwd("/Users/eric/code/equal_clustering/R")

kmin <- 3
kmax <- 7

carsharing_data <- read.csv(file = '../summary_output/car-sharing-9999_summary.csv', header = FALSE)
carsharing_data$dataset <- "CS"
colnames(carsharing_data) <- c("k", "MSE", "dataset")
carsharing_data$k <- int(carsharing_data$k)
carsharing_data <-carsharing_data[carsharing_data$k <= kmax && carsharing_data$k >= kmin , ]