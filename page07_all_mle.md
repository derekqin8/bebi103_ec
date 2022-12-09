---
layout: page
title: All MLEs
permalink: all_mles
sidebar: true
interactive: interactive_all_mle.html
---

---

After determining that the Gamma model is a better model for the dataset, we can compute and compare the MLEs produced for all tubulin concentrations.

According to the plot of MLE predictions vs tubulin concentration above, the MLE 𝛽 values are approximately the same, indicating that the rate of a catastrophe event is generally the same for all concentrations. For MLE 𝛼 , there are not enough data points to get a clear idea of the trend. If we consider that there is no trend, then there is no apparent correlation between the concentration of tubulin and the catastrophe time.

However, if we consider 𝛼 to have a general upwards trend ( 𝛼 increases as tubulin concentration increases), then we have a different interpretation. According to the Gamma distribution "story," 𝛼 is the number of arrivals of Poisson processes, in this case microtubule catastrophe events, at 𝛽 time per arrival. Then, since 𝛽 is consistent for all concentrations, it must take longer for a microtubule catastrophe event to occur at higher concentrations than at lower concentrations. This is consistent with the increased rate of polymerization at higher tubulin concentrations because the presence of more tubulin enables faster growth of microtubules. Logically, if the growth of microtubules is faster, then the catastrophe would be slower since the catastrophe would be counteracted by favoring growth.

<!-- The below line includes the interactive figure. Do not change! -->

{% include_relative interactives/{{page.interactive}} %}
