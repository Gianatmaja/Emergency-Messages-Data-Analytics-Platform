# Emergency Messages Data & Analytics Platform

### Project Overview
Every now and then, disasters and emergencies could happen, and while people may do their best to prepare for it, something unexpected can always arise, and  during this time, it is crucial to receive the necessary help quickly. The rise of internet and social media has made communication easy, but manual processing of emergencies and requests for help is still time-consuming, as understanding the situation and the needs of the person in distress may not be so straightforward. This project aims to solve this problem by building a PoC (Proof-of-Concept) for an end-to-end pipeline that stores, analyses, and classifies emergency messages, using techniques from data science, machine learning, and data engineering.

The structure of this repository can be viewed below.

    .
    ├── notebooks/                                         # Contains Jupyter notebooks for exploration & experimentation
    │  ├── Data Augmentation.ipynb                         # Adding additional columns to better suit project use case
    │  ├── Data Cleaning.ipynb                             # Removing redundant data to better suit project use case
    │  ├── Exploratory Data Analysis with Spark.ipynb      # Exploring the data with PySpark
    │  ├── ML Model Building.ipynb                         # Random forest model training for message categories prediction
    │  ├── Prediction Illustration.ipynb                   # Illustrate prediction process
    ├── dags/
    │  ├── etl.py                                          # Main Python script for Airflow DAG
    │  ├── Helpers.py                                      # Python sript containing helper functions
    ├── data/                                              # Contains sample data
    │  ├── Staging.csv                                     
    │  ├── Processing.csv
    │  ├── Refined.csv   
    │  ├── Msg_Fact.csv                                     
    │  ├── Date_Dim.csv
    │  ├── Lang_Dim.csv 
    │  ├── Cat_Dim.csv 
    ├── images/                                            # Contains images used in README
    └── README.md

The data that is used in this project is the multilingual disaster response messages data. This dataset, along with its description, can be accessed [here](https://www.kaggle.com/datasets/landlord/multilingual-disaster-response-messages).

### Business Process
The main process considered in this project is after an emergency message has been submitted. For future development, we propose a mobile app as the main entry point for these messages. Through the app, the use will be prompted to describe their emergencies and optinally select the request categories of their emergencies (meds, food, water, etc.), before submitting the request. The ID, date, and language, will be automatically added. If a user labels/ categorises their message, then there will be a 1 or 0 value, indicating yes or no, in each of the target variables (meds, food, water, etc.).

To better follow the process of submitting an emergency message, a mockup of the emergency message mobile app has been created and can be viewed and interacted with [here](https://rp.mockplus.com/run/mZjA1toNnZ/lcyvCAMMEB?cps=hide&rps=hide&nav=1&ha=0&la=0&fc=0&dt=iphoneX&out=0&rt=1).

![Mockup](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Screenshot_2022-11-17_at_9.35.33_PM-removebg.png)

Once submitted. the message will be stored, processed and analysed using a pre-trained machine learning model, which will predict the request categories of the emergency message. Based on those predictions, the level of the emergency (low, medium, high) will also be determined. As more messages are submitted, the size of the data will grow and business users can then analyse and view insights through queries, reports, and dashboards.

### Solution Architecture
The solution architecture for this project can be viewed below. The main tools that are used include Python, Spark, Airflow, and Amazon Web Services.

![Architecture](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Picture5.png)

Aligning with the business process, when an emergency message is submitted, it will first be stored in the staging layer in S3. This raw data will then be checked for data quality, then passed into the processing layer. The pre-trained machine learning model will take the data here as input, and the predictions, along with other analyses, will be stored alongside the input data in one table, in the refined layer. From there, data transformations will be applied to transform the data into a star schema model, which will then be stored in a Redshift data warehouse. To get a better sense of how the data looks in each of these layers, several data samples have been uploaded in .csv format in the `data/` folder.

To automate the data pipelines, Apache Airflow can be utilised. Below is a sample DAG which has been created for this project. The codes can be viewed in the `etl.py` and `Helpers.py` file, located inside the `dags/` folder, which is normally under the `airflow` directory in an Airflow project structure.

![dag](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/dag.png)

Data in the data warehouse can then be queried into the consumption zone for further business analysis, or passed into BI tools, such as Power BI, to be viewed in a dashboard format.

From time to time, offline copies of the data in the staging layer will also be passed into the exploratory zone, where data science and machine learning activities are conducted. This is where new machine learning models are experimented and trained in. Tools that can be used here include Python, Jupyter notebooks, Scikit-learn, Spark, as well as GitHub as the code repository. We demonstrate some of these use cases in the `Exploratory Data Analysis with Spark.ipynb` and `ML Model Building.ipynb`, which can be accessed in the `notebooks/` folder. 

In the `Exploratory Data Analysis with Spark.ipynb` notebook, we used PySpark, Spark SQL, as well as Spark's UDFs to perform analyses on our data, whereas in the `ML Model Building.ipynb` notebook, we trained a multi-output random forest classifier to predict message categories, and in the end developed a pipeline to preprocess and predict future emergency messages. The pipeline is then exported using joblib for future usage.

### Data Consumption
As mentioned in the previous section, the data in the data warehouse will follow a star schema. In our case, there will be one fact table and three dimension tables. These three dimension tables will contain information about the dates, languages, and emergency category levels, respectively. The star schema data model for this project can be viewed below.

![Schema](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Picture6.png)

An example use case for the consumption zone would be to query the data in the data warehouse and pass it to be viewed in a Power BI dashboard. An example query would be:
                      
    SELECT Msg_Fact.*, Date_Dim.date, Lang_Dim.language, Cat_Dim.category 
    FROM Msg_Fact LEFT JOIN Date_Dim 
    ON Msg_Fact.date_ID = Date_Dim.date_ID 
    LEFT JOIN Lang_Dim 
    ON Msg_Fact.language_ID = Lang_Dim.language_ID 
    LEFT JOIN Cat_Dim 
    ON Msg_Fact.category_ID = Cat_Dim.category_ID;
    
Using data from the above query, a sample Power BI dashboard has also been created. The dashboard can be viewed below.

![Dashboard](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Dashboard.png)

From the dashboard, business users can oberve the trends in the number of messages submitted throughout the years. They can also observe the proportion of related and labeled messages, from a variety of languages. Furthermore, the number of low, medium, and high emergency messages are also shown. Finally, business users can also identify the leading cause of emergencies using the treemap located in the bottom right area of the dashboard.

### Future Development
Some recommendations which could be taken into consideration during future development include:
- Improving the Hardware: The hardware specifications such as the number of clusters, or the data refresh rate, could be optimised. This will help to provide services to a larger amount of users and offer real-time predictions.
- Machine Learning Model Retraining Pipeline: MLOps could be included as a part of the architecture, to support model retraining and to maintain the model performance through time and data drifts.
- More Sophisticated Emergency Level Classification: Currently, the emergency level (low, medium, high) is only based on the number of classes/ categories a message is classified into (meds, food, water, etc.). In the future, a more sophisticated method of determining this could be developed.
