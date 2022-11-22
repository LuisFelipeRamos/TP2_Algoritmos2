#include <iostream>
#include <bits/stdc++.h>

struct Node{
    int bound;
    int cost;
    std::vector<int> path;
    bool oneBeforeTwo;

    Node(int bound, int cost, std::vector<int> path, bool oneBeforeTwo){
        this-> bound = bound;
        this->cost = cost;
        this-> path = path;
        this->oneBeforeTwo = oneBeforeTwo;
    };
};

/* se estimativa igual, heap ordena com custo */
bool operator < (Node n1, Node n2){
    return n1.bound != n2.bound ? n1.bound < n2.bound : n1.cost < n2.cost;
}

int bound(std::vector<std::vector<int>> graph){
    return 16;
}

std::vector<int> branch_and_bound_tsp(std::vector<std::vector<int>> graph){

    int numberOfNodes = graph.size();
    Node root = Node(bound(graph), 0, std::vector<int>({0}), false);
    std::priority_queue<Node> pq;
    pq.push(root);
    double best = INT_MAX;
    std::vector<int> solution = {};
    
    while (!pq.empty()){
        continue;
    }

};

int main(int argc, char* argv){
    return 0;
};
