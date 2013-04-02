#include<iostream>
#include<cmath>
#include<set>
#include<string>
using namespace std;
#define SIZE 7
bool arr[7][7];
bool visited[7][7];

bool valid(int i,int j,int n){
	return i>=0 && j>=0 && i<n && j<n && !((i<=1 && (j<=1 || j>=n-2))|| (i>=n-2 && (j<=1 || j>=n-2)));
}
int iterations=0;

set<string> expanded;

string array_to_string(bool arr[][SIZE]){
	string s="";
	for(int i=0;i<SIZE;i++){
		for(int j=0;j<SIZE;j++){
			s+=(char)(arr[i][j]+'0');
		}
	}
	return s;
}

bool dfs(){
	string s = array_to_string(arr)	;
	if(expanded.find(s)!=expanded.end()){
		return false;	
	}
	else expanded.insert(s);
	iterations++;
	bool found=false;
	int count=0;
	for(int x=0;x<SIZE;x++){
		for(int y=0;y<SIZE;y++){
			int xhop1=0,xhop2=0,yhop1=0,yhop2=0;
			if(arr[x][y]){
				count++;
				for(int i=-1;i<=1;i++){
					for(int j=-1;j<=1;j++){
						bool valid_move=0;
						if(i!=0 && j==0 && valid(x+i,y,SIZE) && valid(x+i+i,y,SIZE) && arr[x+i][y] && !arr[x+i+i][y]){
							xhop1=x+i;xhop2=x+i+i;yhop1=yhop2=y;valid_move=1;
						}
						else if(i==0 && j!=0 && valid(x,y+j,SIZE) && valid(x,y+j+j,SIZE) && arr[x][y+j] && !arr[x][y+j+j]){
							xhop1=xhop2=x;yhop1=y+j;yhop2=y+j+j;valid_move=1;
						}
						if(valid_move){
							arr[xhop2][yhop2]=1;
							arr[xhop1][yhop1]=arr[x][y]=0;
							if(dfs()){
								return true;
							}
							arr[xhop2][yhop2]=0;
							arr[xhop1][yhop1]=arr[x][y]=1;
						}
					}
				}
			}
		}
	}
	return(count==1 && arr[3][3]);
}

int main(){
	int t;
	cin>>t;
	for(int ii=0;ii<t;ii++){
	set<string> new_set;
	expanded=new_set;
	iterations=0;
	string input;
	cin>>input;
	int count=0;
	bool base[SIZE][SIZE];
	for(int i=0;i<7;i++){
		for(int j=0;j<7;j++){
			if(valid(i,j,SIZE)){
				base[i][j]=(input[count++]=='0'?0:1); 
				arr[i][j]=base[i][j];
			}
		}
	}
	if(dfs()){
		cout<<"CASE "<<ii<<endl;
		cout<<"SUCCESS "<<endl;
	}
	else{
		cout<<"CASE "<<ii<<endl;
		cout<<"FAIL"<<endl;
	}
	cout<<"ITERATIONS "<<iterations<<endl;
	cout<<expanded.size()<<endl;
		
	}
}
