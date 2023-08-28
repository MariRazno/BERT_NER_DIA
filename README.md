# BERT_NER_DIA
This repository contains script that extracts Diagnoses names from German medical reports.

1) For using this script firstly initialize the variable with model path. 
Linux/Unix using bash: `export MY_BERT_MODEL_PATH="/your/desired_model/path"`

2) _**Input data**_ should be in the CSV format and contain at least two columns named: ['number', 'report']
   
   Input data path should be stored in the variable: `export DATA_PATH="/your/data/path.csv"`

    1. **'number'** column contains the number of the medical report (e.g. '121923351.0')
    
    2. **'report'** column contains medical report text in plain text format (e.g. '0121923274 13.04.2019Unter kontinuierlicher Kreislaufüberwachung war der Patient allseits kardiopulmonal stabil, wach und adäquat auf Ansprache reagierend. Zwischenzeitlich auftretende hypertone RR-Werte konnten mit Ebrantil gesenkt werden...')

    Input data can contain any number of reports, results will be saved in the CSv document after processing each 100 medical reports. 

3) Save folder should be defined as global variable using bash:
Linux/Unix using bash: `export SAVE_FOLDER_PATH="/your/desired_save_directory/path"`

4) Usage steps:
   1. Install python `3.11`
   2. Clone this repository
   3. Define all global variables (listed above)
   4. Run setup.py `python setup.py`
   5. Run __init__.py `python __init__.py`