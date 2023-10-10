import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from counts import CountMin, CountMed, CountSketch
import time

f = open("results.txt", "a")

def main():
    global f
    start = time.time()
    data = pd.read_csv('user-ct-test-collection-01.txt', sep='\t')
    queries = data.Query.dropna().str.split(' ').head(500)
    stop = time.time()
    print("read in table = ", stop - start, " secs")

    _, axs = plt.subplots(3, 3)
    R = [2**10, 2**14, 2**18]
    intersect_cts = [[], [], []] # [[min cts], [med cts], [sketch cts]]
    for r in range(3):
        print("-------------------------------------------------------------------------------------------------------")
        print("experiment R = ", R[r])
        start = time.time()
        dfs, series = experiment(R[r], queries)
        for i in range(3):
            # print("plot i = ", i)
            plot_ct(dfs[i], axs[r,i])
            intersect_cts[i].append(series[i])
        stop = time.time()
        print("experiment time = ", (stop - start) / 60, " mins")

    f.close()
    plt.figure()
    plot_heap(R, intersect_cts)
    print("\n\n\nDone! :)")
    plt.show(block = True)
    

def experiment(R, queries):
    global f
    print("create sketches")
    ct_dict = defaultdict(int)
    ct_min = CountMin(R)
    ct_med = CountMed(R)
    ct_sketch = CountSketch(R)

    start = time.time()
    for query in queries:
        for q in query:
            ct_dict[q] += 1
            ct_min.increment(q)
            ct_med.increment(q)
            ct_sketch.increment(q)
    stop = time.time()
    print("insertion = ", (stop - start) / 60, " mins")

    f.write("-------------------------------------------------------------------------------------------------------------\n")
    f.write("R = " + str(R) + "\n")
    f.write("-------------------------------------------------------------------------------------------------------------\n")
    f.write("Top 500 Tokens - CountMin\n\n\n")
    f.write(ct_min.print_heap())
    f.write("-------------------------------------------------------------------------------------------------------------\n")
    f.write("Top 500 Tokens - CountMed\n\n\n")
    f.write(ct_med.print_heap())
    f.write("-------------------------------------------------------------------------------------------------------------\n")
    f.write("Top 500 Tokens - CountSketch\n\n\n")
    f.write(ct_sketch.print_heap())

    counts = pd.Series(ct_dict).sort_values(ascending=False)

    freq_100 = pd.DataFrame(
        counts.head(100),
        columns=['expected']
    ).reset_index().rename(columns={'index': 'token'})
    infreq_100 = pd.DataFrame(
        counts.tail(100),
        columns=['expected']
    ).reset_index().rename(columns={'index': 'token'})
    rand_100 = pd.DataFrame(
        counts.sample(100),
        columns=['expected']
    ).reset_index().rename(columns={'index': 'token'})

    start = time.time()
    for df in [freq_100, infreq_100, rand_100]:
        df['estimate_min'] = df['token'].apply(lambda token: ct_min.estimate(token))
        df['estimate_med'] = df['token'].apply(lambda token: ct_med.estimate(token))
        df['estimate_sketch'] = df['token'].apply(
            lambda token: ct_sketch.estimate(token))
        df['error_min'] = abs(df['estimate_min'] -
                              df['expected']) / df['expected']
        df['error_med'] = abs(df['estimate_med'] -
                              df['expected']) / df['expected']
        df['error_sketch'] = abs(
            df['estimate_sketch'] - df['expected']) / df['expected']
    stop = time.time()
    print("calculate estimate = ", (stop - start) / 60, " mins")

    min_top_tokens = ct_min.token_list_to_set()
    min_intersect_ct = len(set(freq_100["token"]).intersection(min_top_tokens))
    med_top_tokens = ct_med.token_list_to_set()
    med_intersect_ct = len(set(freq_100["token"]).intersection(med_top_tokens))
    sketch_top_tokens = ct_sketch.token_list_to_set()
    sketch_intersect_ct = len(set(freq_100["token"]).intersection(
        sketch_top_tokens))

    return [freq_100, infreq_100, rand_100], [min_intersect_ct, med_intersect_ct, sketch_intersect_ct]


def plot_ct(df, ax):
    ax.plot(df['token'], df['error_min'], label="count-min", alpha=0.5)
    ax.plot(df['token'], df['error_med'], label="count-med", alpha=0.5)
    ax.plot(df['token'], df['error_sketch'], label="count-sketch", alpha=0.5)
    ax.tick_params(axis='x', labelrotation=90)
    ax.legend()

def plot_heap(R, intersect_cts):
    plt.plot(R, intersect_cts[0], label="count-min", alpha=0.5)
    plt.plot(R, intersect_cts[1], label="count-med", alpha=0.5)
    plt.plot(R, intersect_cts[2], label="count-sketch", alpha=0.5)
    plt.xlabel("R-values")
    plt.ylabel("# of Intersections")
    plt.title("Accuracy of Sketches")
    plt.legend()
    plt.xticks(R)

if __name__ == "__main__":
    main()