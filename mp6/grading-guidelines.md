# Machine Project 6 - Grading Guidelines

## Grading Process

### Timelines for Grading

* The day after the regular deadline: grading process starts.
* Five days after the hard deadline: TAs finish grading.
* Within one week after the hard deadline: grades posted to Canvas and start collecting regrade requests
* Students can submit regrade requests through the Project Grading Issue Form.
    * The regrade requests are only for TA's mistakes in manual grading.
    * Please do not submit any regrade requests until grades are posted to Canvas.
* One week after the grade release on Canvas: we will stop collecting regrade requests.
* One week after closing regrade requests for projects: TAs will contact you for regrade request results.

### Deduction Decisions

* We will only grade individual portion.
* We will deduct points for hardcoding and not following directions.
* Other bugs may receive written feedback with no deduction.
* We will try to include at least one inline comment about how to improve the code for each student’s submission, even for the ones with a perfect score.

## Rubric for MP6

### Deduction Reasons

**Individual - Part 1 (10 points)**
* Hardcoding, **-10**
    * e.g., displaying empty plot 
* Setting up train & test sets (4 points)
    * If didn't add all land use feature, **-2**
    * If didn't split train & test sets, **-1**
* Building model (2 points)
    * If didn’t use all land use columns as feature columns or didn't use `POP100` as label column, **-1**
    * If didn't use train set to fit the model, **-1**
* Barplot (2 points)
    * If wrong shape, **-2**
    * If no x, y labels or x ticks for each feature, **-1**
* Interpretation (2 points)
    * If incorrect interpretation, **-2**

**Individual - Part 2 (15 points)**
* Hardcoding, **-15**
    * e.g., displaying any number larger than 0.35
* Building models (4 points)
    * If didn't use `POP100` as label column, **-1**
    * If didn't use train set to fit the model, **-1**
    * If the two models are not different, **-2**
* Evaluating models (5 points)
    * If use test set to compute cross validation scores, **-1**
    * For each model: 
        * If mean of cross validation scores is missing, **-1**
        * If variance of cross validation scores is missing, **-1**
* Recommendation (3 points)
    * If wrong recommendation, **-3**
    * If the reasoning is insufficient, **-1**
* Evaluating recommended model (3 points)
    * If didn't use test set to compute score, **-1**