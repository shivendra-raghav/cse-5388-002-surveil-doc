# cse-5388-002-surveil-doc
This is a repository for SurveilDoc.

Install the required packages with the following command:
```
pip install -r requirements.txt
```

To run the application, use the following steps:
```
1. data_generation - This folder contains the code for synthetic secret and dataset generation. Here are the steps to generate the dataset:
    a. secrets_pre_processing.ipynb - This files reads the SecretBench "Secret Regular Expression.xlsx" files and cleans and creates a JSON with synthetic data. It then reads the common_passwords.csv and adds it to the JSON. The JSON is then saved as "secrets.json" file in the "sensitive_data_values" folder.
    b. pii_generator.ipynb - This files creates synthetic PIIs for the project. The data is saved as profiles.csv file in the "sensitive_data_values" folder.
    c. claude_api.py - This file is used to call the Claude API to save the response in the "synthetic_dataset/sensitive_with_placeholders" folder.
    d. post_process.py - This file is used to call the Claude API to clean the dataset created by the initial call and make it more realistic and do cleanup and the response is stored in the "synthetic_dataset/processed_sensitive_with_placeholders" folder.
    e. document_classification_generator.ipynb - This files reads converts all the text files for processed synthetic dataset into a single CSV file with classification columns and metadata. It saves the data to "synthetic_dataset/document_classified_data.csv" file.
    f. sentence_classification_generator.ipynb - This files reads converts all the text files for processed synthetic dataset into a single CSV file with classification columns and metadata. It also extracts the NER details from the sentences. It saves the data to "synthetic_dataset/sentence_classified_data_ner.csv" file.
    g. prompts - This folder contains all the sensitive prompts used to generate the dataset.
    h. non_sensitive_prompts - This folder contains 300 non sensitive prompts, for remaining 200 files in the dataset, the enron email dataset is used.
```

Dataset:
``` 
1. Secret Regular Expression.xlsx - This is a dataser that contains regular expressions for sensitive data values collected by SecretBench.
Source: https://github.com/setu1421/SecretBench/blob/main/Regular%20Expressions/Secret%20Regular%20Expression.xlsx
2. common_passwords.csv - This is a dataset that contains 10000 most common passwords.
Source: https://www.kaggle.com/datasets/shivamb/10000-most-common-passwords
3. Enron Email Dataset - This is a dataset that contains emails from Enron employees.
Source: https://www.cs.cmu.edu/~enron/ 
```