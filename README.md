# Emergency Messages Data & Analytics Platform

### Project Overview
Every now and then, disasters and emergencies could happen, and while people may do their best to prepare for it, something unexpected can always arise, and  during this time, it is crucial to receive the necessary help quickly. The rise of internet and social media has made communication easy, but manual processing of emergencies and requests for help is still time-consuming, as understanding the situation and the needs of the person in distress may not be so straightforward. This project aims to solve this problem by building an end-to-end pipeline that stores, analyses, and classifies emergency messages, using techniques from data engineering, data science, and machine learning.

The structure of this repository can be viewed below.

    .
    ├── notebooks/                                         # Contains Jupyter notebooks for exploration & experimentation
    │  ├── Data Augmentation.ipynb                         # Adding additional columns to better suit project use case
    │  ├── Data Cleaning.ipynb                             # Removing redundant data to better suit project use case
    │  ├── Exploratory Data Analysis with Spark.ipynb      # Exploring the data with PySpark
    │  ├── ML Model Building.ipynb                         # Random forest model training for message categories prediction
    │  ├── Prediction Illustration.ipynb                   # Illustrate prediction process
    ├── dags/
    │  ├── __init__.py
    │  ├── msg_classifier.py                               # Python script for Airflow DAG
    ├── images/                                            # Contains images used in README
    └── README.md

The data that is used in this project is the multilingual disaster response messages data. This dataset, along with its description, can be accessed [here](https://www.kaggle.com/datasets/landlord/multilingual-disaster-response-messages).

### Business Process
The main process considered in this project is after an emergency message has been submitted. For future development, we propose a mobile app as the main entry point for these messages. Through the app, the use will be prompted to describe their emergencies and optinally select the request categories of their emergencies (meds, food, water, etc.), before submitting the request. The ID, date, and language, will be automatically added. If a user labels/ categorizes their message, then there will be a 1 or 0 value, indicating yes or no, in each of the target variables (meds, food, water, etc.).

To better follow the process of submitting an emergency message, a mockup of the emergency message mobile app can be viewed and interacted with [here](https://rp.mockplus.com/run/mZjA1toNnZ/lcyvCAMMEB?cps=hide&rps=hide&nav=1&ha=0&la=0&fc=0&dt=iphoneX&out=0&rt=1).

![Mockup](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Screenshot_2022-11-17_at_9.35.33_PM-removebg.png)

Once submitted. the message will be stored, processed and analysed using a pre-trained machine learning model, which will predict the request categories of the emergency message. Based on those predictions, the level of the emergency (low, medium, high) will also be determined. As more messages are submitted, the size of the data will grow and business users can then analyse and view insights through queries, reports, and dashboards.

### Solution Architecture
The solution architecture of this project can be viewed below. The main tools that are used include Python, Spark, Airflow, and Amazon Web Services.

![Architecture](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Picture3.png)

Aligning with the business process, when an emergency message is submitted, it will first be stored in the staging layer in S3. This raw data will then be checked for data quality, then passed into the processing layer. The pre-train machine learning model will take the data here as input, and the predictions, along with other analyses, will be stored alongside the input data in one table, in the refined layer. From there, data transformations will be applied to transform the data into a star schema model, which will then be stored in a Redshift data warehouse. The data pipelines used will be managed by Apache Airflow.

Insert Airflow DAGs screenshot here.

Data in the data warehouse can then be queried into the consumption zone for further business analysis, or passed into BI tools, such as Power BI, to be viewed in a dashboard format.

From time to time, offline copies of the data in the staging layer can also be passed into the exploratory zone, where data science and machine learning activities are conducted. This is where new machine learning models are experimented and trained in. Tools that can be used here include Python, Jupyter notebooks, Scikit-learn, Spark, as well as GitHub as the code repository.

### Data Consumption
As mentioned in the previous section, the data in the data warehouse will follow a star schema. In our case, there will be one fact table and three dimension tables. These three dimension tables will contain information about the dates, languages, and emergency category levels, respectively. The star schema data model can be viewed below.

![Schema](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Picture2.png)

An example use case for the consumption zone would be to query the data in the data warehouse and pass it to be viewed in a Power BI dashboard. An example query would be:
                      
    SELECT Msg_Fact.*, Date_Dim.date, Lang_Dim.language, Cat_Dim.category 
    FROM Msg_Fact LEFT JOIN Date_Dim 
    ON Msg_Fact.date_ID = Date_Dim.date_ID 
    LEFT JOIN Lang_Dim 
    ON Msg_Fact.language_ID = Lang_Dim.language_ID 
    LEFT JOIN Cat_Dim 
    ON Msg_Fact.category_ID = Cat_Dim.category_ID;
    
A sample Power BI dashboard using the data from the above query has also been created. The dashboard can be seen below.

![Dashboard](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Dashboard.png)

From the dashboard, business users can oberve the trends in the number of messages submitted throughout the years. They can also observe the proportion of related and labeled messages, from a variety of languages. Furthermore, the number of low, medium, and high emergency messages are also shown. Finally, business users can also identify the leading cause of emergencies using the treemap located in the bottom right area of the dashboard.

### Future Development
Some recommendations which could be taken in consideration, for future development, include:
- Improving the Hardware: The hardware specifications, such as the number of clusters or the data refresh rate, could be increased. This might help to provide services to a larger amount of users and offer real-time predictions.
- Machine Learning Model Retraining Pipeline: MLOps could be included as a part of the architecture, to provide model retraining and maintain the performance through time and data drifts.
- More Sophisticated Emergency Level Classification: Currently, the emergency level (low, medium, high) is only based on the number of classes/ categories a message is classified into (food, water, electricity, etc.) In the future, a more sophisticated method of determining this could be developed.
