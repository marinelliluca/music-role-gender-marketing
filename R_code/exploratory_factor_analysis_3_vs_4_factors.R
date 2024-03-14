library(paran)
library(readr)
library(psych)
library(MVN)
library(EFA.dimensions)

# Compare the various models' RMSEA index and the Tucker Lewis Index 
# They are, for 3-factors models, OK (marginal fit) on all and GOOD for fem commercials
# But they are VERY BAD for masc and mixed 

# RMSEA is an estimate of the discrepancy between the model and the data per degree of freedom for the model. 
# It has been suggested that values less than 0.05constitute good fit, values in the 0.05 to 0.08 range 
# acceptable fit, values in the 0.08 to 0.10 range marginal fit, and values greater than 0.10 poor fit.
## FROM Fabrigar et al. (1999). Evaluating the use of exploratory factor analysis in psychological research 

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

fm <- "pa"

# parallel <- paran(all_commercials_scales,
#                   iterations=5000,
#                   cfa= TRUE,
#                   centile=95,
#                   all=TRUE,
#                   graph=FALSE) # graph=TRUE
# 
# fa_mod <- fa(r=cor(all_commercials_scales, method="spearman"),
#              nfactors = parallel$Retained,
#              fm="pa", # factoring method, principal axis
#              max.iter=5000,
#              rotate="oblimin",
#              n.obs=nrow(all_commercials_scales))
# 
# #fa.diagram(fa_mod)
# print(fa_mod)

if (experiment == "mm"){
  initial_communalities <- c(0.9, 0.4, 0.66, 0.8, 0.8, 0.6, 0.65)
} else if (experiment == "mf"){
  initial_communalities <- c(0.67, 0.76, 0.47, 0.74, 0.75, 0.54, 0.76, 
                             0.77, 0.88, 0.53, 0.41, 0.48, 0.74, 0.78)
}

fa_3 <- fa(r=cor(fem_commercials_scales, method="spearman"), 
           nfactors = 4, 
           fm=fm, 
           SMC=TRUE,
           max.iter=1000,
           rotate="oblimin",
           warnings = TRUE,
           n.obs=nrow(fem_commercials_scales))
print(fa_3)
fa_4 <- fa(r=cor(fem_commercials_scales, method="spearman"),
           nfactors = 5,
           fm=fm,
           SMC=TRUE,
           max.iter=1000,
           rotate="oblimin",
           warnings = TRUE)
print(fa_4)
anova.psych(fa_3,fa_4)


fa_3 <- fa(r=cor(masc_commercials_scales, method="spearman"), 
           nfactors = 4, 
           fm=fm, 
           SMC=TRUE,
           max.iter=1000,
           rotate="oblimin",
           warnings = TRUE,
           n.obs=nrow(masc_commercials_scales))
print(fa_3)
fa_4 <- fa(r=masc_commercials_scales,
           nfactors = 5,
           fm=fm,
           SMC=TRUE,
           max.iter=1000,
           rotate="oblimin",
           warnings = TRUE)
print(fa_4)
anova.psych(fa_3,fa_4)



fa_3 <- fa(r=mix_commercials_scales,
           nfactors = 4, 
           fm=fm, 
           SMC=TRUE,
           max.iter=1000,
           rotate="oblimin",
           warnings = TRUE,
           n.obs=nrow(mix_commercials_scales))
print(fa_3)
fa_4 <- fa(r=mix_commercials_scales,
           nfactors = 5,
           fm=fm,
           SMC=TRUE,
           max.iter=1000,
           rotate="oblimin",
           warnings = TRUE)
print(fa_4)
anova.psych(fa_3, fa_4)

