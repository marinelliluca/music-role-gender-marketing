# A Multimodal Understanding of the Role of Sound and Music in Gendered Toy Marketing

Luca Marinelli<sup>1</sup>, Petra Lucht<sup>2</sup>, Charalampos Saitis<sup>1</sup>

<sup>1</sup>Centre for Digital Music, Queen Mary University of London, United Kingdom

<sup>2</sup>Center for Interdisciplinary Women’s and Gender Studies, Technical University of Berlin, Germany

**Manuscript currently under revision.**

## Abstract
> Literature in music theory and psychology shows that, even in isolation, musical sounds can reliably encode gender-loaded messages. In fact, musical material can be imbued with many ideological dimensions and gender is just one of them. Nonetheless, studies of the gendering of music within multimodal communicative events are sparse and lack an encompassing theoretical framework. The present study attempts to address this literature gap by means of a critical quantitative analysis of music in gendered toy marketing, which integrated a content analytical approach with multimodal affective and music-focused perceptual responses. Ratings were collected on a set of 606 commercials spanning over a ten years time frame, and strong gender polarisation was observed in nearly all of the collected variables. Gendered music styles in toy commercials were found to exhibit synergistic design choices, as music in masculine-targeted adverts was substantially more abrasive---louder, more inharmonious, and more distorted---than that in feminine-targeted ones.  Toy advertising music appeared thus to be deliberately and consistently in line with traditional gender norms. In addition, music perceptual scales and voice-related content analytical variables were found to explain quite well the heavily polarised affective ratings. This study presents an empirical understanding of the gendering of music as constructed within multimodal discourse, reiterating the importance of the sociocultural underpinnings of music cognition. We provide a public repository with all code and data necessary to reproduce the results of this study at github.com/marinelliluca/music-role-gender-marketing.

## Quick guide
- For Table 1 (contingency tables) refer to `nb_2_contingency_tables.ipynb` in the main folder
- For the inter-rater agreement of the music-focused (`mf` experiment) and of the multimodal ratings (`mm` experiment) refer to `nb1_inter_rater_agreement.ipynb`
- For Table 2 and Table 3 see `nb3_anova_content_analysis.ipynb`
- For Figure 2 and 3 see `nb4_umap.ipynb`
- For the variance inflation factor computed to inform the exploratory factor analysis and factor score regression see `nb5_variance_inflation_factor.ipynb`
- For the exploratory factor analysis see `R_code/exploratory_factor_analysis.R`
- For Krippendorff's alpha of the content analytical variables see `R_code/compute_krippendorffs_alpha.Rmd`
- For the factor score regression (via principal axis extraction) see `R_code/principal_axis_regression.Rmd`

## Interactive maps
- https://marinelliluca.github.io/mf-interactive.html
- https://marinelliluca.github.io/mm-interactive.html
