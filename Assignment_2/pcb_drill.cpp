#pragma GCC optimize("O3")

#include <iostream>
#include <cmath>
#include <vector>
#include <chrono>

using namespace std;
using namespace std::chrono;

// function for calculating Euclidean distance between 2 points
double dist(pair<double, double> p1, pair<double, double> p2) {
    return sqrt(pow(p1.first - p2.first, 2) + pow(p1.second - p2.second, 2));
}

// exhaustive search algorithm (calculating the distance for every permutation of points)
pair<double, vector<int>> find_path(vector<pair<double, double>> points) {
    vector<int> all_permutations, min_path;
    double min_dist = 10e9;
    for (int i = 0; i < points.size(); ++i) all_permutations.push_back(i);

    do {
        double total_dist = 0;
        for (int i = 0; i < all_permutations.size() - 1; ++i) {
            double distance = dist(points[all_permutations[i]], points[all_permutations[i + 1]]);
            total_dist += distance;
        }
        if (total_dist < min_dist) {
            min_dist = total_dist;
            min_path = all_permutations;
        }
    } while (next_permutation(all_permutations.begin(), all_permutations.end()));
    return make_pair(min_dist, min_path);
}

// driver function for printing the solution
void solve(vector<pair<double, double>> points) {
    pair<double, vector<int>> result = find_path(points);
    cout << "Minimal length of the drill path for the first " << points.size() << " holes = " << result.first << " mm\n";
    vector<int> min_path = result.second;
    cout << "Order of holes: ";
    for (int i : min_path) cout << i + 1 << " ";
    cout << "\n";
}

int main() {
    // defining all points/holes
    vector<pair<double, double>> holes = {{2.7, 33.1}, {2.7, 56.8}, {9.1, 40.3}, {9.1, 52.8},
                                          {15.1, 49.6}, {15.3, 37.8}, {21.5, 45.8}, {22.9, 32.7},
                                          {33.4, 60.5}, {28.4, 31.7}, {34.7, 26.4}, {45.7, 25.1},
                                          {34.7, 45.1}, {46.0, 45.1}, {54.2, 29.1}, {57.7, 42.1},
                                          {67.9, 19.6}, {51.7, 56.0}, {57.5, 56.0}, {62.0, 58.4}};


    // solve for first 8 holes
    auto holes_8 = vector<pair<double, double>>(holes.begin(), holes.end() - 12);
    auto start = high_resolution_clock::now();
    solve(holes_8);
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    cout << "Time taken by function: " << duration.count() << " microseconds\n\n";

    // solve for first 12 points
    auto holes_12 = vector<pair<double, double>>(holes.begin(), holes.end() - 8);
    start = high_resolution_clock::now();
    solve(holes_12);
    stop = high_resolution_clock::now();
    duration = duration_cast<microseconds>(stop - start);
    cout << "Time taken by function: " << duration.count() << " microseconds\n\n";

    return 0;
}
