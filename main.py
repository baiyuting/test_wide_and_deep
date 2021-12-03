import pandas

import file_util

_CSV_COLUMNS = [
    'age', 'workclass', 'fnlwgt', 'education', 'education_num',
    'marital_status', 'occupation', 'relationship', 'race', 'gender',
    'capital_gain', 'capital_loss', 'hours_per_week', 'native_country',
    'income_bracket'
]

_CSV_COLUMN_DEFAULTS = [[0], [''], [0], [''], [0], [''], [''], [''], [''], [''],
                        [0], [0], [0], [''], ['']]

_HASH_BUCKET_SIZE = 1000

_NUM_EXAMPLES = {
    'train': 32561,
    'validation': 16281,
}


# file_util.write_lines("total.csv", [l for l in file_util.read_lines("adult.data")+file_util.read_lines("adult.test") if l.strip() != ""])
def get_column_vocab(csv, column, skip_title=True):
    lines = [l.split(",")[column] for l in file_util.read_lines(csv)[1 if skip_title else 0:]]
    vocab = []
    for v in lines:
        if v not in vocab:
            vocab.append(v)
    return vocab


# print(get_column_vocab(csv="total.csv", column=6))


wordclass_vocab = ['Self-emp-not-inc', 'Private', 'State-gov', 'Federal-gov', 'Local-gov', '?', 'Self-emp-inc', 'Without-pay', 'Never-worked']
education_vocab = ['Bachelors', 'HS-grad', '11th', 'Masters', '9th', 'Some-college', 'Assoc-acdm', 'Assoc-voc', '7th-8th', 'Doctorate', 'Prof-school', '5th-6th', '10th', '1st-4th', 'Preschool', '12th']
marital_status_vocab = ['Married-civ-spouse', 'Divorced', 'Married-spouse-absent', 'Never-married', 'Separated', 'Married-AF-spouse', 'Widowed']
occupation_vocab = ['Adm-clerical', 'Exec-managerial', 'Handlers-cleaners', 'Prof-specialty', 'Other-service', 'Sales', 'Craft-repair', 'Transport-moving', 'Farming-fishing', 'Machine-op-inspct', 'Tech-support', '?', 'Protective-serv', 'Armed-Forces', 'Priv-house-serv']
relationship_vocab = ['Husband', 'Not-in-family', 'Wife', 'Own-child', 'Unmarried', 'Other-relative']



