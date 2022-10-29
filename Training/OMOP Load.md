## Generate mock OMOP dataset

We're going to leverage the work of Michael Shamberger who created a downloadable OMOP from synthea. https://forums.ohdsi.org/t/synthetic-data-with-simulated-covid-outbreak/10256 
The raw data already exists in folder `data` so feel free to browse that and load the data into mysql. (https://medium.com/macoclock/mysql-on-mac-getting-started-cecb65b78e) But you should be aware we need a flat file aggregate of any database file. A report in most peoples parlance. Generate your own fresh flat file with a sql statement of your choice after that you will load the data into a database engine. I've dropped some example SQL statements in the SQL folder. I'm only premaking the output for the tutorial file as I imagine most people will use this with real data.

Using the ./SQL/Example_Cohort_SQL_Statement.txt file I created the following file you can find in the database.

Creating file: COVID19Patients.csv
Columns:
person_id = The identity key
start_date = The Start date of COVID 19
C19_identification_visit_id = The visit ID where COVID was identified
Source = is the plain text from measurement
Gender = Male/Female/Unknown
Age = The age
Race_source_value = The race 
Ethnicity_source_value = The reported ethnicity, Hispanic/non-hispanic

---

After your file is loaded run SQL queries

```bash
--Purpose - pull together all covid19 positive patients into a single table
--Creator/Owner/contact - Jeremy Harper 
--Description - This gets all people with a measurement or a problem list indicating C19. 
select measurement.person_id, measurement.measurement_date as start_date, measurement.value_as_concept_name as description, measurement.visit_occurrence_id as C19_identification_visit_id, "concept_651620200" as source --measurement.data_partner_id
from measurement 
--At the time of writing, measurement_source_concept_id got 64706, measurement concept id got 109526, both got 101093 it looks like measurement concept id is the best choice. 
left join concept_set_members on measurement.measurement_concept_id=concept_set_members.concept_id
--The concept grabs all current potential concept_id's. The Value indicates it is positive result
where concept_set_members.codeset_id in ('651620200') and (measurement.value_as_concept_id in ('4126681', '45877985', '45884084', '9191'))
union all
--This grabs everyone with a problem list item
select person_id, MIN(condition_start_datetime) as start_date, first(condition_concept_name) as description, first(visit_occurrence_id) as C19_identification_visit_id, "condition_37311061" as source
from condition_occurrence
where condition_occurrence.condition_concept_id=37311061
group by person_id
```

Example 1
```bash
--Purpose - Calculate age and decade grouping
--Creator/Owner/contact - Jeremy Harper 
--Description - This takes everyone can creates an age column at time of C19 and a age_group column. Note I chose to use an assumption of everyone being born 1/1/year. This is wrong, you could also list out years but that seems to create problems in 2021 etc. 
select C19_Positive_Hospitalization.person_id, C19_Positive_Hospitalization.start_date, C19_Positive_Hospitalization.description, C19_Positive_Hospitalization.C19_identification_visit_id, C19_Positive_Hospitalization.Hospitalization_visit_id, C19_Positive_Hospitalization.hospitalization, C19_Positive_Hospitalization.source, round(Age_At_C19_temp, 2) as Age_At_C19, if(round(Age_At_C19_temp, 1) between 0 and 9.9,"0-9",if(round(Age_At_C19_temp, 1) between 10 and 19.9,"10-19",if(round(Age_At_C19_temp, 1) between 20 and 29.9,"20-29",if(round(Age_At_C19_temp, 1) between 30 and 39.9,"30-39",if(round(Age_At_C19_temp, 1) between 40 and 49.9,"40-49",if(round(Age_At_C19_temp, 1) between 50 and 59.9,"50-59",if(round(Age_At_C19_temp, 1) between 60 and 69.9,"60-69",if(round(Age_At_C19_temp, 1) between 70 and 79.9,"70-79",if(round(Age_At_C19_temp, 1) between 80 and 89.9,"80-89",if(round(Age_At_C19_temp, 1) between 90 and 99.9,"90-99",if(round(Age_At_C19_temp, 1) between 100 and 109.9,"100-109",if(round(Age_At_C19_temp, 1) between 110 and 119.9,"110-119","ERROR")))))))))))) as age_group
from (
    select C19_Positive_Hospitalization.person_id, C19_Positive_Hospitalization.start_date, C19_Positive_Hospitalization.description, C19_Positive_Hospitalization.C19_identification_visit_id, C19_Positive_Hospitalization.Hospitalization_visit_id, C19_Positive_Hospitalization.hospitalization, C19_Positive_Hospitalization.source, datediff(C19_Positive_Hospitalization.start_date,PPL.fake_dob)/365 as Age_At_C19_temp
from C19_Positive_Hospitalization
--If you just want a year without any other considerations get rid of date diff above and insert this as age_at_c19_temp: (year(C19_Positive_Hospitalization.start_date) - person.year_of_birth)
left outer join (select person.person_id, 
  concat(if(person.year_of_birth is not null, person.year_of_birth, '01'),
   '-', if(person.month_of_birth is not null, person.month_of_birth, '01'), '-', if(person.day_of_birth is not null, person.day_of_birth, '01')
   ) as fake_dob
from person) PPL on C19_Positive_Hospitalization.person_id=PPL.person_id
) as C19_Positive_Hospitalization 
```

Example 2
```bash
--Purpose - Add Hospitalization Information
--Creator/Owner/contact - Jeremy Harper 
--Description - This takes a list of people with a specific event date (COVID19) and looks for hospitalization in the 15 days pre/post the date. Note that you might want to restructure this to look at the specific encounter that is listed from the original generated on C19 patients, here we only look at whether the encounter for what we define as inpatient has happened between plus/minus 15 days. Currently 86% result in null
SELECT COVID19_Positive_Identification.person_id, COVID19_Positive_Identification.start_date, COVID19_Positive_Identification.description, COVID19_Positive_Identification.C19_identification_visit_id, COVID19_Positive_Identification.source,visit_occurrence.visit_occurrence_id as Hospitalization_visit_id, if(visit_occurrence.visit_occurrence_id is not Null, "Hospitalized", "Not_Hospitalized") as hospitalization
FROM COVID19_Positive_Identification
left outer join visit_occurrence on COVID19_Positive_Identification.person_id=visit_occurrence.person_id and (visit_occurrence.visit_concept_name like "Inpatient Critical Care Facility" OR visit_occurrence.visit_concept_name like "Inpatient Visit" OR visit_occurrence.visit_concept_name like "Inpatient Hospital" OR visit_occurrence.visit_concept_name like "Emergency Room and Inpatient Visit" OR visit_occurrence.visit_concept_name like "Inpatient Critical Care Facility") 
--immediately above I opted to use visit_concept_name, long term you might want to migrate to equivalent codes instead
-- immediately below is the +-15 day constraint. Tune as you see fit
and DATEDIFF (COVID19_Positive_Identification.start_date, visit_occurrence.visit_start_date) between -15 and 15
```



Example 3
```bash
--Purpose - group conditions from the dataset and count number of people who have C19 and condition
--Creator/Owner/contact - Jeremy Harper 
--Last Update - 11/10/2020
--Description - this is very simple count
SELECT condition_occurrence.condition_type_concept_id, condition_occurrence.condition_source_value, count(condition_occurrence.person_id) as condition_count
FROM condition_occurrence
left outer join C19_positive_persons on condition_occurrence.person_id=C19_positive_persons.person_id
where C19_positive_persons.person_id is not null
group by condition_occurrence.condition_type_concept_id, condition_occurrence.condition_source_value
```