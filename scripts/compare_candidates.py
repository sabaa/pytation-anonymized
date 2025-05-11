import os
import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('.mutmut-cache')

query = '''
SELECT
    Mutant.id as mutant_id,
    MutantType.mutation_type,
    SourceFile.filename,
    Line.line_number,
    Line.line
FROM
    Mutant
JOIN
    MutantType
ON
    MutantType.mutant = Mutant.id
JOIN
    Line
ON
    Line.id = Mutant.line
JOIN
    SourceFile
ON
    SourceFile.id = Line.sourcefile
'''

mutmut_df = pd.read_sql_query(query, conn)

conn.close()


with open('dynamic_patterns_list.json') as f:
    dynamic_patterns = json.load(f)

with open('static_patterns_list.json') as f:
    static_patterns = json.load(f)


flame_patterns = dynamic_patterns + static_patterns
flame_df = pd.DataFrame(flame_patterns)

flame_df = flame_df[
    ~(
        (flame_df['pattern_status'].isin(['EQUIVALENT', 'UNCOVERED']))
    )
]

def normalize_path(path):
    try:
        return os.path.normpath(path).lower()
    except Exception as e:
        print(e)
        return path


def delete_prefix(path):
    to_remove = {
        'all': str(os.getcwd()) + '/'
    }

    prefixes_to_remove = list(to_remove.values())

    # Remove the prefix if it exists
    for prefix in prefixes_to_remove:
        try:
            if path.startswith(prefix):
                path = path[len(prefix):]
                break
        except Exception as e:
            print(e)
            continue
    return path


flame_df['source_code_path'] = flame_df['pattern_location'].apply(
    lambda x: x['filename'])
flame_df['source_code_path'] = flame_df['source_code_path'].apply(delete_prefix)
# flame_df['source_code_path'] = flame_df['source_code_path'].apply(normalize_path)
flame_df['source_code_line'] = flame_df['pattern_location'].apply(
    lambda x: x['start_line'])
flame_df['pattern_location_str'] = flame_df['pattern_location'].apply(lambda x: str(x))
flame_df['pattern_data_str'] = flame_df['pattern_data'].apply(lambda x: str(x))
flame_df = flame_df.drop(columns=['pattern_location', 'pattern_data'])

mutmut_df['normalized_filename'] = mutmut_df['filename'].apply(normalize_path)
mutmut_df.head()


merged_df = pd.merge(
    mutmut_df,
    flame_df,
    left_on=['filename', 'line_number'],
    right_on=['source_code_path', 'source_code_line'],
    how='inner'
)

line_number_plus_one_df = pd.merge(
    mutmut_df,
    flame_df,
    left_on=['filename', 'line_number'],
    right_on=['source_code_path', 'source_code_line'],
    how='inner',
    suffixes=('', '_plus_one')
)
line_number_plus_one_df = line_number_plus_one_df[
    line_number_plus_one_df['line_number'] + 1 == line_number_plus_one_df[
        'source_code_line']]

combined_df = pd.concat([merged_df, line_number_plus_one_df])
combined_df.drop_duplicates(inplace=True)


def is_subset_or_equal(str1, str2):
    return str1 in str2 or str2 in str1


merged_df = pd.merge(
    mutmut_df,
    flame_df,
    left_on=['filename'],
    right_on=['source_code_path', ],
    how='inner',
    suffixes=('_dfs', '_flame')
)

merged_df = merged_df[
    merged_df['line_number'] + 1 == merged_df['source_code_line']
    ]

df_unique_mutmut = mutmut_df[~mutmut_df.index.isin(merged_df.index)]

df_unique_flame = flame_df[~flame_df.index.isin(merged_df.index)]

results = {
    'df_match': merged_df,
    'df_unique_mutmut': df_unique_mutmut,
    'df_unique_flame': df_unique_flame
}

all_rows = []
if not results['df_match'].empty:
    df_match = results['df_match'].copy()
    df_match['match_type'] = 'match'
    all_rows.append(df_match)

if not results['df_unique_mutmut'].empty:
    df_mutmut = results['df_unique_mutmut'].copy()
    df_mutmut['match_type'] = 'unique_mutmut'
    all_rows.append(df_mutmut)

if not results['df_unique_flame'].empty:
    df_flame = results['df_unique_flame'].copy()
    df_flame['match_type'] = 'unique_flame'
    all_rows.append(df_flame)

final_df = pd.concat(all_rows, ignore_index=True)


final_df.drop_duplicates(subset=['normalized_filename', 'line_number', 'source_code_path','source_code_line', 'match_type'], inplace=True)
counts = final_df.value_counts('match_type')
match_cnt = int(counts['match'])
flame_unique_cnt = int(counts['unique_flame'])
mutmut_unique_cnt = int(counts['unique_mutmut'])

flame_unique_per = round((flame_unique_cnt / (flame_unique_cnt + match_cnt)) * 100, 2)
mutmut_unique_per = round((mutmut_unique_cnt / (mutmut_unique_cnt + match_cnt)) * 100, 2)

summary_df = pd.DataFrame([{
    'flame_unique': int(counts['unique_flame']),
    'flame_unique_per': flame_unique_per,
    'mutmut_unique': int(counts['unique_mutmut']),
    'mutmut_unique_per': mutmut_unique_per,
}])

print("Comparison of candidates:")
print(summary_df)
summary_df.to_csv('compare_candidates.csv', index=False)
