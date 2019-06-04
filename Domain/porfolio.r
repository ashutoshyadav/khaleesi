library(nloptr)
library(RiskPortfolios)
library(quantmod)
library(fPortfolio)

args<-commandArgs(TRUE)
returns = read.csv(args[1])

# Compute variance-covariance matrix 
colnum=ncol(returns)


rets=data.matrix(returns,rownames.force = NA)
mu = meanEstimation(rets)



Sigma = covEstimation(rets)

# Semi-deviation estimation
semiDev = semidevEstimation(rets)

# Minimim volatility portfolio with the long-only constraint

##### min variance
mvol=optimalPortfolio(Sigma = Sigma, 
                      control = list(type = 'minvol', constraint = 'user', LB = rep(0.0, colnum), UB = rep(1.00, colnum)))

# Aman Equal-risk-contribution portfolio with the long-only constraint
ercp=optimalPortfolio(Sigma = Sigma, 
                      control = list(type = 'erc', constraint = 'user', LB = rep(0.0, colnum), UB = rep(1.00, colnum)))

#Aman max dec
# Maximum decorrelation portoflio with the long-only constraint
maxdec=optimalPortfolio(Sigma = Sigma, 
                        control = list(type = 'maxdec', constraint = 'user', LB = rep(0.0, colnum), UB = rep(1.00, colnum)))

#Aman Max Sharpe 
constts="maxW[1:colnum]=1.00"
assetsNames=colnames(rets)
tport=tangencyPortfolio(as.timeSeries(rets),constraints=constts)#"LongOnly",maxW=1.00)

maxsharpe=getWeights(tport)

array1n=matrix(1/colnum,colnum,1)
colnames(array1n, do.NULL = TRUE, prefix = "col")
colnames(array1n) <- "EW"

weightsvalue20=cbind(ercp,maxdec,mvol,maxsharpe,array1n)
print(weightsvalue20)
