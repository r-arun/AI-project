#include<iostream>
#include<cstring>
#include<string>
#include<algorithm>
#include<vector>
#include<queue>
#include<set>
using namespace std;
#define SIZE 7

bool isvalid(int i,int j,int n){
	return i>=0 && j>=0 && i<n && j<n && !((i<=1 && (j<=1 || j>=n-2))|| (i>=n-2 && (j<=1 || j>=n-2)));
}

string array_to_string(int arr[][SIZE]){
	string s;
	for(int i=0;i<SIZE;i++){
		for(int j=0;j<SIZE;j++){
			if(isvalid(i,j,SIZE))
				s+=arr[i][j]?'1':'0';
		}
	}
	return s;
}

void string_to_array(string s,int arr[][SIZE]){
	int count=0;
	for(int i=0;i<SIZE;i++){
		for(int j=0;j<SIZE;j++){
			if(isvalid(i,j,SIZE))
				arr[i][j]=(s[count++]=='1');
		}
	}
}

int count_ones(string s){
	int counter=0;
	for(int i=0;i<s.size();i++)
		if(s[i]=='1')
			counter++;
	return counter;
}
int main(){
	int arr[7][7];
	for(int i=0;i<7;i++){
		for(int j=0;j<7;j++){
			arr[i][j]=0;
		}
	}
	arr[3][3]=1;
	set<string> explored;
	queue<string> q;
	string root = array_to_string(arr);
	q.push(root);
	
	while(!q.empty()){
		string current = q.front();
		q.pop();
		if(count_ones(current)>12) break;
		if(explored.find(current)!=explored.end())
			continue;
		explored.insert(current);
		string_to_array(current,arr);
		for(int i=0;i<SIZE;i++){
			for(int j=0;j<SIZE;j++){
				if(isvalid(i,j,SIZE) && arr[i][j]==1){
					for(int x=-1;x<=1;x++){
						for(int y=-1;y<=1;y++){
							int xhop1,yhop1,xhop2,yhop2;
							if(x==0 && y!=0 || x!=0 && y==0){
								xhop1=i+x;
								yhop1=j+y;
								xhop2=i+x+x;
								yhop2=j+y+y;
								if(isvalid(xhop1,yhop1,SIZE) && isvalid(xhop2,yhop2,SIZE) && !arr[xhop1][yhop1] && !arr[xhop2][yhop2]){
									arr[xhop1][yhop1]=arr[xhop2][yhop2]=1;
									arr[i][j]=0;
									string neighbor = array_to_string(arr);
									q.push(neighbor);
									arr[xhop1][yhop1]=arr[xhop2][yhop2]=0;
									arr[i][j]=1;
								}
							}
						}
					}
				}
			}
		}
	}
	set<string>::iterator it=explored.begin();
	cout<<explored.size()<<endl;
	for(it;it!=explored.end();it++){
		string result=*it;
		int counter=0;
		
		cout<<result;
		cout<<endl;
	}
}
