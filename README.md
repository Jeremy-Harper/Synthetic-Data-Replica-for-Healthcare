#  Synthetic-Data-Replica-for-Healthcare

## Description
 
**What is this?**

This manual provides a practical guide to generating synthetic data replicas from healthcare datasets using Python. It specifically utilizes the OMOP (Observational Medical Outcomes Partnership) data schema, widely adopted in medical research.

**Understanding Synthetic Data replicas**

A synthetic data replica is algorithmically generated to replicate the statistical characteristics of an original dataset without using any specific data from it post-training. In healthcare, this technique is instrumental in preserving patient confidentiality and surpassing HIPAA compliance requirements by removing data from HIPAA-regulated environments.

**Types of Synthetic Data Builds**

We cover four synthetic data build methods:

Random Distribution: Mimics original datasets with evenly distributed values. Ideal for sharing data while preventing reidentification.
*Comparison of ages in original (left) and random synthetic (right)*
![Random mode age bracket histograms](plots/random_Age_bracket.png)

Independent Attributes: Generates datasets with statistically accurate columns but without inter-column correlations. Less relevant in healthcare contexts.
*Comparison of ages in original (left) and correlated synthetic (right)*
![correlated mode age bracket histograms](plots/correlated_Age_bracket.png)

Correlated Attributes: Employs Bayesian Networks to maintain inter-column statistical correlations, though limited in capturing complex relationships. (Often struggles with small count examples, and good with secondary relationships between columns but tertiary relationships between columns may fail)

Time Series: Preserves chronological order and relationships, crucial for healthcare data but computationally intensive.

**Intended Audience?**

This tutorial is designed for individuals seeking to create synthetic replicas of healthcare data.

**About the Author?**

Jeremy Harper, a Biomedical Informatician, offers his expertise and consultancy in this area.

**Implementing this Technology in Your Research Environment?**

The process of integrating synthetic data replica technology into your research framework involves several key steps, ensuring both compliance with regulations and effective utilization of the technology.

Step 1: Engage with Institutional Review Boards (IRB)

The initial step involves collaborating with your organization's Institutional Review Board (IRB). The goal here is two-fold:

**IRB Approval:** Seek an official determination from the IRB that the use of synthetic data replicas qualifies as non-human subjects research. This distinction is crucial as it impacts the regulatory oversight and ethical considerations of your research projects.

**Data Broker Identification:** While engaging with the IRB, it is also essential to identify and gain approval for an 'honest data broker'. This entity will play a pivotal role in managing and overseeing the use of data, ensuring that patient privacy is upheld. Their role is particularly critical in maintaining the integrity of the data handling process, especially in contexts where patient confidentiality and data security are paramount.

Step 2: Data Reporting from Healthcare Systems

After securing IRB approval and establishing a data broker, the next step involves the actual data handling process:

**Source Data Selection:** Identify the specific datasets within your healthcare system that you intend to use for creating synthetic replicas. This decision should be guided by your research objectives and the relevance of the data to your study.

**Data Extraction and Reporting:** Extract these datasets from your healthcare system's production environment. This process should be conducted in accordance with your organization's data governance and IT security policies. The extracted data will serve as the foundation for the synthetic data generation process.

Step 3: Generation and Utilization of Synthetic Data

With the source data in hand, you can now proceed to the generation of synthetic data:

**Module Utilization:** Employ the modules and techniques outlined in this tutorial to transform the extracted datasets into synthetic replicas. This step involves the application of algorithms and methods described earlier, such as random distribution, independent attributes, correlated attributes, and time series analysis.

***Data Sharing and Research Application:*** Once the synthetic datasets are generated, they can be utilized for your research purposes. Due to their de-identified nature, these datasets can facilitate a wide range of research activities while significantly mitigating privacy concerns. They are particularly useful in scenarios where accessing real patient data is restricted or impractical.

**Continued Compliance and Evaluation:** It's important to continually assess the synthetic data for compliance with privacy standards and relevance to research goals. Regular reviews and updates may be necessary to align the synthetic data with evolving research needs and regulatory landscapes.

## Overview

This tutorial offers a step-by-step guide for generating and analyzing synthetic data replicas from healthcare datasets. The focus is on using a simulated version of the OMOP schema to demonstrate these techniques, which are applicable even though the data may not appear entirely realistic.
### Key Steps in the Process
1. Data Preparation

    **Create a Flat File for Synthesis:** Begin by preparing a flat file that serves as the basis for data synthesis. An example using COVID-19 patient data is provided (./data/COVID19Patients.csv).

    **Run Anonymization:** Apply anonymization techniques to the flat file to further protect patient privacy. The result is a de-identified dataset (/data/COVID19Patients_deidentify.csv).

