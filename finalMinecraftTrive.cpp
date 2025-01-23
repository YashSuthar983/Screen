#include <bits/stdc++.h>
#define ll long long
using namespace std;

vector<vector<bool>> check;
set<vector<float>> ans;
set<pair<int,int>> sc;

void Display(set<pair<int,int>>&sc,int rows,int cols)
{
    vector<vector<int>> dis(rows,vector<int>(cols,0));
    for (auto&x : sc) {
        cout << x.first << " " << x.second << "\n";
        dis[x.first][x.second]=1;
    }
    
    for(int x=0;x<rows;x++)
    {
        for(int y=0;y<cols;y++)
        {
            if(dis[x][y]==1)
            {
                cout<<"0";
            }
            else
            {
                cout<<"-";
            }
        }
        cout<<"\n";
    }
    cout<<"\n";
}

bool outOfBound(pair<int, int> ind, int rows, int cols) {
    return (ind.first < 0 || ind.second < 0 || ind.first >= rows || ind.second >= cols);
}

void dfs(const vector<vector<int>>& grid, const vector<pair<int, int>>& dir, pair<int, int> source, pair<int, int> prev, int cn, int t, int rows, int cols) 
{
    if (cn > 7) return;
    
    if (outOfBound(source, rows, cols)) {
        check[prev.first][prev.second] = true;
        ans.insert({(float)source.first, (float)source.second, (float)(t * 0.25)});
        return;
    }
    
    // Check if Height of Current is Bigger than Previous
    if (grid[source.first][source.second] > grid[prev.first][prev.second]) return;
    
    //If visited return
    if (check[source.first][source.second]) return;

    //To Calculate if water is on Ground How far it goes if block has height less than privious it set to 0 and again repeats
    if (grid[source.first][source.second] != grid[prev.first][prev.second]) {
        cn = 0;
    } else {
        cn++;
    }

    // To store the Blocks water is on
    sc.insert({source.first, source.second});
    check[source.first][source.second] = true;
    
    // t is nunmber of blocks visited untile it stops
    t++;

    for (auto go : dir) {
        pair<int, int> next = {source.first + go.first, source.second + go.second};
        dfs(grid, dir, next, source, cn, t, rows, cols);
    }

    check[source.first][source.second] = false;
}

int main() {
    int rows, cols;
    cout << "Enter number of rows and columns: ";
    cin >> rows >> cols;

    vector<vector<int>> grid(rows, vector<int>(cols));
    check.assign(rows, vector<bool>(cols, false));

    cout << "Enter grid values: " << endl;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cin >> grid[i][j];
        }
    }

    int start_x, start_y;
    cout << "Enter starting position (row and column): ";
    cin >> start_x >> start_y;

    pair<int, int> source = {start_x, start_y};
    vector<pair<int, int>> dir = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    pair<int, int> prev = source;
    int cn = 0;
    
    dfs(grid, dir, source, prev, cn, 0, rows, cols);
    
    cout<<"Displaying Water Behaviour";
    Display(sc,rows,cols);

    cout << "Out-of-bound positions:\n";
    if(ans.size()==0)
    {
        cout<<"-1\n";
        return 0;
    }
    for (auto p : ans) {
        cout << "[{" << p[0] << ", " << p[1] << "} , " << p[2] << "]\n";
    }
    
    return 0;
}
