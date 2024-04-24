# cse-5388-002-surveil-doc
This is a repository for SurveilDoc.

Install the virtual environment with the following command:
```
pip install virtualenv
```

Active the environment with the following command:
```
source env/bin/activate
```

Install the required packages with the following command:
```
pip install -r requirements.txt
```

To deactivate the environment, use the following command:
```
deactivate
```

To run the application, use the following command:
```
```

Folder Structure:
```
.
├── README.md
├── sensitive_data_values
│   ├── datasets
│   │   ├── Secret Regular Expression.xlsx
|   |   ├── common_passwords.csv
│   ├── processed_datasets
│   │   ├── secret_data_values.csv
│   │   ├── common_passwords.csv
│   ├── scripts
├── requirements.txt


Dataset:
``` 
1. Secret Regular Expression.xlsx - This is a dataser that contains regular expressions for sensitive data values collected by SecretBench.
Source: https://github.com/setu1421/SecretBench/blob/main/Regular%20Expressions/Secret%20Regular%20Expression.xlsx
2. common_passwords.csv - This is a dataset that contains 10000 most common passwords.
Source: https://www.kaggle.com/datasets/shivamb/10000-most-common-passwords
```