2. Synthetic Data Generation

    **Generate Synthetic Datasets:** Use the provided modules to create various forms of synthetic data:
        Option A: Highly correlated dataset (./data/COVID19Patients_data_synthetic_correlated.csv) suitable for complex statistical analysis.
        Option B: Random dataset (./data/COVID19Patients_data_random.csv) for software development and testing.
        Option C: Independently attributed dataset (./data/COVID19Patients_data_random.csv) offering column-specific statistical representation without inter-data relationships.

3. Analysis and Evaluation

    **Compare and Analyze:** Examine the synthetic datasets to assess their similarity to the original data. This comparison is crucial to ensure the synthetic data's usefulness and reliability.

###Considerations and Caveats

   **Synthetic vs. Anonymization:** It's important to understand that synthetic data generation is not a substitute for data anonymization. While synthetic data does not contain direct personal information, patterns from the original data could be transferred, potentially leading to re-identification risks.

   **Dealing with Outliers:** Special attention should be given to outliers in the data. If the synthetic dataset replicates unique characteristics present in the original data, it may inadvertently lead to re-identification of individuals.

Practical Implementation Tips

    Starting with a Test File: It's advisable to initially run the synthesis process using the provided example files. This approach allows you to familiarize yourself with the process and troubleshoot any issues before applying it to more complex datasets.

    Understanding Dataset Limitations: The synthetic data generated will not perfectly mirror real-world datasets, especially in terms of data missingness. This limitation is an inherent part of using publicly available datasets for training purposes.



## Setup

Commands need to be run from a terminal, Python3 must be installed you can check in terminal with 

```bash
python --version
```

Install required dependent libraries in a virtual environment. You can do that, for example, with venv in ubuntu https://realpython.com/python-virtual-environments-a-primer/

Create the virtual environment. 

```bash
python3 -m venv /path/
```

Activate the new environment you created. 

```bash
source ./venv/bin/activate
```

 (If you are running an M1 Mac you may need to run the following for matlab "brew install pkg-config" and "brew install freetype")

```bash
cd /path/to/repo/synthetic_data_tutorial/
python3 -m venv ./omop_venv
source ./omop_venv/bin/activate
pip3 install -r requirements_freeze.txt
pip3 install -r requirements.txt
sudo apt-get install python3-tk
```
python3-tk: Tk is a Tcl package implemented in C that adds custom commands to create and manipulate GUI widgets.

## Generate mock OMOP dataset

See /Training/OMOP Load.md

## De-identification

If you are going to run this in a production environment please practice de-identification at /Training/deidentification.md

We want to deidentify datasets wherever possible to further lower patient reidentification risks

## Synthetic data replica

In this section, we delve into the creation of three distinct types of synthetic datasets: Random, Independent, Correlated, and Time Series. Each type serves a unique purpose and offers different levels of statistical resemblance to the original data.

Synthetic data exists on a spectrum from merely the same columns and datatypes as the original data (Random) all the way to carrying approximately all of the statistical patterns of the original dataset (Correlated|Time Series).

**Time Series** uses a different code base from the other three. This is because with time series we need to maintain strict ordering, and relationships between time and measurement values. 

> In **correlated attribute mode**, the software will learn a differentially private Bayesian network capturing the correlation structure between attributes, then draw samples from this model to construct the result dataset.
>
> In cases where the correlated attribute mode is too computationally expensive or when there is insufficient data to derive a reasonable model, one can use an **independent attribute mode**. In this mode, a histogram is derived for each attribute, noise is added to the histogram to achieve differential privacy, and then samples are drawn for each attribute. This is not often helpful in healthcare as we want related variables but its good to know that another technique is available.
>
> For cases where you want no relationship to the patient data, one can use **random mode** that simply generates type-consistent random values for each attribute so if you have 4 zip codes in your database each will be assigned to 25% of the fields.


### Differential privacy and Bayesian networks

