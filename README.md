## CSES Problems

300 computer science problems to solve! This repository houses solutions to the problems written in Rust according to the following table:

|Category|Solved|Unsolved|Total|
|---|---|---|---|
|Advanced Techniques|0|24|24|
|Dynamic Programming|0|19|19|
|Geometry|0|7|7|
|Graph Algorithms|0|36|36|
|Introductory Problems|0|19|19|
|Mathematics|0|31|31|
|Range Queries|0|19|19|
|Sorting and Searching|0|35|35|
|String Algorithms|0|17|17|
|Tree Algorithms|0|16|16|
|Additional Problems|0|77|77|

This repository also contains a scraper that scrapes the official problems, turns them into .md files and saves them locally. This way the problems can be attempted without an internet connection!


### Running the scraper

First install the packages

```
pip install -r requirements.txt
```

then run the scraper

```
python scraper.py
```

This will scrape all problem categories and all individual problems into a folder called `categories`. From there you can access them how you see fit.