#include <iostream>
#include <vector>
#include <numeric>
#include <chrono>

using namespace std;
using namespace std::chrono;

// recursive utility function for generating a Cartesian product
void r_cartesian_product(const vector<vector<int>>& arrays,
                         vector<vector<int>>& result,
                         vector<int>& currentArray,
                         int count) {
    if (count == arrays.size()) {
        result.emplace_back(currentArray);
        return;
    }

    for (const int& element : arrays[count]) {
        currentArray[count] = element;
        r_cartesian_product(arrays, result, currentArray, count + 1);
    }
}

// function for generating a Cartesian product
vector<vector<int>> cartesian_product(const vector<int>& array, unsigned int repeat) {
    vector<vector<int>> array2, result;
    vector<int> currentArray(repeat);
    for (int i = 0; i < repeat; ++i) array2.emplace_back(array);

    r_cartesian_product(array2, result, currentArray, 0);
    return result;
}

// function which generates all Prufer sequences for graphs with n vertices
vector<vector<int>> all_prufer_sequences(int n) {
    vector<vector<int>> sequences;
    vector<int> sequence(n);
    iota(sequence.begin(), sequence.end(), 1);
    return cartesian_product(sequence, n - 2);
}

// function for calculating total weight of a graph given by a Prufer sequence
int calculate_total_weight(const vector<int>& prufer, const vector<vector<int>>& weights) {
    int n = prufer.size() + 2;
    vector<int> degree(n, 1), degree_util(n, 1);
    int total = 0;

    for (int i : prufer) {
        ++degree[i - 1];
        ++degree_util[i - 1];
    }

    for (int i : prufer) {
        for (int j = 0; j < n; ++j) {
            if (degree[j] == 1) {
                total += weights[i - 1][j];
                if (degree_util[i - 1] > 3) total += 250 * (degree_util[i - 1] - 3);
                if (degree_util[j] > 3) total += 250 * (degree_util[j] - 3);
                --degree[i - 1];
                --degree[j];
                break;
            }
        }
    }

    int u = 0, v = 0;

    for (int i = 0; i < n; ++i) {
        if (degree[i] == 1) {
            if (u == 0) u = i;
            else {
                v = i;
                break;
            }
        }
    }
    total += weights[u][v];
    return total;
}

// function for converting Prufer sequence to the edge list for printing it out
vector<pair<int, int>> prufer_to_edge_list(const vector<int>& prufer) {
    int n = prufer.size() + 2;
    vector<int> degree(n, 1);
    vector<pair<int, int>> edges;

    for (int i : prufer) ++degree[i - 1];

    for (int i : prufer) {
        for (int j = 0; j < n; ++j) {
            if (degree[j] == 1) {
                edges.emplace_back(make_pair(i - 1, j));
                --degree[i - 1];
                --degree[j];
                break;
            }
        }
    }

    int u = 0, v = 0;

    for (int i = 0; i < n; ++i) {
        if (degree[i] == 1) {
            if (u == 0) u = i;
            else {
                v = i;
                break;
            }
        }
    }
    edges.emplace_back(make_pair(u, v));
    return edges;
}

int main() {
    vector<vector<int>> connection_table = {
            {0,   374, 350, 223, 108, 178, 252, 285, 240, 356},
            {364, 0,   27,  166, 433, 199, 135, 95,  136, 17},
            {350, 27,  0,   41,  52,  821, 180, 201, 131, 247},
            {223, 166, 41,  0,   430, 47,  52,  84,  40,  155},
            {108, 433, 52,  430, 0,   453, 478, 344, 389, 423},
            {178, 199, 821, 47,  453, 0,   91,  37,  64,  181},
            {252, 135, 180, 52,  478, 91,  0,   25,  83,  117},
            {285, 95,  201, 84,  344, 37,  25,  0,   51,  42},
            {240, 136, 131, 40,  389, 64,  83,  51,  0,   118},
            {356, 17,  247, 155, 423, 181, 117, 42,  118, 0}
    };

    auto start = high_resolution_clock::now();
    vector<vector<int>> sequences = all_prufer_sequences((int)connection_table.size());
    vector<int> best_network;
    int minimal_price = 10e8;

    for (const auto& seq : sequences) {
        int price = calculate_total_weight(seq, connection_table);
        if (price < minimal_price) {
            minimal_price = price;
            best_network = seq;
        }
    }
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    cout << "Time taken to solve: " << duration.count() << " microseconds\n\n";
    cout << "Minimal Price: " << minimal_price << "\nNetwork edges:\n";
    for (auto edge : prufer_to_edge_list(best_network)) cout << (char)('A' + edge.first) << " - " << (char)('A' + edge.second) << "\n";
    return 0;
}