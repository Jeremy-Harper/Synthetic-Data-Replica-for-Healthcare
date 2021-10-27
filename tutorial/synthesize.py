'''
This generates synthetic data from the omop_data_deidentify.csv
file (not you can change the file target in filepaths.py. It generates correlated synthetic data and saves them under ./data as COVID19Patients_description_correlated.json and COVID19Patients_data_synthetic_correlated.csv 
'''

import random 
import os
import time
import argparse
import pandas as pd
import numpy as np

import filepaths
from DataDescriber import DataDescriber
from DataGenerator import DataGenerator
from ModelInspector import ModelInspector
from lib.utils import read_json_file


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


#args: str

def main():

    start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", default='./data_output', type=str, help="*NOT IMPLEMENTED* Where you want to have the comparison images and the datafiles saved.")
    parser.add_argument("--input_file_name", default='COVID19Patients_deidentify', type=str, help="Batch size per GPU/CPU for training.")
    parser.add_argument("--bayesian_network_degree", default=1, type=int, help="The degrees of bayesian relationships being looked at.")
    parser.add_argument("--epsilon_count", default=10, type=int, help="The amount of fuzziness injected to further obfuscate patient information")
    parser.add_argument("--mode", default='correlation', type=str, help="The three output options, 'random', 'independent', 'correlated'")
    parser.add_argument("--row_count", default=0, type=int, help="The default return value uses the same number of rows as you put in. This is overridden when you turn on the percentage!!")
    parser.add_argument("--activate_percentage", default='no', type=str, help="To use percentage mark this as 'Yes' otherwise percentage is ignored")
    parser.add_argument("--row_percentage", default=10, type=int, help="The default percentage of return is +-10% we use a random number generator to identify what direction we will go, you will have to edit code to make it work for your use case if that is unacceptable")
    args = parser.parse_args()

    # "_df" is the Pandas DataFrame we have to bring it in first so we can default the row count
    omop_data_deidentify = os.path.join(filepaths.data_dir, args.input_file_name+'.csv')
    omop_df = pd.read_csv(omop_data_deidentify)

    # Specify the number of rows to return to the engine
    if args.row_count == 0:
        num_rows = len(omop_df)
    else:
        num_rows = args.row_count
    if args.activate_percentage == 'Yes':
        #this chooses a random number between the top and bottom percentage
        random_number_between_percentage = random.randint(round(len(omop_df)*(1-(args.row_percentage/100))),round(len(omop_df)*(1+(args.row_percentage/100))))

        num_rows = round(random_number_between_percentage)

    # iterate through the mode variable to generate synthetic data, note this also assigns the mode variable
    for mode in [args.mode]: 
        #declaring the output data
        jsonfile = os.path.join(filepaths.data_dir, args.input_file_name+'_description_'+mode+'.json')
        outputfile = os.path.join(filepaths.data_dir, args.input_file_name+'_data_synthetic_'+mode+'.csv')


        print('describing synthetic data for', mode, 'mode...')
        describe_synthetic_data(args, mode, jsonfile)

        print('generating synthetic data for', mode, 'mode...')
        generate_synthetic_data(
            mode, 
            num_rows, 
            jsonfile,
            outputfile
        )

        print('comparing histograms for', mode, 'mode...')
        compare_histograms(
            mode, 
            omop_df, 
            jsonfile,
            outputfile
        )

        print('comparing pairwise mutual information for', mode, outputfile, 'mode...')
        compare_pairwise_mutual_information(
            mode, 
            omop_df, 
            jsonfile,
            outputfile
        )

    elapsed = round(time.time() - start, 0)
    print('done in ' + str(elapsed) + ' seconds.')


