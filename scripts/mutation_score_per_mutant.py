import pandas as pd

mapping = {
    "ChangeUsedAttribute": "ChUsedAttr",
    "DeleteAttributeAccess": "RemAttrAccess",
    "DeleteElementsIterable": "RemElCont",
    "DeleteExpressionsIf": "RemExpCond",
    "DeleteFunctionArgument": "RemFuncArg",
    "DeleteMethodCall": "RemMetCall",
    "DeleteConversionFunctions": "RemConvFunc",
}

def calculate_mutation_score(file_path):
    df = pd.read_csv(file_path)
    df['operator'] = df['operator'].replace(mapping)

    result = df.groupby('operator').agg(
        dead_count=('mutant_result', lambda x: (x == 'DEAD').sum()),
        mutant_count=('mutant_result', lambda x: ((x == 'ALIVE') | (x == 'DEAD')).sum())
    )

    result['mutation_score'] = (result['dead_count'] / result['mutant_count'] * 100).round(2)
    result = result.rename(columns={'dead_count': 'dead_mutant_count'}).reset_index()
    result = result[['operator', 'mutant_count', 'mutation_score']]
    print("Mutation Score per Operator:")
    print(result)
    result.to_csv('mutation_scores.csv', index=False)

calculate_mutation_score("csv_results.csv")
