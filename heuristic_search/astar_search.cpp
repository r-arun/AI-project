#include<iostream>
#include<string>
#include<algorithm>
#include<queue>
#include<map>
#include<set>
#include<climits>
#include<cstring>
#define SQUARE_SIZE 7
using namespace std;

int arr[SQUARE_SIZE][SQUARE_SIZE];

bool isvalid(int i,int j,int n){
	return i>=0 && j>=0 && i<n && j<n && !((i<=1 && (j<=1 || j>=n-2))|| (i>=n-2 && (j<=1 || j>=n-2)));
}

void pretty_print(int arr[][SQUARE_SIZE]){
	for(int i=0;i<SQUARE_SIZE;i++){
		for(int j=0;j<SQUARE_SIZE;j++){
			if(isvalid(i,j,SQUARE_SIZE))
			cout<<arr[i][j]<<" ";
			else cout<<"X ";
		}
		cout<<endl;
	}
	cout<<endl;
}

int h(int arr[][SQUARE_SIZE]){
	int hp=0,vp=0;
	bool valid=0;
	for(int i=0;i<SQUARE_SIZE;i++){
		int counter=0;
		for(int j=0;j<SQUARE_SIZE;j++){
			if(isvalid(i,j,SQUARE_SIZE)){
				if(arr[i][j]){
					valid=1;
					if(counter<0) counter=0;
					counter++;
					if(counter>2){
						counter=2;
						hp++;
					}
				}	
				else{
					counter--;
					if(counter==-1 && valid){
						valid=0;
						hp++;
					}
				}
			}
		}
		if(valid){
			hp++;
		}
	}
	for(int i=0;i<SQUARE_SIZE;i++){
		int counter=0;
		for(int j=0;j<SQUARE_SIZE;j++){
			if(isvalid(j,i,SQUARE_SIZE)){
				if(arr[j][i]){
					valid=1;
					if(counter<0) counter=0;
					counter++;
					if(counter>2){
						counter=2;
						vp++;
					}
				}	
				else{
					counter--;
					if(counter==-1 && valid){
						valid=0;
						vp++;
					}
				}
			}
		}
		if(valid){
			vp++;
		}
	}
	return min(hp,vp);
}

bool isgoal(int arr[][SQUARE_SIZE]){
	int count=0;
	for(int i=0;i<SQUARE_SIZE;i++){
		for(int j=0;j<SQUARE_SIZE;j++){
			if(arr[i][j]==1) count++;
		}
	}
	return count==1 && arr[3][3];
}

string array_to_string(int arr[][SQUARE_SIZE]){
	string s="";
	for(int i=0;i<SQUARE_SIZE;i++){
		for(int j=0;j<SQUARE_SIZE;j++){
			if(isvalid(i,j,SQUARE_SIZE))
				s+=arr[i][j]?'1':'0';
		}
	}
	return s;
}

void string_to_array(int arr[][SQUARE_SIZE],string s){
	int count=0;
	for(int i=0;i<SQUARE_SIZE;i++){
		for(int j=0;j<SQUARE_SIZE;j++){
			if(isvalid(i,j,SQUARE_SIZE))
				arr[i][j]=s[count++]=='1';
		}
	}
	return ;
}

int main(){
	//get the initial configuration
	int t;
	cin>>t;
	for (int ii=0;ii<t;ii++){
	string input;
	cin>>input;
	
	int count=0;
	for(int i=0;i<SQUARE_SIZE;i++){
		for(int j=0;j<SQUARE_SIZE;j++){
			if(isvalid(i,j,SQUARE_SIZE)){
				arr[i][j]=input[count++]=='1';
				cout<<arr[i][j];
			}
		}
	}
	
	priority_queue<pair<int,pair<int,string> > > q;
	map<string,int> explored;
	string root=array_to_string(arr);
	q.push(make_pair(INT_MAX-0,make_pair(0,root)));
	//hcost,global ccost,arrangement
	map<string,int>  expanded;
	bool found_goal=0;
	int fcost=0;
	int ccost=0;
	expanded[root]=0;
	do{
		pair<int,pair<int,string> > node =q.top();
		q.pop();
		string pattern=node.second.second;
		ccost=node.second.first;
		int fcost=INT_MAX-node.first;
		map<string,int>::iterator mindex;
		mindex=expanded.find(pattern);
		if(mindex==expanded.end()){
			cout<<"STATUS 1 Missing in expanded map"<<endl;
			continue;		
		}
		else{
			int temp=expanded[pattern];
			expanded.erase(mindex);
			if(fcost!=temp){
				cout<<"STATUS 2 Cost mismatch "<<fcost<<" "<<temp<<endl;
				continue;		
			}
		}
		if(explored.find(pattern)==explored.end() || explored[pattern]>fcost)
			explored[pattern]=fcost;
		else{
			continue;
		}
		string_to_array(arr,pattern);
		pretty_print(arr);
		if(isgoal(arr)){
			found_goal=1;
			break;
		}
		for(int x=0;x<SQUARE_SIZE;x++){
			for(int y=0;y<SQUARE_SIZE;y++){
				if(!arr[x][y] || !isvalid(x,y,SQUARE_SIZE)) continue;
				for(int i=-1;i<=1;i++){
					for(int j=-1;j<=1;j++){
						int tarr[SQUARE_SIZE][SQUARE_SIZE];
						for(int ii=0;ii<SQUARE_SIZE;ii++){
							for(int ij=0;ij<SQUARE_SIZE;ij++){
								tarr[ii][ij]=arr[ii][ij];
							}
						}
						int xinc,yinc;
						int xhop1,yhop1;
						int xhop2,yhop2;
						if(i==0 && j!=0 || j==0 && i!=0){
							yinc=j;
							xinc=i;
						}
						xhop1=x+xinc;xhop2=x+xinc+xinc;
						yhop1=y+yinc;yhop2=y+yinc+yinc;
						if(isvalid(xhop1,yhop1,SQUARE_SIZE) && isvalid(xhop2,yhop2,SQUARE_SIZE) && arr[xhop1][yhop1] && !arr[xhop2][yhop2]){
							tarr[xhop1][yhop1]=tarr[x][y]=0;
							tarr[xhop2][yhop2]=1;
							string new_pos=array_to_string(tarr);
							int hcost=h(tarr);
							int new_ccost=ccost+1;
							int tcost=new_ccost+hcost;
							bool allow_insert=0;
							int	min_cost=INT_MAX-q.top().first;
							if((explored.find(new_pos)==explored.end() || explored[new_pos]<tcost) && (expanded.find(new_pos)==expanded.end() || expanded[new_pos]<tcost))
								allow_insert=1;
							if(allow_insert){
								expanded[new_pos]=tcost;
							}
							else continue;
							pretty_print(tarr);
							if(isgoal(tarr)){
								if(tcost<=min_cost){
									pretty_print(arr);
									found_goal=1;
									break;
								}
							}
							q.push(make_pair(INT_MAX-tcost,make_pair(new_ccost,new_pos)));
						}
					}
					if(found_goal)
						break;
				}
				if(found_goal)
					break;
			}
			if(found_goal)
				break;
		}
		if(found_goal)
			break;
	}while(!q.empty());
	cout<<"CASE "<<ii<<endl;
	if(found_goal)
		cout<<"SUCCESS"<<endl;
	else
		cout<<"FAIL"<<endl;
	cout<<"EXPLORED SIZE "<<explored.size()<<endl;
	cout<<"EXPANDED SIZE "<<expanded.size()<<endl;
	}
}

