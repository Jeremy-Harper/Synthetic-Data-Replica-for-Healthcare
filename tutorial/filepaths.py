import os
import sys
from pathlib import Path

this_filepath = Path(os.path.realpath(__file__))
project_root = str(this_filepath.parents[1])

data_dir = os.path.join(project_root, 'data/')

# add the DataSynthesizer repo to the pythonpath
data_synthesizer_dir = os.path.join(project_root, 'DataSynthesizer/')
sys.path.append(data_synthesizer_dir)

plots_dir = os.path.join(project_root, 'plots/')


OMOP_data = os.path.join(data_dir, 'COVID19Patients.csv')
omop_data_deidentify = os.path.join(data_dir, 'COVID19Patients_deidentify.csv')

omop_data_synthetic_random = os.path.join(
    data_dir, 'COVID19Patients_data_synthetic_random.csv')
omop_data_synthetic_independent = os.path.join(
    data_dir, 'COVID19Patients_data_synthetic_independent.csv')
omop_data_synthetic_correlated = os.path.join(
    data_dir, 'COVID19Patients_data_synthetic_correlated.csv')

omop_description_random = os.path.join(
    data_dir, 'COVID19Patients_description_random.json')
omop_description_independent = os.path.join(
    data_dir, 'COVID19Patients_description_independent.json')
omop_description_correlated = os.path.join(
    data_dir, 'COVID19Patients_description_correlated.json')

