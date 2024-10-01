# Machine Project 5: EDGAR Web Logs

## Corrections/Clarifications

* None yet

## Overview

In the US, public companies need to regularly file
various statements and reports to the SEC's (Securities and Exchange
Commission) EDGAR database.  EDGAR data is publicly available online;
furthermore, web requests to EDGAR from around the world are logged
and published.  EDGAR logs are huge.  Logs for *just one day* might be
about 250 MB compressed as a .zip (or 2 GB uncompressed!).

We'll develop tools to extract information from the filings stored in EDGAR (this will be done in a Python module, `edgar_utils.py`) and we'll use those tools to analyze user behavior in `mp5.ipynb`.

### Learning Objectives

During this machine project, students will:
- Work with large datasets from a zipfile using the Python `zipfile` module.
- Create a custom class for analyzing filing data using regular expressions
and other tools.
- Plot geographic data using the `geopandas` module.

## Setup

Before you begin, follow the "starting a machine project" instructions in the [git-workflows](../../git-workflows/README.md/#starting-a-machine-project) document to make sure that you are on the right branch and have the right files.

For this machine project, we will need some additional modules. You can install them by running the
following lines in your VM's command line:

```
pip3 install --upgrade pip
sudo apt install -y graphviz
sudo apt install -y python3-rtree
pip3 install geopandas shapely descartes geopy netaddr==0.10.0 graphviz
```

## Testing

Be sure to run `python3 tester.py` regularly to estimate your grade. As in machine project 2, the tester will both check the results of the analysis in your notebook, and use `module_tester.py` to check your `edgar_utils.py` module.

## Submission

**Required Files**
* `mp5.ipynb`: A notebook that contains the answers to the questions found below.
* `edgar_utils.py`: A Python module (.py file) that will have a `Filing` class as well
as various functions for parsing filing information.

To submit the machine project, make sure that you have followed the instructions for "submitting a project"
in the [git-workflows](../../git-workflows/README.md/#submitting-a-machine-project) document for the required file(s) above.

When following the submission instructions from above, the final output should look similar to this in GitLab:

<img src="./successful-submission.PNG">

If you do not know how to get to this screen, review the link above. If you are having issues, please come to office hours.

## Data format

Take a look at the list of daily zips and CSV documentation on the EDGAR site:

- https://www.sec.gov/dera/data/edgar-log-file-data-set.html
- https://www.sec.gov/files/EDGAR_variables_FINAL.pdf

We have provided a `server_log.zip` file, which is a subset of the
records from `log20170101.zip`. Since you'll need to work with a lot of zipped files for this machine project, you'll want to know some command line techniques
to troubleshoot.

You could use `sudo apt install unzip` to install unzip, and then view names of files in a zip file:

```
unzip -l server_log.zip
```

View the start of a file inside of a zip file (change "head" to "tail"
to see the end):

```
unzip -p server_log.zip rows.csv | head -n 5
```

The expected result is:

```
ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser
104.197.32.ihd,2017-01-01,00:00:00,0.0,1111711.0,0001193125-12-324016,-index.htm,200.0,7627.0,1.0,0.0,0.0,10.0,0.0,
208.77.214.jeh,2017-01-01,00:00:00,0.0,789019.0,0001193125-06-031505,.txt,200.0,46327.0,0.0,0.0,0.0,10.0,0.0,
54.197.228.dbe,2017-01-01,00:00:00,0.0,800166.0,0001279569-16-003038,-index.htm,200.0,16414.0,1.0,0.0,0.0,10.0,0.0,
108.39.205.jga,2017-01-01,00:00:01,0.0,354950.0,0000950123-09-011236,-index.htm,200.0,8718.0,1.0,0.0,0.0,10.0,0.0,
```

Looking at the `cik`, `accession`, and `extention` fields tells you what web resource a user was requesting (in particular, each company has it's own `cik`):

```
ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser,region
54.212.94.jcd,2017-01-01,03:31:36,0.0,1461219.0,0001209191-21-001287,-index.htm,301.0,243.0,1.0,0.0,1.0,10.0,0.0,,United States of America
...
```

**Note**: For this row, we can construct the following URL from `1461219.0`, `0001209191-21-001287`, and `-index.htm`: https://www.sec.gov/Archives/edgar/data/1461219/0001209191-21-001287-index.htm

Looking at this page and its source (as well as the source of the pages where your parser does not behave as expected) is highly recommended and will be very important later in the machine project.

We have already downloaded the docs for a subset of the requests in
`server_log.zip` for you and placed them in `docs.zip`. Note, however, that the file structure is slightly different than the URL above. The path in the zip to that file would be "1461219/0001209191-21-001287/-index.htm".

Note that by default reading inside a zip gives you bytes.  For your regex work, convert to a string using UTF-8 (like we have done for `check_output`).

# Group Part (77%)

For this portion of the machine project, you may collaborate with your group members in any way (including looking at group members' code). You may also seek help from CS 320 course staff (peer mentors, TAs, and the instructor). You **may not** seek or receive help from other CS 320 students (outside of your group) or anybody else outside of the course.

## Part 1: `server_log.zip` analysis

Answer these questions in `mp5.ipynb`.

### Q1: What's the total size in bytes of the files requested?

Look at the `size` column of the CSV in `server_log.zip`.  We want to
include duplicates here; this gives us an estimate of the amount of
network traffic handled by EDGAR (since this data is only a sample,
the true value will be even larger). Answer with an integer.

### Q2: How many filings have been accessed by the top 10 IPs?

Answer with a dictionary, with the (anonymized) IP as key and the number of requests seen in the logs as the values. Each row in the logs corresponds to one request. Note that the anonymized IP addresses are consistent between requests.

**Hint:** for this question and most of the others expecting dictionary output, it might be easiest to use Pandas operations to process the data into a `Series` and to use the `to_dict()` method. Consider using tools like `groupby`, `apply`, and aggregation methods like `size()`. In Q30-32 from [MP1](../mp1/README.md), there is an example of `apply`.

### Q3: What fraction of the requests had errors?

Any request with a status code greater than or equal to 400 has an error. Answer with a floating point number.

### Q4: What is the second most frequently accessed file?

Answer with a string formatted like so: "cik/accession/extention" (these are the names of columns in "rows.csv").

## Part 2: Creating `edgar_utils.py` module

This part is to be started during [Lab 9](../../labs/Lab9/README.md). 

Finish the `edgar_utils.py` module now if you didn't have enough time
during the scheduled lab.

## Part 3: Using `edgar_utils.py` module

### Q5: Which region uses EDGAR most heavily?

Use your `lookup_region` function and answer with a string.

### Q6: What fraction of IPs in each region are high-volume users?

Consider IPs which accessed more than 300 EDGAR resoures to be
high-volume. This might indicate machines running automated scraping
and analysis tasks.

Note that given the sampling done in the data, the true EDGAR usage of
these machines is likely to be even heavier.

Answer with a dictionary, where the keys are the regions and the
values are the fraction (in floating point form) of IPs from that
region classified as high-volume.

**Example:**

Say "United States of America" has four IPs:
* 1.1.1.1 appears 1200 times in the logs
* 2.2.2.2 appears 900 times in the logs
* 3.3.3.3 appears 5 times in the logs
* 4.4.4.4 appears 234 times in the logs

This means that 1/2 of the IPs in the US are high volume, so there should be an entry like this:

```
{
    "United States of America": 0.5,
    ...
}
```

**Note:** Some of the filings are listed as having a region of '-'. Please include this in your final
answer.

### Requirement: `filings` dictionary

Read every file ending with .htm or .html in `docs.zip`, and create a `Filing`
object based on that file. Then, save that `Filing` object to a dictionary as follows:
- **Key:** The filepath for this filing object (ex. `850693/0000850693-07-000159/-index.htm`)
- **Value:** The `Filing` object created from this filepath.

Creating this dictionary once now will save us from needing to loop over all values
in future questions.

<!-- TODO: Update question/answer -->
### Q7: What dates appear in the `886982/0000769993-16-001958/-index.htm` file of `docs.zip`?

Read the HTML from this file and use it to create a `Filing` object,
from which you can access the `.dates` attribute.

### Q8: What is the distribution of states for the filings in `docs.zip`?

Answer with a dict, like the following:

```
{'CA': 92,
 'NY': 83,
 'TX': 67,
 'None': 56,
 'MA': 30,
 'IL': 25,
 'PA': 25,
 'CO': 25,
 ...
}
```

The showing order of each key-value pair doesn't really matter. Please include `None` in the
dictionary.

**Hint:** We created the `filings` dictionary above, which means we don't have to
iterate through `docs.zip` here again!

### Q9: What is the distribution for the ten most common addresses for the filings in `docs.zip`?

Answer in the same format as the previous question.

Expected output:
```
{'2000 AVENUE OF THE STARS, 12TH FLOOR\nLOS ANGELES CA 90067': 134,
 '2000 AVENUE OF THE STARS, 12TH FLOOR\nLOS ANGELES CA 90067\n3102014100': 113,
 '3 LANDMARK SQUARE\nSUITE 500\nSTAMFORD CT 06901\n2033564400': 60,
 'C/O KKR ASSET MANAGEMENT LLC\n555 CALIFORNIA STREET, 50TH FLOOR\nSAN FRANCISCO CA 94104': 36,
 'C/O ARES MANAGEMENT LLC\n2000 AVENUE OF THE STARS, 12TH FLOOR\nLOS ANGELES CA 90067': 35,
 '4740 AGAR DRIVE\nRICHMOND A1 V7B 1A3': 25,
 'CENTRALIS S.A., 8-10 AVENUE DE LA GARE\nLUXEMBOURG N4 L-1610': 25,
 'CENTRALIS S.A., 8-10 AVENUE DE LA GARE\nLUXEMBOURG N4 L-1610\n352-26-186-1': 25,
 '3 LANDMARK SQUARE\nSUITE 500\nSTAMFORD CT 06901': 24,
 '801 CHERRY STREET\nSUITE 2100\nFORT WORTH TX 76102': 22}
```

# Individual Part (23%)

For this portion of the machine project, you are only allowed to seek help from CS 320 course staff (peer mentors, TAs, and the instructor). You **may not** receive help from anyone else.

## Part 4: Combining logs with documents

### Q10: What is the distribution of requests across industries?

For each request in the logs that has a corresponding filing in
`docs.zip`, lookup the SIC (ignore rows in the logs which refer to
pages not in `docs.zip`).

Answer with a dictionary, where the keys are the SIC and the values
are the number of times the resources of that industry were accessed.

If you're curious, consider looking up the industry names for the top
couple categories:
https://www.sec.gov/corpfin/division-of-corporation-finance-standard-industrial-classification-sic-code-list

Expected output:

```
{2834: 984,
 1389: 656,
 1311: 550,
 2836: 429,
 6022: 379,
 1000: 273,
 ...
 }
 ```

### Q11: How many requests were made in each hour?

Use `pd.to_datetime` (the `hour` attributes of the converted
timestamps may be useful) or string manipulation to process the `time`
column. Answer with a dictionary, where the keys are integers from 0
to 23 representing the hour of the day, and the values are the number
of requests made in that hour.

### Q12: What is the geographic overlap in interest between Australia, France, Indonesia, and Viet Nam?

Answer with a Digraph like the following:

<img src="digraph.png" width=400>

In addition to a node for each of these three countries, there should
be a node for each state having a filing accessed by somebody in one
of these countries.

An edge from a country to a state means somebody in that country
looked at least one filing for a company in that state.

**Important:** Make sure not to hardcode these values. It might be helpful to
define a list like `countries = ["Australia", "France", "Indonesia", "Viet Nam"]` and then loop over the filings for these countries only.

### Q13: Geographic plotting of postal code

The `locations.geojson` contains the positions of some of the
addresses in the dataset.  Plot this over the background map in
"shapes/cb_2018_us_state_20m.shp"

Additional requirements:

* Crop to the following lat/lon bounds:

```python
west = -90
east = -65
north = 50
south = 25
```

* Use a Mercator projection, "epsg:2022"
* The color of each point should indicate the postal code. For example, the postal code of `245 SUMMER STREET\nBOSTON MA 02210` is `2210`. If it's in the form like `53705-1234`, only take `53705`. If it's neither 5 digits number nor 9 digits number, don't use the point.
* Only show the street with a postal code from 10000 to 60000
* Use the "viridis" colormap, with a colorbar
* The color of background is "lightgray"

The result should look similar to this:

![](geo.png)

**Hint:** If you are getting issues with getting the slanted lines or issues with your graphs 
disappearing, make sure that you are applying the `.to_crs(...)` function to both the points
and the background before plotting.

# Conclusion

The EDGAR logs are supposedly anonymized (with the last three docs
left), but we can still tell where the users live and what they're
looking at.

 By connecting the filing information with the logs, we can learn a lot about the behavior of the investment firms which use the database - for example, we might learn which companies (or industries) a hedge fund might be considering investing in, and the extent to which it relies on automated vs manual research in its trading.

Others have used this same data to make good guesses
about what docs various hedge funds and others are looking at, then
correlate that with success.  For those interested in the nitty-gritty
details of what could be done with this data, take a look at this
early-stage work: [Hedge Funds and Public Information
Acquisition](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3127825).
