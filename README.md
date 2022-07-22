# melk
Corpus Gathering and Analysis Framework

![License: CC0-1.0](https://img.shields.io/github/license/flnasc/melk)
![Python version: 3.9](https://img.shields.io/badge/python-3.9-blue)
![Code style: black](https://img.shields.io/badge/code%20style-black-black)

### Project Description 
Project Melk is a tool that allows digital humanities instructors and students without significant technical backgrounds to easily collect large datasets about specific research topics from social networks and other online media sources. The tool is pedagogical in nature- rather than attempt to provide fine grained control of every aspect of data collection, it gives students a simple, approachable interface with which to collect datasets that will allow them to explore digital text analysis methods. 

The ultimate goal of this project is to make an important research method accessible to students and researchers without backgrounds in computer science. We hope it will enable professors to introduce their students to the novel insights enabled by computational analysis methods without requiring them to spend a prohibitively high amount of time wrestling with the mechanics of data collection. 

### Supported Sources 
![The New York Times](https://developer.nytimes.com/files/poweredby_nytimes_150c.png?v=1583354208341)
<img width="105" alt="Reddit Logo" src="https://user-images.githubusercontent.com/63132911/180308426-5033dbc5-c96f-4541-800b-0cec69a7e7aa.png">
![2021 Twitter logo - blue](https://user-images.githubusercontent.com/63132911/180309613-de537691-68f4-4d8f-8a9e-2b7752a261e9.png)


- The New York Times 
- Reddit 
- Twitter 

- Local datasets including:
  - Billboard Top 100 Song Lyrics Archive
  - Poetry Foundation Archive
  - State of the Union Archive 

### Usage
Project Melk is primarily intended to be used via its web interface, which is currently under development. 

However, you can also use the gatherer module on your computer to create datasets. Unlike the web interface, this will require some work using the command line and Python. Instructions for Mac: 

##### Clone repository

Open the terminal, then navigate to the folder you would like to download the melk program into. Clone this directory like so:

```git clone https://github.com/flnasc/melk```

##### Import required packages

##### Optional: Configure API keys 

If you want to access sources (New York Times, Twitter) that require API keys, open the apiconfig.py file and enter your own API key and bearer token from those sources, then save the file. The Twitter gatherer expects an API key with Academic level access to be able to search the full Twitter archive. The gatherer will fail if you try to access sources that require an API key without providing one in apiconfig.py.

##### Run gatherer.py 

This will create a csv file under the `outputs` folder in your working directory that contains your data. 





