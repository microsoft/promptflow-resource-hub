# Tutorial: Evaluate Semantic Kernel Planner

## Overview

Navigating the dynamic terrain of AI orchestration requires precise evaluation of your plugins and planners. This is where the integration of [semantic kernel](https://github.com/microsoft/semantic-kernel) and [prompt flow](https://github.com/microsoft/promptflow) comes into play. It allows you to not only orchestrate automatically functions on the fly using planner, but also to evaluate your semantic kernel plugins and planners comprehensively for higher quality control and tunning.

Semantic Kernel is an open-source SDK that seamlessly merges AI services with traditional programming languages like C# and Python. Its plugins and planners utilize AI capabilities to optimize operations, thereby improving efficiency and accuracy in planning.

However, as more plugins are added to planners, ensuring their correct operation becomes crucial. While previously this was a manual and time-consuming task, Prompt Flow now enables you to automate this process.

In this tutorial, we guide you on how to:

* Develop a flow: We give the sample flow with Semantic Kernel planner capability including SK curated plugins and custom plugins.
* Golden dataset preparation: We show you how to prepare a golden dataset for the planner evaluation.
* Execute batch tests: We walk you through the pf batch test to generate output of your multi-rows dataset.
* Conduct evaluations: An evaluation flow provided Finally, we show you how to quantitatively assess the accuracy of your planners and plugins.

By following this tutorial, you will gain a practical understanding of the Semantic Kernel Planner and how to effectively incorporate it with Prompt Flow.
