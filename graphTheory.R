library(Matrix)
occur <- readMM("occurence.mtx")
edges <- summary(occur)
edges <- as.matrix(edges)

library(igraph)
graph = graph_from_edgelist(edge[,-1], directed=FALSE)



#source("https://bioconductor.org/biocLite.R")
#biocLite("RBGL")
library(RBGL)
library(graph)
library(SparseM)
hcs <- highlyConnSG(g, sat=5)


test <- graphAM-class(adjMat=A)

graph <- graphNEL(nodes=dat,edgeL=A)

dat = readLines("features.txt")
g<-sparseM2Graph(sM=A,nodeNames = dat, edgemode="undirected")

A <- as.matrix.csr(occur, nrow=dim(occur)[1], ncol=dim(occur)[1])

#########################################
library(Matrix)
library(RBGL)
library(graph)
library(SparseM)

occur <- readMM("occurence.mtx")
A <- as.matrix.csr(occur, nrow=dim(occur)[1], ncol=dim(occur)[1])
dat = readLines("features.txt")
g <- sparseM2Graph(sM=A,nodeNames = dat, edgemode="undirected")

A<-as.matrix(A)
g <- graphAM(adjMat=A, edgemode='undirected')# A must be symmetric
