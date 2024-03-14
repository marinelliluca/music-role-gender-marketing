library(paran)
library(readr)
library(psych) # rdocumentamion.org/packages/psych/versions/2.2.5/topics/fa
library(MVN)
library(EFA.dimensions)
library(dplyr)
library(GPArotation)
library(flexmix)

experiment <- "mf"
aggregator <- "mean"
fpath <- sprintf("%s_%s_ratings_for_R.csv", 
                 experiment,
                 aggregator)

scales_and_targets <- read_csv(fpath)

# Let's drop "Heavy/Light" as it is extremely co-linear
scales_and_targets <- scales_and_targets[ , !names(scales_and_targets) %in% "Heavy_Light"]

if (experiment == "mm"){
  scales_columns <- c(2:8)
  cor_method <- "pearson"
  initial_communalities <- c(0.9, 0.4, 0.66, 0.8, 0.8, 0.6, 0.65)
} else if (experiment == "mf"){
  scales_columns <- c(2:15)
  cor_method <- "spearman"
  initial_communalities <- c(0.67, 0.76, 0.47, 0.74, 0.75, 0.54, 0.76, 
                             0.77, 0.88, 0.53, 0.41, 0.48, 0.74, 0.78)
}


all_commercials_scales <- scales_and_targets[,scales_columns]

masc_commercials_scales <- all_commercials_scales[scales_and_targets$target=='masc',]
fem_commercials_scales <- all_commercials_scales[scales_and_targets$target=='fem',]
mix_commercials_scales <- all_commercials_scales[scales_and_targets$target=='mix',]


# KMO(r=cor(all_commercials_scales, method=cor_method))
# cortest.bartlett(all_commercials_scales)
# result <- mvn(all_commercials_scales, mvnTest="mardia")
# print(result$multivariateNormality)
# 
# parallel <- paran(all_commercials_scales,
#                   iterations=5000,
#                   cfa= TRUE,
#                   centile=95,
#                   all=TRUE,
#                   graph=TRUE) # graph=TRUE
# #print(parallel$AdjEv)
# 
# fa_mod <- fa(r=cor(all_commercials_scales, method=cor_method),
#              nfactors = parallel$Retained,
#              fm="pa", # factoring method, principal axis
#              max.iter=5000,
#              rotate="oblimin",
#              n.obs=nrow(all_commercials_scales))
# 
# #fa.diagram(fa_mod)
# print(fa_mod)

cor_mat <- cor(fem_commercials_scales, method=cor_method)
n_obs <- nrow(fem_commercials_scales)

KMO(r=cor_mat)
cortest.bartlett(fem_commercials_scales)
result <- mvn(fem_commercials_scales, mvnTest="mardia")
print(result$multivariateNormality)

parallel <- paran(mat = cor_mat, 
                  n = n_obs,
                  iterations=5000, 
                  cfa= TRUE, 
                  centile=95, 
                  all=TRUE, 
                  graph=TRUE)
#print(parallel$AdjEv)

if (experiment == "mm"){
  nfactors <- parallel$Retained
} else if (experiment == "mf"){
  nfactors <- parallel$Retained # i.e., 3 factors
}


fa_mod <- fa(r=cor_mat, 
             nfactors = nfactors,
             fm="pa", # factoring method, principal axis
             SMC=initial_communalities, # from the above FA on the entire set
             max.iter=5000,
             rotate="oblimin",
             n.obs=n_obs)
#fa.diagram(fa_mod)
print(fa_mod)



cor_mat <- cor(masc_commercials_scales, method=cor_method)
n_obs <- nrow(masc_commercials_scales)

KMO(r=cor_mat)
cortest.bartlett(masc_commercials_scales)
result <- mvn(masc_commercials_scales, mvnTest="mardia")
print(result$multivariateNormality)

parallel <- paran(mat = cor_mat, 
                  n = n_obs, 
                  iterations=5000, 
                  cfa= TRUE, 
                  centile=95, 
                  all=TRUE, 
                  graph=FALSE)
#print(parallel$AdjEv)

if (experiment == "mm"){
  nfactors <- parallel$Retained
} else if (experiment == "mf"){
  nfactors <- parallel$Retained # i.e., 4 factors
}

fa_mod <- fa(r=cor_mat, 
             nfactors = nfactors, 
             fm="pa", # factoring method, principal axis
             SMC=initial_communalities, # from the above FA on the entire set
             max.iter=5000,
             rotate="oblimin",
             n.obs=n_obs)
#fa.diagram(fa_mod)
print(fa_mod)


cor_mat <- cor(mix_commercials_scales, method=cor_method)
n_obs <- nrow(mix_commercials_scales)

KMO(r=cor_mat)
cortest.bartlett(mix_commercials_scales)
result <- mvn(mix_commercials_scales, mvnTest="mardia")
print(result$multivariateNormality)

parallel <- paran(mat = cor_mat, 
                  n = n_obs,
                  iterations=5000, 
                  cfa= TRUE, 
                  centile=95, 
                  all=TRUE, 
                  graph=FALSE)
#print(parallel$AdjEv)

if (experiment == "mm"){
  nfactors <- parallel$Retained
} else if (experiment == "mf"){
  nfactors <- parallel$Retained # from the comparison of BIC values
}

fa_mod <- fa(r=cor_mat,
             nfactors = nfactors, # parallel$Retained, 
             fm="pa", # factoring method, principal axis
             SMC=initial_communalities, # from the above FA on the entire set
             max.iter=5000,
             rotate="oblimin",
             n.obs=n_obs)
#fa.diagram(fa_mod)
print(fa_mod)






