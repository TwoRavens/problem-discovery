import pandas as pd
import json


datasets = [
    {
        "filename": "ck_cces2014.dta",
        "models": [
            {
                "Name": "Table 1 Column 1",
                "DependentVariable": "epabin",
                "EvaluationMetric": "rms",
                "Goal": "prediction",
                "Predictors": "epaconst epapolicy gop5 dem5 male education age white globalwarmbin",
                "StatisticalModel": "logistic regression"
            },
            {
                "Name": "Table 1 Column 2",
                "DependentVariable": "epabin",
                "EvaluationMetric": "rms",
                "Goal": "prediction",
                "Predictors": "epabin epaconst epapolicy epaconst*globalwarmbin epapolicy*globalwarmbin gop5 dem5 male education age white globalwarmbin",
                "StatisticalModel": "logistic regression"
            }
        ]
    },
    {
        "filename": "ck_yougov1.dta",
        "models": [
            {
                "Name": "Table 2 Column 1",
                "DependentVariable": "isisbin",
                "EvaluationMetric": "rms",
                "Goal": "prediction",
                "Predictors": "isiscongopp gop5 dem5 male education age white",
                "StatisticalModel": "logistic regression"
            },
            {
                "Name": "Table 2 Column 2",
                "DependentVariable": "loansbin",
                "EvaluationMetric": "rms",
                "Goal": "prediction",
                "Predictors": "loanscongopp gop5 dem5 male education age white",
                "StatisticalModel": "logistic regression"
            }
        ]
    },
    {
        "filename": "ck_yougov2.dta",
        "models": [
            {
                "Name": "Table 3 Column 1",
                "DependentVariable": "isissupport",
                "EvaluationMetric": "rms",
                "Goal": "prediction",
                "Predictors": "isiscongshort isislawprof isismedia isiscongboth dem5 gop5 education age white",
                "StatisticalModel": "logistic regression"
            }
        ]
    },
    {
        "filename": "ck_yougov3.dta",
        "models": [
            {
                "Name": "Table 3 Column 1",
                "DependentVariable": "epasuppbin",
                "EvaluationMetric": "rms",
                "Goal": "prediction",
                "Predictors": "epagop epadem gop5 dem5 male education age white",
                "StatisticalModel": "logistic regression"
            }
        ]
    }
]


def validate(data):
    colnames = list(map(lambda col: col['ColName'], data['Columns']))

    for model in data['Models']:

        if type(model['Predictors']) == str:
            predictors = model['Predictors'].split()
            model['Predictors'] = list(map(lambda entry: {"VarTransformation": entry}, predictors))

            for predictor in predictors:
                if predictor not in colnames:
                    print('WARN: ' + predictor + ' not in columns.')

    return data


def process_dataset(meta):
    dataframe = pd.read_stata("./datasets/" + meta['filename'])

    column_json = []
    for colname in list(dataframe):
        column_json.append({"ColName": colname})

    return validate({
        "Columns": column_json,
        "FileType": meta['filename'].split('.')[-1],
        "FileName": '.'.join(meta['filename'].split('.')[:-1]),
        "Dimensions": {
            "ColumnCount": dataframe.shape[1],
            "RowCount": dataframe.shape[0]
        },
        "isSubset": False,
        "Models": meta['models']
    })


print(json.dumps(list(map(process_dataset, datasets)), sort_keys=True, indent=2, separators=(',', ': ')))
