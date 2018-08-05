# Logs Analysis

## About

This practice project is an internal reporting tool for a fictional newspaper site to be used for analyzing what kind of articles the readers like.

The database contains a list of articles as well as the server log in three tables:
 - Articles
 - Authors
 - Log
 
The report provides an answer to the following **questions**:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


### Requirements

- **Linux** with [**Python 3**](https://www.python.org/) and [**PostgreSQL**](https://www.postgresql.org/) installed
(or a corresponding VM, e.g.: [Vagrant](https://www.vagrantup.com/) & [VirtualBox](https://www.virtualbox.org/))
- [**News data**](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)


## To Run
Clone this repo and `cd` into its directory.
Make sure to **download the** [**news data**](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

To create the news database with necessary data: 
`psql -d news -f newsdata.sql`.


Run `python log_analysis.py` from the shell to view the report.