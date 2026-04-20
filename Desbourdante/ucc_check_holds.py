import desbordante as db
import pandas as pd

def print_results_for_ucc(ucc_verifier, path_to_dataset):
    if ucc_verifier.ucc_holds():
        print('This set of attributes ensures uniqueness.\n')
        return
    print('This set of attributes doesn\'t ensures uniqueness.')

    print('Clusters violating UCC:')
    print(f'found {ucc_verifier.get_num_clusters_violating_ucc()} clusters violating UCC:')

    table = pd.read_csv(path_to_dataset)

    violating_clusters = ucc_verifier.get_clusters_violating_ucc()
    cluster_num = 1
    for violating_cluster in violating_clusters:
        print(f"Violating cluster {cluster_num}:")
        cluster_num+=1
        violating_series = []
        for i, row in table.iterrows():
            if i not in violating_cluster:
                continue
            violating_series.append(row)
        print(pd.DataFrame(violating_series))
    print()


def get_cluster(dataset, indexes):
    df = pd.read_csv(dataset)
    selected_rows = df.iloc[indexes]
    return selected_rows

polluted_dataset = pd.read_csv("student_conference_polluted.csv")
print(polluted_dataset.head())

# polluted data
ucc_verifier = db.aucc_verification.algorithms.Default()
ucc_verifier.load_data(table=("student_conference_polluted.csv", ',', True))
ucc_verifier.execute(ucc_indices=[1, 6]) # Передаем индексы соответствующие аттрибутам (Email, Year)

print()
print_results_for_ucc(ucc_verifier, "student_conference_polluted.csv")

# fixed data
ucc_verifier.load_data(table=("student_conference_fixed.csv", ',', True))
ucc_verifier.execute(ucc_indices=[1, 6])

print()
print_results_for_ucc(ucc_verifier, "student_conference_fixed.csv")
