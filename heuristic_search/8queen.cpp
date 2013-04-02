#include<iostream>
#define SIZE 8
using namespace std;

bool arr[SIZE][SIZE]; //board state

bool check(int x,int y){
	for(int i=0;i<SIZE;i++){
		if(arr[x][i]) return false;
	}
	for(int i=0;i<SIZE;i++){
		if(arr[i][y]) return false;
	}
	int x1,y1;
	x1=x;y1=y;
	while(x1>=0 && y1>=0){
		if(arr[x1--][y1--]) return false;
	}
	x1=x;y1=y;
	while(x1<SIZE && y1<SIZE){
		if(arr[x1++][y1++]) return false;
	}
	return true;
}

bool foo(int col){
	int row=0;
	for(;row<SIZE;row++){
		if(!arr[row][col] && check(row,col)){
			arr[row][col]=1;
			cout<<row<<" "<<col<<endl;
			if(col+1==SIZE) return true;
			if(!foo(col+1)){
				arr[row][col]=0;
			}
			else break;
		}
	}
	if(row<SIZE){
		cout<<col<<" success "<<row<<endl;
		return true;
	}
	return false;
}

int main(){
	bool ret=foo(0);	
	cout<<ret<<endl;
	for(int i=0;i<SIZE;i++){
		for(int j=0;j<SIZE;j++){
			if(arr[i][j])
				cout<<i<<","<<j<<endl;
		}
	}
}
