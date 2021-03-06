# TextML: Text Classification and Clustering with Sklearn and visualization with Dash

This repo offers an all-in-one tool for processing text using the most popular ML algorithms.
The app runs as a microservice with an embedded server, which performs the ML functionality and offers a UI for using the tool.
We also include a jupyter notebook for demonstrating the algorithms used (K-Means and Naive-Bayes).

:rocket: **Live working example here**: https://ml-text-app-tydzzcuoha-oa.a.run.app/

## :point_right: Included functionality

### Upload data
Upload data in .json or .csv format. Depending on the file size, the algorithms may take longer to run, so we advise to start
with smaller datasets.

*Note:* The column names must follow this naming convention: 

* **input**: The raw text data
* **label**(optional): The labels of the data, needed for classification.

![screenshot](screenshots/capture1.png)


### Train and evaluate models

* Choose number of clusters for Kmeans by examining sihlouette plots
* Explore generated clusters and see samples for each category
* Train Naive-Bayes classifier
* Explore performance metrics
* Save models for latter use

![screenshot](screenshots/capture2.png)

### Use the models

Test your saved classifier/classification models with new samples.

![screenshot](screenshots/capture3.png)

## :bar_chart: Dataset

The example data are Amazon user reviews, taken from 5 categories:
* Movies
* Music Instruments
* Books
* Software
* Clothing

The datasets are located in the /demo/datasets directory. Each file corresponds to a category with 5000 samples.
The full data can be downloaded from http://jmcauley.ucsd.edu/data/amazon/

Also there are mixed datasets with sizes 200 and 500 per class. These are loaded into the microservice on startup, so you can experiment
without having to provide your own data.


## :running: How to run

The easiest way to run is with Docker Compose. Simply type

`docker-compose up`

and visit http://localhost:8080

If you don't have docker installed then run the main.py file included in the root directory. This spins up a server running on localhost.
You also need to have a Mongo db running on localhost.

`pip3 install -e .`

`python3 main.py`


## :blue_book: Jupyter report and demo

Under /demo you may find the jupyter notebook which evaluates the performance of the algorithms in the given datasets.