We have the option of using differential privacy for anonymization, we are turning it on in a very lightweight manner, if you are using this in production you will want to evaluate your organizations requirements. If you care to learn more about differential privacy this article from accessnow might help (https://www.accessnow.org/understanding-differential-privacy-matters-digital-rights/).

Bayesian networks are graphs with directions which model the statistical relationship between a dataset's variables. It does this by saying certain variables are "parents" of others, that is, their value influences their "children" variables. Parent variables can influence children but children can't influence parents. In our case, if patient age is a parent of waiting time, it means the age of patient influences how long they wait, but how long they doesn't influence their age. So by using Bayesian Networks, we can model these influences and use this model in generating the synthetic data. (https://www.probabilisticworld.com/bayesian-belief-networks-part-1/)

### Notes on Timing

The data generated from synthea didn't have any missingness, it will in a real world dataset. That allows these models to be run VERY VERY quickly. I strongly suggest running the file I've given you FIRST to test whether it is working. To give you an idea of how Degrees of Bayesian network can add time on the rather slow home machine I'm running I've run the following:

With no missingness:
Degree 1 took 30 seconds
Degree 2 degrees its 45
Degree 3 degrees its 120

With Missingness and no deidentification
Degree 1 2000 Seconds (32 Minutes)
Degree 3 2044 Seconds (34 Minutes)



### Random mode

Command to run to generate 10,000 rows of random data from your source dataset

```bash
python3 ./tutorial/synthesize.py     \
--input_file_name='COVID19Patients_deidentify'     \
--mode='random'     \
--row_count=10000
```

Command to generate the same number of rows of data within +-5% of the original, you can crank that up to 50% but be aware that is can half the size of your output dataset as its a random selection. 

```bash
python3 ./tutorial/synthesize.py     \
--input_file_name='COVID19Patients_deidentify'     \
--mode='random'     \
--activate_percentage='Yes'     \
--row_percentage=5
```

Remember Random mode will give you a dataset that has roughly a similar size and that the datatypes and columns align with the source.

#### Attribute Comparison

We'll compare each attribute in the original data to the synthetic data by reviewing the generated plots of histograms. Look in the ./plots folder for the output.

*note, the original dataset is on the left, the synthetic dataset is on the right.

Let's look at the histogram plots now for a few of the attributes. We can see that the generated data is random and doesn't contain any information about averages or distributions.

*Comparison of ages in original data (left) and random synthetic data (right)*
![Random mode age bracket histograms](plots/random_Age_bracket.png)

*Comparison of Ethnicity in original data (left) and random synthetic data (right)*
![Random mode Ethnicity bracket histograms](plots/random_ethnicity_source_value.png)

*Comparison of race in original data (left) and random synthetic data (right)*
![Random mode race bracket histograms](plots/random_race_source_value.png)

*Comparison of all variables via heatmap in original data (left) and random synthetic data (right)*
![Random mode mutual_information bracket histograms](plots/mutual_information_heatmap_random.png)
Learn more about how to read this: http://www.scholarpedia.org/article/Mutual_information)

### Independent attribute mode
*I recommend you skip and go to correlated*
What if we had the use case where we wanted to build models to analyze the medians of ages, or race in the synthetic data but no other variable relationships? In this case we'd use independent attribute mode.

Command to run to generate 10,000 rows of independent data from your source dataset

```bash
python3 ./tutorial/synthesize.py     \
--input_file_name='COVID19Patients_deidentify'     \
--mode='independent'     \
--row_count=10000
```

Command to generate the same number of rows of data within +-5% of the original, you can crank that up to 50% but be aware that is can half the size of your output dataset. 

```bash
python3 ./tutorial/synthesize.py     \
--input_file_name='COVID19Patients_deidentify'     \
--mode='independent'     \
--activate_percentage='Yes'     \
--row_percentage=5
```

Attribute Comparison: Independent

Comparing the attribute histograms we see the independent mode captures the distributions mildly accurately. You can see the synthetic data is somewhat similar but not exactly.


### Correlated attribute mode - include correlations between columns in the data

If we want to capture correlated variables, for instance if patient is related to waiting times, we'll need correlated data. To do this we use *correlated mode*.

#### Data Description: Correlated

There's a couple of parameters that are different here so we'll explain them.

`epsilon_count` is a value for DataSynthesizer's differential privacy which says the amount of noise to add to the data - the higher the value, the more noise and therefore more privacy.

`bayesian_network_degree` is the maximum number of parents in a Bayesian network, i.e., the maximum number of incoming edges. For simplicity's sake, we're going to set this to 1, saying that for a variable only one other variable can influence it. You'll want to crank this higher depending on how many columns your database has to make it more realistic

Command to run to generate 10,000 rows of Correlated data from your source dataset

```bash
python3 ./tutorial/synthesize.py     \
--input_file_name='COVID19Patients_deidentify'     \
--bayesian_network_degree=1     \
--epsilon_count=10     \
--mode='correlated'     \
--row_count=10000
```

Command to generate the same number of rows of data within +-5% of the original, you can crank that up to 50% but be aware that is can half the size of your output dataset. 

```bash
python3 ./tutorial/synthesize.py     \
--input_file_name='COVID19Patients_deidentify'     \
--bayesian_network_degree=1     \
--epsilon_count=10     \
--mode='correlated'     \
--activate_percentage='Yes'     \
--row_percentage=5
```

#### Attribute Comparison: Correlated

We can see correlated mode keeps similar distributions also. It looks the exact same but if you look closely there are small differences in the distributions, crank up epsilon and you'll see bigger disparities.

*Comparison of ages in original data (left) and correlated synthetic data (right)*
![correlated mode age bracket histograms](plots/correlated_Age_bracket.png)

*Comparison of Ethnicity in original data (left) and correlated synthetic data (right)*
![correlated mode Ethnicity bracket histograms](plots/correlated_ethnicity_source_value.png)

*Comparison of race in original data (left) and correlated synthetic data (right)*
![correlated mode race bracket histograms](plots/correlated_race_source_value.png)

*Comparison of all variables via heatmap in original data (left) and correlated synthetic data (right)*
![correlated mode mutual_information bracket histograms](plots/Missingness_Run/mutual_information_heatmap_correlated.png)
Learn more about how to read this: http://www.scholarpedia.org/article/Mutual_information)


#### Custom Run's for other flat files

Data Description Examples that are hardcoded in synthesize.py

The first step is to create a description of the data, defining the datatypes and which are the categorical variables.

Example1:

```python
attribute_to_datatype = {
    'person_id': 'Integer',
    'start_date': 'String', 
    'C19_identification_visit_id': 'String',
    'Gender': 'String', 
    'race_source_value': 'String', 
    'ethnicity_source_value': 'String', 
    'Age bracket': 'String' 
}

attribute_is_categorical = {
    'person_id': False, 
    'start_date': False, 
    'C19_identification_visit_id': False,
    'Gender': True,  
    'race_source_value': True, 
    'ethnicity_source_value': True,     
    'Age bracket': True
}
```

Example2:

```python
attribute_to_datatype = {
    'Time in A&E (mins)': 'Integer',
    'Treatment': 'String',
    'Gender': 'String',
    'Index of Multiple Deprivation Decile': 'Integer',
    'Hospital ID': 'String',
    'Arrival Date': 'String',
    'Arrival hour range': 'String',  
    'Age bracket': 'String'
}

attribute_is_categorical = {
    'Hospital ID': True,
    'Time in A&E (mins)': False,
    'Treatment': True,
    'Gender': True,
    'Index of Multiple Deprivation Decile': False,
    'Arrival Date': True,
    'Arrival hour range': True,  
    'Age bracket': True
}
```

*Note, ideally we'll expand this with a list of expected names/types so that it doesn't need modification to match each flat file.



### Time Series Data
Time Series Data Here is a step by step created by Greta AI

https://towardsdatascience.com/creating-synthetic-time-series-data-67223ff08e34

Here are another few github repos which is actively generating synthetic data.
https://github.com/sdv-dev/SDV

https://github.com/ydataai/ydata-synthetic

https://www.kdnuggets.com/2022/06/generate-synthetic-timeseries-data-opensource-tools.html



### Wrap-up

This is the end of the tutorial.


## Credit to others

This tutorial is a tailored, updated version of https://github.com/theodi/synthetic-data-tutorial Which was originally inspired by the [NHS England and ODI Leeds' research](https://odileeds.org/events/synae/) in creating a synthetic dataset from NHS England's accident and emergency admissions. 

The synthetic data generating library they used was [DataSynthetizer]( https://github.com/DataResponsibly/DataSynthesizer) and comes as part of this codebase. 

---
### DataSynthesizer

This is powered through an open source project called, DataSynthesizer. Which is able to generate synthetic datasets of arbitrary size by sampling from the probabilistic model in the dataset description file.

We've created and inspected our synthetic datasets using three modules within it.

> 1. **DataDescriber**: investigates the data types, correlations and distributions of the attributes in the private dataset, and produces a data summary.
> 2. **DataGenerator**: samples from the summary computed by DataDescriber and outputs synthetic data
> 3. **ModelInspector**: creates plots comparing what was computed by DataDescriber, allowing you to evaluate the accuracy of the summarization process

---

---


### References I thought might be helpful for you

- [Exploring methods for synthetic A&E data](https://odileeds.org/blog/2019-01-24-exploring-methods-for-creating-synthetic-a-e-data) - Jonathan Pearson, NHS England with Open Data Institute Leeds.
- [DataSynthesizer: Privacy-Preserving Synthetic Datasets](https://faculty.washington.edu/billhowe/publications/pdfs/ping17datasynthesizer.pdf) Haoyue Ping, Julia Stoyanovich, and Bill Howe. 2017
