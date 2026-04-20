import desbordante as db
import pandas as pd
import numpy as np
from collections import Counter

def get_cluster(dataset, indexes):
    df = pd.read_csv(dataset)
    selected_rows = df.iloc[indexes]
    return selected_rows


def print_results_for_fd(verifier_fd, path_to_dataset):
    if verifier_fd.fd_holds():
        print("This FD holds")
        return
    print(f"Number of violating clusters = {verifier_fd.get_num_error_clusters()}")
    highlights = verifier_fd.get_highlights()
    highlight_num = 1
    for highlight in highlights:
        print(f"Violating cluster {highlight_num}:")
        highlight_num += 1
        cluster = highlight.cluster
        print(get_cluster(path_to_dataset, cluster))
    print()



# FD mining
polluted_dataset = pd.read_csv("student_conference_polluted.csv")
print(polluted_dataset.head())

fd_miner = db.afd.algorithms.Default()
fd_miner.load_data(table=("student_conference_polluted.csv", ',', True))
fd_miner.execute(error=0)
for fd in fd_miner.get_fds():
    print(fd)
print()


print("got [Paper_Number Year] -> Y, where Y -- some atribute. Lets check this rules:")
fd_verifier = db.afd_verification.algorithms.Default()
fd_verifier.load_data(table=("student_conference_polluted.csv", ',', True))
for i in [0, 1, 2, 3, 5]:
    fd_verifier.execute(lhs_indices=[4, 6], rhs_indices=[i])
    print(f"[{polluted_dataset.columns[4]}, {polluted_dataset.columns[6]}] -> {polluted_dataset.columns[i]}")
    print_results_for_fd(fd_verifier, "student_conference_polluted.csv")
print('\n')


all_fds = []
for e in np.arange(0.0, 1.0, 0.01):
    fd_miner.execute(error=e)
    for fd in fd_miner.get_fds():
        all_fds.append(str(fd))


print("FDs close to hold:")
for fd, count in Counter(all_fds).most_common(10):
    print(f"{count} count: {fd}")
