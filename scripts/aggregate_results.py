import os
import pandas as pd

# Define paths and filenames
results_folder = "/app/results/"
compare_candidates_file = "compare_candidates.csv"
mutation_scores_file = "mutation_scores.csv"

# Initialize lists to gather data for each table
mutation_data = []
unique_candidates_data = []

# Loop through each project folder (assuming each folder is named after the project)
folders = os.listdir(results_folder)
# delete unique_candidates_comparison.csv and mutation_scores_per_operator.csv
if "unique_candidates_comparison.csv" in folders:
    folders.remove("unique_candidates_comparison.csv")
if "mutation_scores_per_operator.csv" in folders:
    folders.remove("mutation_scores_per_operator.csv")
for folder in folders:
    skipped_mutation_score = False
    project_name = folder

    # Load mutation scores data
    mutation_scores_path = os.path.join(results_folder, folder, mutation_scores_file)
    try:
        with open(mutation_scores_path, "r") as f:
            headers = f.readline().strip().split(",")
            mutation_scores = pd.read_csv(mutation_scores_path)
    except FileNotFoundError:
        print(f"Skipping project {project_name} as mutation_scores.csv is missing")
        skipped_mutation_score = True

    # Extract mutation count and score per operator
    if not skipped_mutation_score:
        mutation_counts = {}
        mutation_scores_percentage = {}
        total_mutants = 0
        total_score_sum = 0
        for _, row in mutation_scores.iterrows():
            operator = row['operator']
            mutant_count = row['mutant_count']
            mutation_score = row['mutation_score']

            mutation_counts[operator] = mutant_count
            mutation_scores_percentage[operator] = mutation_score
            total_mutants += mutant_count
            total_score_sum += mutation_score

        # Calculate total score percentage
        total_score = total_score_sum / len(mutation_scores) if len(mutation_scores) > 0 else 0

        # Append data for Table 1
        mutation_data.append({
            'Project': project_name,
            'RemFuncArg #Mut': mutation_counts.get('RemFuncArg', 0),
            'RemFuncArg MS%': mutation_scores_percentage.get('RemFuncArg', 0),
            'RemConvFunc #Mut': mutation_counts.get('RemConvFunc', 0),
            'RemConvFunc MS%': mutation_scores_percentage.get('RemConvFunc', 0),
            'RemElCont #Mut': mutation_counts.get('RemElCont', 0),
            'RemElCont MS%': mutation_scores_percentage.get('RemElCont', 0),
            'RemExpCond #Mut': mutation_counts.get('RemExpCond', 0),
            'RemExpCond MS%': mutation_scores_percentage.get('RemExpCond', 0),
            'ChUsedAttr #Mut': mutation_counts.get('ChUsedAttr', 0),
            'ChUsedAttr MS%': mutation_scores_percentage.get('ChUsedAttr', 0),
            'RemAttrAcc #Mut': mutation_counts.get('RemAttrAccess', 0),
            'RemAttrAcc MS%': mutation_scores_percentage.get('RemAttrAccess', 0),
            'RemMetCall #Mut': mutation_counts.get('RemMetCall', 0),
            'RemMetCall MS%': mutation_scores_percentage.get('RemMetCall', 0),
            'Total #Mut': total_mutants,
            'Total MS%': total_score
        })

    # Load compare candidates data
    compare_candidates_path = os.path.join(results_folder, folder, compare_candidates_file)
    try:
        with open(compare_candidates_path, "r") as f:
            headers = f.readline().strip().split(",")
            compare_candidates = pd.read_csv(compare_candidates_path)
    except FileNotFoundError:
        print(f"Skipping project {project_name} as compare_candidates.csv is missing")
        continue

    # Extract flame and mutmut unique counts and percentages
    flame_unique = compare_candidates['flame_unique'][0]
    flame_unique_per = compare_candidates['flame_unique_per'][0]
    mutmut_unique = compare_candidates['mutmut_unique'][0]
    mutmut_unique_per = compare_candidates['mutmut_unique_per'][0]

    # Append data for Table 2
    unique_candidates_data.append({
        'Project': project_name,
        'Flame Uniques #Unique Cand': flame_unique,
        'Flame Uniques Unique%': flame_unique_per,
        'Mutmut Uniques #Unique Cand': mutmut_unique,
        'Mutmut Uniques Unique%': mutmut_unique_per
    })

# Convert lists to DataFrames for display and further processing
mutation_df = pd.DataFrame(mutation_data)
unique_candidates_df = pd.DataFrame(unique_candidates_data)

# Calculate and append averages for each DataFrame
mutation_averages = mutation_df.mean(numeric_only=True).to_dict()
mutation_averages['Project'] = 'Average'
mutation_df = pd.concat([mutation_df, pd.DataFrame([mutation_averages])], ignore_index=True)

unique_candidates_averages = unique_candidates_df.mean(numeric_only=True).to_dict()
unique_candidates_averages['Project'] = 'Average'
unique_candidates_df = pd.concat([unique_candidates_df, pd.DataFrame([unique_candidates_averages])], ignore_index=True)

print("Table 1: Mutation Scores per Operator")
print(mutation_df.to_markdown())


mutation_df.to_csv(results_folder + "mutation_scores_per_operator.csv", index=False)

print("\nTable 2: Unique Candidates Comparison")

print(unique_candidates_df.to_markdown())


unique_candidates_df.to_csv(results_folder + "unique_candidates_comparison.csv", index=False)