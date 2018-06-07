import pandas as pd
import json
import re
import os

from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr


article = '/doi/abs/10.1111/ajps.12297'
dataset_folder = article.split('.')[-1]
datasets = json.load(open('./intermediate.json', 'r'))[article]


def validate(data):
    colnames = list(map(lambda col: col['ColName'], data['Columns']))

    for model in data['Models']:
        predictors = re.split('[\s\+]+', model['Predictors'])
        model['Predictors'] = list(map(lambda entry: {"VarTransformation": entry}, predictors))

        for predictor in predictors:
            if predictor not in colnames:
                print('WARN: ' + predictor + ' not in columns.')

    return data


def process_dataset(meta):
    filetype = meta['filename'].split('.')[-1]
    column_json = []

    if filetype == 'rda':
        print("R detected")

        pandas2ri.activate()
        base = importr('base')
        base.load(os.path.join(os.getcwd(), 'datasets', str(dataset_folder), meta['filename']))
        rdf_List = base.mget(base.ls())

        # an rda may contain many dataframes
        pydf_dict = {}

        for i, f in enumerate(base.names(rdf_List)):
            pydf_dict[f] = pandas2ri.ri2py_dataframe(rdf_List[i])

        dataframe = pydf_dict[meta["dataframe"]]

    elif filetype == 'dta':
        dataframe = pd.read_stata("./datasets/" + meta['filename'])

    else:
        raise(NotImplementedError, "Unknown filetype: " + filetype)

    for colname in list(dataframe):
        column_json.append({"ColName": colname})

    return validate({
        "Columns": column_json,
        "FileType": filetype,
        "FileName": '.'.join(meta['filename'].split('.')[:-1]),
        "Dimensions": {
            "ColumnCount": dataframe.shape[1],
            "RowCount": dataframe.shape[0]
        },
        "isSubset": False,
        "Models": meta['models']
    })


print(json.dumps(list(map(process_dataset, datasets)), sort_keys=True, indent=2, separators=(',', ': ')))
