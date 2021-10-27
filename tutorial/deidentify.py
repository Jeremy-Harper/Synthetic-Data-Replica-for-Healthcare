'''
Takes the data generated and runs it through a
set of de-identification steps. It then saves this as a new dataset.
'''
import random 
import time
import string

import pandas as pd
import numpy as np

import filepaths


def main():
    print('running de-identification steps...')
    start = time.time()

    # "_df" is the usual way people refer to a Pandas DataFrame object
    OMOP_data_df = pd.read_csv(filepaths.OMOP_data)

    print('removing source...')
    OMOP_data_df = remove_source(OMOP_data_df)

    #print('replacing Hospital with random number...')
    #OMOP_data_df = replace_hospital_with_random_number(OMOP_data_df)

    print('removing non-male-or-female from gender ...')
    OMOP_data_df = remove_non_male_or_female(OMOP_data_df)

    print('putting ages in age brackets...')
    OMOP_data_df = add_age_brackets(OMOP_data_df)

    OMOP_data_df.to_csv(filepaths.omop_data_deidentify, index=False)

    elapsed = round(time.time() - start, 2)
    print('done in ' + str(elapsed) + ' seconds.')


def remove_source(OMOP_data_df: pd.DataFrame) -> pd.DataFrame:
    """Drops the Source column from the dataset, we don't need it and it gives you a framework to delete columns

    Keyword arguments:
    OMOP_data_df -- 
    """
    OMOP_data_df = OMOP_data_df.drop('Source', 1)
    return OMOP_data_df



def replace_hospital_with_random_number(
        OMOP_data_df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Gives each hospital a random integer number and adds a new column
    with these numbers. Drops the hospital name column. 

    Keyword arguments:
    OMOP_data_df -- Hopsitals A&E records dataframe
    """

    hospitals = OMOP_data_df['Hospital'].unique().tolist()
    random.shuffle(hospitals)
    hospitals_map = {
        hospital : ''.join(random.choices(string.digits, k=6))
        for hospital in hospitals
    }
    OMOP_data_df['Hospital ID'] = OMOP_data_df['Hospital'].map(hospitals_map)
    OMOP_data_df = OMOP_data_df.drop('Hospital', 1)

    return OMOP_data_df



def remove_non_male_or_female(OMOP_data_df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Removes any record which has a non-male-or-female entry for gender. 

    Keyword arguments:
    OMOP_data_df -- Hopsitals A&E records dataframe
    """

    OMOP_data_df = OMOP_data_df[OMOP_data_df['Gender'].isin(['Male', 'Female'])]
    return OMOP_data_df


def add_age_brackets(OMOP_data_df: pd.DataFrame) -> pd.DataFrame:
    """
    Put the ages in to age brackets 

    Keyword arguments:
    OMOP_data_df -- Hopsitals A&E records dataframe
    """

    OMOP_data_df['Age bracket'] = pd.cut(
        OMOP_data_df['Age'], 
        bins=[0, 18, 25, 45, 65, 85, 150], 
        labels=['0-17', '18-24', '25-44', '45-64', '65-84', '85-'], 
        include_lowest=True
    )
    OMOP_data_df = OMOP_data_df.drop('Age', 1)
    return OMOP_data_df


if __name__ == "__main__":
    main()
