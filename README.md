# Emergency Messages Data & Analytics Platform
![Header](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Screenshot%202022-11-18%20at%202.02.33%20PM.png)

### Project Overview
Every now and then, disasters and emergencies could happen, and while people may do their best to prepare for it, something unexpected can always arise, and  during this time, it is crucial to receive the necessary help quickly. The rise of internet and social media has made communication easy, but manual processing of emergencies and requests for help is still time-consuming, as understanding the situation and the needs of the person in distress may not be so straightforward. This project aims to solve this problem by building an end-to-end pipeline that stores, analyses, and classifies emergency messages, using techniques from data engineering, data science, and machine learning.

The structure of this repository can be viewed below.

    .
    ├── models                            
    │  ├── __init__.py
    │  ├── ngram_nlm.py                           # language model algorithm
    ├── readers                 
    │  ├── _init_.py
    │  ├── ngram_dataset.py                       # Load dataset
    ├── _init_.py
    ├── lm.py                                     # Performs the language modelling
    ├── images
    └── README.md

### Business Process
The main process considered in this project is after an emergency message has been submitted. For future development, we propose a mobile app as the main entry point for these messages. Through the app, the use will be prompted to describe their emergencies and optinally select the categories of their emergencies (meds, food, water, etc.), before submitting the request. To better follow the process of submitting an emergency message, a mockup of the emergency message mobile app can be viewed and interacted with [here](https://rp.mockplus.com/run/mZjA1toNnZ/lcyvCAMMEB?cps=hide&rps=hide&nav=1&ha=0&la=0&fc=0&dt=iphoneX&out=0&rt=1).

![Mockup](https://github.com/Gianatmaja/Emergency-Messages-Data-Analytics-Platform/blob/main/Images/Screenshot%202022-11-17%20at%209.35.33%20PM.png)

Once submitted