def describe_synthetic_data(args, mode: str, description_filepath:str):
    '''
    Describes the synthetic data and saves it to the data/ directory.

    Keyword arguments:
    mode -- what type of synthetic data
    category_threshold -- limit at which categories are considered blah
    description_filepath -- filepath to the data description
    '''
    describer = DataDescriber()
    print('second synthetic data for', mode, 'epsilon_count', args.epsilon_count, 'mode...')

    if mode == 'random':
        describer.describe_dataset_in_random_mode(
            filepaths.omop_data_deidentify,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical)
    
    elif mode == 'independent':
        describer.describe_dataset_in_independent_attribute_mode(
            filepaths.omop_data_deidentify,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical)
    
    elif mode == 'correlated':
        # Increase epsilon value to reduce the injected noises. 
        # We're using differential privacy in this tutorial, 
        # set epsilon=0 to turn off differential privacy 
        
        epsilon = args.epsilon_count

        # The maximum number of parents in Bayesian network
        # i.e., the maximum number of incoming edges.
        degree_of_bayesian_network = args.bayesian_network_degree

        describer.describe_dataset_in_correlated_attribute_mode(
            dataset_file=filepaths.omop_data_deidentify, 
            epsilon=epsilon, 
            k=degree_of_bayesian_network,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical)
            # attribute_to_is_candidate_key=attribute_to_is_candidate_key)

    describer.save_dataset_description_to_file(description_filepath)


def generate_synthetic_data(
        mode: str, 
        num_rows: int, 
        description_filepath: str,
        synthetic_data_filepath: str
    ):
    '''
    Generates the synthetic data and saves it to the data/ directory.

    Keyword arguments:
    mode -- what type of synthetic data
    num_rows -- number of rows in the synthetic dataset
    description_filepath -- filepath to the data description
    synthetic_data_filepath -- filepath to where synthetic data written
    '''
    generator = DataGenerator()

    if mode == 'random':
        generator.generate_dataset_in_random_mode(num_rows, description_filepath)
            
    elif mode == 'independent':
        generator.generate_dataset_in_independent_mode(num_rows, description_filepath)
    
    elif mode == 'correlated':
        generator.generate_dataset_in_correlated_attribute_mode(num_rows, description_filepath)

    generator.save_synthetic_data(synthetic_data_filepath)


def compare_histograms(
        mode: str, 
        omop_df: pd.DataFrame, 
        description_filepath: str,
        synthetic_data_filepath: str
    ):
    '''
    Makes comparison plots showing the histograms for each column in the 
    synthetic data.

    Keyword arguments:
    mode -- what type of synthetic data
    omop_df -- DataFrame of the original dataset
    description_filepath -- filepath to the data description
    synthetic_data_filepath -- filepath to where synthetic data written
    '''

    synthetic_df = pd.read_csv(synthetic_data_filepath)

    # Read attribute description from the dataset description file.
    attribute_description = read_json_file(
        description_filepath)['attribute_description']

    inspector = ModelInspector(
        omop_df, synthetic_df, attribute_description)

    for attribute in synthetic_df.columns:
        figure_filepath = os.path.join(
            filepaths.plots_dir, 
            mode + '_' + attribute + '.png'
        )
        # need to replace whitespace in filepath for Markdown reference
        figure_filepath = figure_filepath.replace(' ', '_')
        inspector.compare_histograms(attribute, figure_filepath)

def compare_pairwise_mutual_information(
        mode: str, 
        omop_df: pd.DataFrame, 
        description_filepath: str,
        synthetic_data_filepath: str
    ):
    '''
    Looks at correlation of attributes by producing heatmap

    '''

    synthetic_df = pd.read_csv(synthetic_data_filepath)

    attribute_description = read_json_file(
        description_filepath)['attribute_description']

    inspector = ModelInspector(
        omop_df, synthetic_df, attribute_description)

    figure_filepath = os.path.join(
        filepaths.plots_dir, 
        'mutual_information_heatmap_' + mode + '.png'
    )

    inspector.mutual_information_heatmap(figure_filepath)


if __name__ == "__main__":
    main()
