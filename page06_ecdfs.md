---
layout: page
title: Predictive ECDFs
permalink: ecdfs
sidebar: true
interactive1: interactive_ecdf.html
interactive2: interactive_diffs.html
---

---

We draw 10000 samples from the Gamma distribution and sum of 2 exponential random variables and plot the predictive ECDFs to assess model performance graphically.

We can also plot the 95% regions with the difference of ECDFs to better observe the differences between the distributions

Looking at the ECDF plots, the observed values for the Gamma distribution lie more within the 95% confidence region, which indicates that it is a better model for predicting the observed data.

<!-- The below line includes the interactive figure. Do not change! -->

{% include_relative interactives/{{page.interactive1}} %}

{% include_relative interactives/{{page.interactive2}} %}
