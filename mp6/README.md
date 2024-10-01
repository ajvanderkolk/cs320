# Machine Project 6: Intro to Regression Models

## Corrections/Clarifications

* None yet

## Overview

We will be making predictions about census data for Wisconsin using
regression models. You'll need to extract data from four files to
construct DataFrames suitable for training during this machine project:

* `counties.geojson` - population and boundaries of each county in Wisconsin
* `tracts.shp` - boundaries of each census tract (counties are subdivided into tracts)
* `counties_tracts.db` - details about housing units per tract
* `land.zip` - details about land use (farm, forest, developed, etc.)

### Learning Objectives

During this machine project, students will:
- Extract, transform, and load data from multiple data sources into one DataFrame for training
machine learning models.
- Analyze machine learning model performance using several different metrics and factoring in feature
impact on the model score.
- Plot geographical data using the `geopandas` module.

## Setup

Before you begin, follow the "starting a machine project" instructions in the [git-workflows](../../git-workflows/README.md/#starting-a-machine-project) document to make sure that you are on the right branch and have the right files.

## Testing

Be sure to run `python3 tester.py mp6.ipynb` regularly to estimate your grade.

## Submission

**Required Files**
* `mp6.ipynb`: A notebook that contains the answers to the questions found below.

To submit the machine project, make sure that you have followed the instructions for "submitting a machine project"
in the [git-workflows](../../git-workflows/README.md/#submitting-a-machine-project) document for the required file(s) above.

When following the submission instructions from above, the final output should look similar to this in GitLab:

<img src="./successful-submission.PNG">

If you do not know how to get to this screen, review the link above. If you are having issues, please come to office hours.

# Group Part (73%)

For this portion of the machine project, you may collaborate with your group members in any way (including looking at group members' code). You may also seek help from CS 320 course staff (peer mentors, TAs, and the instructor). You **may not** seek or receive help from other CS 320 students (outside of your group) or anybody else outside of the course.

## Part 1: Predicting Population using Area

### Q1: How many counties are in Wisconsin?

Read `counties.geojson` into a GeoDataFrame and use it to calculate the number of counties in Wisconsin.

### Q2: What is the population of each county in WI?

Create a geopandas plot that has a legend using the population from
the `POP100` column.

<img src="fig/q2.png" width="500">

The US Census Bureau does some surveys that attempt to sample the
population and others (like the decennial one) that attempt to count
everybody.  "POP100" means this is there attempt to count 100% of the
population (no sampling).  Similarly, "HU100" is a 100% count of
housing units.

### Requirement: Feature 1 - `AREALAND`

Let's add an `AREALAND` column to your GeoDataFrame of counties so
that we can try to predict population based on area.

You can get the area from the `counties_tracts.db` database.  Open it using [sqlite3](https://docs.python.org/3/library/sqlite3.html) then use [read_sql](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html) on the DB connection to execute a query.

A great first query for an unfamiliar DB is `pd.read_sql("""SELECT * FROM sqlite_master""", conn)`.  That will show you all the tables the DB has. Try running `pd.read_sql("""SELECT * FROM ????""", conn)` for each table name to see what all the tables look like.

Use data from the database to add an `AREALAND` column to your
GeoDataFrame.  The order of rows in your GeoDataFrame should not
change as part of this operation.

After you've added `AREALAND` to your GeoDataFrame, use
`train_test_split` from `sklearn` to split the rows into `train` and
`test` datasets.

* By default, `train_test_split` randomly shuffles the data differently each time it runs.  Pass `random_state=320` as a parameter so that it shuffles the same way as it did for us (so that you get the answers the tester expects).
* Pass `test_size=0.25` to make the test set be one quarter of the original data and the other three quarters remaining in the training set.

### Q3: What are the counties in the test dataset?

Answer with a list, in the same order as the names appear in the original DataFrame. 

### Q4: How much variance in the `POP100` can a `LinearRegression` model explain based only on `AREALAND`?

`fit` the model to your `train` dataset and `score` it on your `test` dataset. 

**Note:** Calling `LinearRegression.score(...)` will, by default return the $r^2$ score: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression.score.

### Q5: What is the predicted population of a county with 300 square miles of area, according to the model?

Consult the [Census documentation](https://tigerweb.geo.census.gov/tigerwebmain/TIGERweb_attribute_glossary.html) to learn what units the data is in, and do any conversions necessary to answer the question.  Assume there are exactly 2.59 square kilometers per square mile for the purposes of your calculation.

## Part 2: Predicting Population using Housing Units

You'll need to wait to do the lab before continuing: [Lab 11](../../labs/Lab11/README.md)

### Requirement: Feature 2 - `HU100` (housing units)

Look at the `tracts` table inside `counties_tracts.db` and find the
`HU100` column. Add a `HU100` column to your GeoDataFrame of counties,
similar to how you added `AREALAND`.

**The query to get housing units per county is more complicated than the
one for AREALAND**.  County names are in the `counties` table and
`HU100` values are in the `tracts` table.  Fortunately, both tables
have a `COUNTY` column you can use to combine. Make sure to get the
total number of housing units for each county from the `tracts` table
by summing the housing units in each tract of the county.

**Split your updated GeoDataFrame into a train and test set, the same
way you did previously.**

**Hints**
1. If I have the same column  in two separate tables, I can run the
following SQL to join based on that column:
```
SELECT table1.column1, column2, column3
FROM table1
INNER JOIN table2
ON table1.column1 == table2.column1
```
2. The order of the counties may not be the same from your original DataFrame
and the one you get from this step. Thus, when you merge them together, consider
using the `pd.merge(...)` function with the `on=????` parameter or the `left_on=????`
and `right_on=????` parameters: https://pandas.pydata.org/docs/reference/api/pandas.merge.html.

### Q6: What are the counties in the test dataset?

Answer with a `list`, in the same order as the names appear in the DataFrame.
Note: Refer [Join](https://www.geeksforgeeks.org/sql-join-set-1-inner-left-right-and-full-joins/) to get a brief understanding on how different joins work

### Q7: What are the HU100 values for the counties in the test dataset?

Answer with a `dict`.

### Q8: How much variance in the `POP100` can a `LinearRegression` model explain based only on `HU100`?

Answer with the average of 5 scores produced by [`cross_val_score` on the training data](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html) (i.e., we are doing 5-fold cross validation).

### Q9: What is the standard deviation of the cross validation scores from Q8?

Refrain from using statistics.stdev to calculate standard deviation. Variance is the average squared deviations from the mean, while standard deviation is the square root of this number.

### Q10: What is the formula relating POP100 and HU100?

Fit your model to the training dataset to find the answer. Round the coefficient and intercept to 2 decimal places. Format the answer according to the following formula, and output it as a string:

```
POP100 = ????*HU100 + ????
```

### Q11: What is the r-squared score of your fitted model (from Q10)?

Use the fitted model from Q10 and [metrics.r2_score()](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html) from sklearn to find the accuracy of your model. Note that you want to use test data for this question.

### Q12: What is the relationship between HU100 and POP100, visually?

Answer with a scatter plot showing the actual values and the predicted fit line based on the model. You should use both train and test data for the plot (i.e., the entire data).

Use a `.text` call to annotate Waukesha County, and a legend to label the actual and predicted parts as in the following:

<img src="fig/q12.png" width="500">

## Part 3: Land Use Features

### Q13: How many numbers in matrix `A` are between 1 and 4 (inclusive)?

You can paste the following to define `A`:

```python
A = np.array([
    [0,0,5,8,4],
    [1,2,4,0,3],
    [2,4,0,9,2],
    [3,5,2,1,1],
    [0,5,0,1,0]
])
```

### Q14: How does Dane County look?

NOTE: in lab, you had to use TIGERweb to get the geodata.  You
**shouldn't** do that here because we already did that saved the results
to `counties.geojson`, which you should use.  Otherwise, this is very
similar to the lab exercise.

You can show the image like this:

```python
fig, ax = plt.subplots(figsize=(6,6))
ax.imshow(????, vmin=0, vmax=255)
```

You can get the matrix for Dane County using `rasterio` and using the geometry in the DataFrame from `counties.geojson`. You can open a file inside zip by running the command `rasterio.open("zip://./land.zip!/wi.tif")`.

You can also define a custom color map ([corresponding to the legend](https://www.mrlc.gov/data/legends/national-land-cover-database-2019-nlcd2019-legend) and pass `cmap=custom_cmap` to `imshow` to use it.

You can create a custom color map using `ListedColormap`, which lets you specify red, green and blue (RGB) mixes for different values.  Here's an example for the land use data:

```python
from matplotlib.colors import ListedColormap

c = np.zeros((256,3))
c[0] = [0.00000000000, 0.00000000000, 0.00000000000]
c[11] = [0.27843137255, 0.41960784314, 0.62745098039]
c[12] = [0.81960784314, 0.86666666667, 0.97647058824]
c[21] = [0.86666666667, 0.78823529412, 0.78823529412]
c[22] = [0.84705882353, 0.57647058824, 0.50980392157]
c[23] = [0.92941176471, 0.00000000000, 0.00000000000]
c[24] = [0.66666666667, 0.00000000000, 0.00000000000]
c[31] = [0.69803921569, 0.67843137255, 0.63921568628]
c[41] = [0.40784313726, 0.66666666667, 0.38823529412]
c[42] = [0.10980392157, 0.38823529412, 0.18823529412]
c[43] = [0.70980392157, 0.78823529412, 0.55686274510]
c[51] = [0.64705882353, 0.54901960784, 0.18823529412]
c[52] = [0.80000000000, 0.72941176471, 0.48627450980]
c[71] = [0.88627450980, 0.88627450980, 0.75686274510]
c[72] = [0.78823529412, 0.78823529412, 0.46666666667]
c[73] = [0.60000000000, 0.75686274510, 0.27843137255]
c[74] = [0.46666666667, 0.67843137255, 0.57647058824]
c[81] = [0.85882352941, 0.84705882353, 0.23921568628]
c[82] = [0.66666666667, 0.43921568628, 0.15686274510]
c[90] = [0.72941176471, 0.84705882353, 0.91764705882]
c[95] = [0.43921568628, 0.63921568628, 0.72941176471]
custom_cmap = ListedColormap(c)
```

<img src="fig/q14.png" width="500">

### Q15: What portion of Dane County is "Crops"?

Be careful!  Not everything in the matrix is Dane County -- be
sure not to count the cells with value 0.

You can lookup the numeric code for "Crops" and other types here: https://www.mrlc.gov/data/legends/national-land-cover-database-2019-nlcd2019-legend

Or, for your convenience, we typed the info from that page into a Python dictionary:

```python
land_use = {"open_water": 11,
            "ice_snow": 12,
            "developed_open": 21,
            "developed_low": 22,
            "developed_med": 23,
            "developed_high": 24,
            "barren": 31,
            "deciduous": 41,
            "evergreen": 42,
            "mixed_forest": 43,
            "dwarf_scrub": 51,
            "shrub_scrub": 52,
            "grassland": 71,
            "sedge": 72,
            "lichens": 73,
            "moss": 74,
            "pasture": 81,
            "crops": 82,
            "woody_wetlands": 90,
            "herbacious_wetlands": 95}
```

### Q16: What is the Relationship Between POP100 and ________________?

Replace the blank with a cell count for a land type of your choosing.
Show a scatter plot where each point corresponds to a county.

For example, the following shows the relation between open water and
population (you may **NOT** reuse open water -- choose a different type for
your plot):

<img src="fig/q16.png" width="500">

# Individual Part (27%)

For this portion of the machine project, you are only allowed to seek help from CS 320 course staff (peer mentors, TAs, and the instructor). You **may not** receive help from anyone else.

For this part, you'll try to predict population on a **per-census
tract** basis (in contrast to our preceding per-county analysis),
using features calculated from the land use data.  

## Part 1: Feature Analysis
1. Start with a GeoDataFrame dataset loaded from `tracts.shp`.
2. Add feature columns to that dataset for every key in land_use(found under q14), with the column value being the number of units present of that land type, based on raster data from `lands.zip`.
**Important:** Computation takes considerable amount of time with raster data so try to minimize masking operations!
3. Split your GeoDataFrame into train/test using `random_state=320` and `test_size=0.20`.
4. Construct a regression model to predict POP100. Use all of the new columns you created in step 2 as the features for training.

### Q17: What features does your model rely on most?

Answer with a bar plot showing feature and coefficient of feature in our trained model.

Write a comment discussing what the graph is showing you and how you might use that 
information in building your own model

In terms of tester scores, this question is weighted to be worth 2 regular questions.

## Part 2: Model Creation and Analysis
1. Construct at least 2 regression models predicting POP100. They should differ in terms of (a) what columns they use and/or (b) whether or not they're preceded by transformers in an sklearn Pipeline
2. Perform cross validation on both of your models over your training dataset

### Q18: What is the mean and variance of the cross validation scores from both of your models?

Answer with a dictionary like this:
```
{
'model1-avg': 0.44286680823801083,
 'model1-std': 0.034903979417578036,
 'model2-avg': 0.4746679087375649,
 'model2-std': 0.033400327309278784
}
```

Write a comment recommending which model you recommend for this prediction task. Factors you **must** consider are (a) mean of cross validation scores is high, (b) variance of cross validation scores is low. Additional factors you might consider are (c) model is simple, and (d) anything else you think is important.

**Note:** Your values are likely to be different than those seen above, which is okay.
We are just checking if you return a dictionary for this question.

### Q19: How does your recommended model score against the test dataset?

Fit your recommended model to the train dataset and then score it using the test dataset.
Your model needs to achieve explained variance higher than 0.35 in order to receive full credit.

This question is weighted to be worth 3 regular questions. 