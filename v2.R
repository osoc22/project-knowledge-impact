library(httr)
library(jsonlite)
library(stringr) 

API_URL <- "https://w3id.org/oc/index/api/v1"
endpoint <- "/citations/"

#doi <- "10.1080/02650487.2021.1963554"

#FIRST: set path to folder with v2.R and doi.csv with setwd()
#setwd('')

dois <- read.csv("doi.csv") #download all dois
doi <-dois$doi[1]

#get citing papers
response <- httr::GET(url=paste0(API_URL, endpoint, doi))
raw <- httr::content(response, as="text")
data <- jsonlite::fromJSON(raw, flatten = TRUE)

#get dois of citing papers
doi_citing <- data$citing #choose column of interest
doi_citing_clean <- c() 
for (i in doi_citing){
doi_citing_clean <- c(doi_citing_clean, str_replace(i, 'coci => ', '')) #generate new 'clean' vector of dois
}

#get times citing papers are cited
matriz <- matrix(nrow = length(doi_citing_clean), ncol = 2)
#rownames(matriz) <- doi_citing_clean
j <- 1
for (i in doi_citing_clean) {
  response <- httr::GET(url=paste0(API_URL, endpoint, i))
  raw <- httr::content(response, as="text")
  data <- jsonlite::fromJSON(raw, flatten = TRUE)
  matriz[j,1] <- i
  if (is.null(nrow(data))==TRUE){matriz[j,2] <- 0} #if its null, then 0
  else {matriz[j,2] <- as.numeric(nrow(data))}
  j <- j+1 
}

colnames(matriz) <- c('doi', 'times_cited')

#sort by column (doesnt rly work -> need to set datatype 'times_cited' as int)
matriz_sorted <- matriz[order(matriz[,'times_cited'],decreasing=FALSE),]
v <- lapply(matriz[,'times_cited'],as.numeric)

#store ordered ids of recs
id <- c()
for (elem in matriz_sorted[ ,1]){
  row <- which(dois == elem, arr.ind=TRUE)[1]
  
  if (is.null(row) == FALSE){
    id <- c(id, dois$id[row])} #returns id associated with dois ordered
}

id_not_null<-id[!is.na(id)] #id associated with dois ordered without nulls

