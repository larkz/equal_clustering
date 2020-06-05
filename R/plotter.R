require(ggplot2)

# setwd("/Users/eric/code/equal_clustering/R")

kmin <- 3
kmax <- 7

carsharing_data <- read.csv(file = '../summary_output/car-sharing-9999_summary.csv', header = FALSE)
carsharing_data$dataset <- "CS"
colnames(carsharing_data) <- c("k", "MSE", "dataset")
carsharing_data$k <- int(carsharing_data$k)
carsharing_data <-carsharing_data[carsharing_data$k <= kmax && carsharing_data$k >= kmin , ]

carsharing_data$MSE <- carsharing_data$MSE / max(carsharing_data$MSE)
starbucks_data <- read.csv(file = '../summary_output/starbucks_summary.csv', header = FALSE)
starbucks_data$dataset <- "SB"

nywifi_data <- read.csv(file = '../summary_output/ny-wifi_summary.csv', header = FALSE)
nywifi_data$dataset <- "NW"
colnames(nywifi_data) <- c("k", "MSE", "dataset")
nywifi_data <-nywifi_data[nywifi_data$k >= kmin, ]
nywifi_data <-nywifi_data[nywifi_data$k <= kmax, ]
nywifi_data$MSE <- nywifi_data$MSE / max(nywifi_data$MSE)

summary_data <- rbind(carsharing_data, nywifi_data)
colnames(summary_data) <- c("k", "MSE", "dataset")

p <- ggplot(summary_data, aes(x=k, y=MSE, group=dataset)) +
  geom_line(aes(color=dataset))+
  geom_point(aes(color=dataset))
p

