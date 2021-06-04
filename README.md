In developing country like India, people face lots of problem in day today life. Major of them
are Potholes on the roads, Garbage on the streets, sewage leakage etc. These problems cause
many accident and thousands of people lose their lives every year. These problems sometimes
takes months or even years to get solved if existing system is followed, there is no proper
platform or system to make complaints about the issues and these problems remain
unaddressed. Sometimes even if a person approaches the local authorities the problems are
unheard and there is no record of the complaint.

## What is Sahayak?
* Sahayak is an AI Enabled citizen grievance monitoring and response system
for reporting grievances observed and faced by local people in their day
to day life.
* Its one click grievance reporting system which will be fed with pictures
of different problems such as garbage spill, potholes, no parkings, stray
dogs etc. with its location to an AI model which will classify the category
of the problems and assigns task to respected authorities.
* Using Data Analysis and Data visualization Sahayak provides a
dashboard to get visual reports of their area weekly, monthly, annually
using different graphs and data visualization techniques which can be
viewed by the authorities as well as by the normal users so there will a
transparent process and complaints can be tracked.


## Techstack
1. Flask -RESTful service.
2. FastAi model - for grievance classification trained at 98% accuracy.
3. React native for Android and IOS application.
4. Mongodb Atlas cluster.
5. HERE maps API.

## Installation

1. Clone the repo
```sh
   https://github.com/vig2306/Sahayak-Mip.git
```

2. Add the required libraries using pip for the server side

```sh
   pip install -r requirements.txt
```
3. For the mobile application move to the app folder and run the command

```sh
   npm i
```
4. After the packages have been installed to run the mobile application

```sh
   expo start
```
5. To run the server

```sh
   python runner.py
```

