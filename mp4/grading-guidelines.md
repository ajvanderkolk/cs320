# Machine Project 4 - Grading Guidelines

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

## Rubric for MP4

### Deduction Reasons

**Dashboard**
* Missing x, y labels, **-1** (deduct only once)
* Query string is not used, **-2**
* Query string is not descriptive enough, **-1**
    * e.g., still use “from=A” for changing the number of bins of the plot
* Changes to the plot with the query string is not meaningful enough, **-3**
    * e.g., simply changing the color of the entire plot from blue to red
    * Meaningful changes can be changing the x/y column, sorting the bar/hist plot, changing the number of bins, color-coding the scatterplot based on a third categorical column, etc. 
* The two plots with different routes are not distinct enough, **-4**
    * By distinct enough, it means that no significant portion of code is reused to generated the two plots
        * e.g., use scatter plots for both routes and only change the x, y columns
    * Distinct plots can be 
        * Two different types of plots (e.g., one scatter plot and one bar plot) or 
        * The same type of plot but with significant data transformations (e.g., aggregation, filtering, etc.)
* For each plot, hardcoding, **-6**
    * e.g., return random/empty plot