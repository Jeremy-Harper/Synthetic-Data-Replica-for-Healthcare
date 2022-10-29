You can skip this stage but it might be useful to review the deidentify.py code if you are going to run this in a production environment, what we're going to do is to anonymize the data further. Not that we have too but its good practice to remember that obfuscate when you can without losing important information in case something fails further down the line.

`filepaths.py` is where all the original filepaths were listed, I've updated the main synthetic script to have the file paths passed in but not the deidentification step.

If you look in `tutorial/deidentify.py` you'll see the full code of all de-identification steps. You can run this code which will deidentify the COVID19Patients.csv file in the data folder.

```bash
python tutorial/deidentify.py
```

It takes the file you generated called COVID19Patients.csv runs all the steps, and saves the new dataset to `data/COVID19Patients_deidentify.csv`.
