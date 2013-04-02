import java.util.ArrayList;
import java.util.Scanner;
import java.io.*;
import aima.core.logic.propositional.algorithms.*;

class Node{
	int x;
	int y;
	int value;
    Node(int x,int y,int value){
        this.x=x;
        this.y=y;
        this.value=value;
    }
    String str(){
        return "P"+(x+1)+"A"+(y+1);
    }
}

class Board{
	Node board[][];
	int length;
	int width;
    Board(String filename) throws IOException{
           Scanner bf = new Scanner(new File(filename));
           if(bf.hasNextLine()){
               String l = bf.nextLine();
               String arr [] = l.split(",");
               this.length = Integer.parseInt(arr[0]);
               this.width = Integer.parseInt(arr[1]);
               board= new Node[this.length][this.width];
           }
           //System.out.println("DOING");
           int xcount=0;
           while(bf.hasNextLine()){
               String line = bf.nextLine();
               String arr[]=line.split(",");
               for(int j=0;j<arr.length;j++){
                    String str = arr[j];
                    Node n;
                    if(str.equals("X")){
                        n = new Node(xcount,j,-1);
                    }
                    else if(str.equals("NH")){
                        n = new Node(xcount,j,-2);
                    }
                    else n = new Node(xcount,j,Integer.parseInt(str));
                    board[xcount][j]=n;
               }
               xcount++;
           }
    }
    String joiner(String op, ArrayList<String> arr){
        String s="";
        if(arr.size()==0) return s;
        if(arr.size()==1) return "("+arr.get(0)+")";
        s="("+arr.get(0)+op+arr.get(1)+")";
        for(int i=2;i<arr.size();i++){
            s="("+s+op+arr.get(i)+")";
        }
        return s;
    }
    ArrayList<Node> adjacent(int x,int y){
        //return all nodes adjacent to board[x][y]
        int xpos ;
        ArrayList<Node>  arr= new ArrayList<Node>();
        xpos=x-1;
        while(xpos<=x+1){
            if(xpos>=0 && xpos<length){
                int ypos=y-1;
                while(ypos<=y+1){
                    if(ypos>=0 && ypos<width){
                        if(!(xpos==x && ypos==y) ){
                            arr.add(board[xpos][ypos]);
                           }
                    }
                    ypos++;
                }
            }
            xpos++;
        }
        return arr;
    }
    void printDoubleArray(ArrayList<ArrayList<Node > > arr){
        for(int i=0;i<arr.size();i++){
            for(int j=0;j<arr.get(i).size();j++){
                System.out.print(arr.get(i).get(j).str());
                System.out.print(" ");
            }
        }
    }
    ArrayList<ArrayList<Node> > select(ArrayList<Node> arr,int count){
        ArrayList<ArrayList <Node> > n = new ArrayList< ArrayList <Node> >();
        if(count<1 || arr.size()<count || arr.size()==0 ){
            n.add(new ArrayList<Node>());
            return n;
        }
        if(count==arr.size()){
            n.add(arr);
            return n;
        }
        ArrayList<Node> ncopy = new ArrayList<Node>();
        //copy with the first element chopped off
        for(int i=1;i<arr.size();i++)
            ncopy.add(arr.get(i));
        //end of copy
        ArrayList<ArrayList <Node> > n1 = this.select(ncopy,count);
                for(int i=0;i<n1.size();i++){
            ArrayList<Node> temp= n1.get(i);
           if(temp.size()>0 && !n.contains(temp )){
            n.add(temp);
           }
        }
        n1 = this.select(ncopy,count-1);
                for(int i=0;i<n1.size();i++){
            ArrayList<Node> n2 = new ArrayList<Node>();
            n2.add(arr.get(0));
            ArrayList<Node> temp = n1.get(i);
            for(int j=0;j<temp.size();j++) n2.add(temp.get(j));
            if(!n.contains(n2)) n.add(n2);
        }
                return n;
    }

    String formPremise(int x,int y){
        Node node = this.board[x][y];
        if(node.value==-2){
            return ("NOT "+node.str());
           }
        if(node.value!=-1){
            ArrayList<Node> arr = this.adjacent(x,y);
            ArrayList<ArrayList<Node> > selection = this.select(arr,node.value);
			ArrayList<String> rules = new ArrayList<String>();
            for (int i = 0;i<selection.size();i++){
                ArrayList<String> premise = new ArrayList<String>();
                for(int j=0;j<arr.size();j++){
                    if(!selection.get(i).contains(arr.get(j))){
                        premise.add("NOT "+arr.get(j).str());
                    }
                    else{
                        premise.add(arr.get(j).str());
                    }
                }
                String rule =this.joiner(" AND ",premise);
                rules.add(rule);
            }
            return this.joiner(" OR ",rules);        
        }
        return new String("");
    }
}

class minesniffer{
    public static void main (String args[]) throws Exception{
        Board b = new Board(args[0]);
		KnowledgeBase kb = new KnowledgeBase();
		for(int i=0;i<b.length;i++){
            for(int j=0;j<b.width;j++){
                ArrayList<Node> n = b.adjacent(i,j);
				String result = b.formPremise(i,j);
                System.out.println(result);
                if(!result.equals("")){
                    if(!result.equals("NOT "+b.board[i][j].str()) ) kb.tell("NOT "+b.board[i][j].str());
                    kb.tell(result);
                }
            }
        }
		Scanner fd2 = new Scanner(new File(args[1]));
		while(fd2.hasNextLine()){
			String ask=fd2.nextLine();	
            System.out.println("ASK = "+ask);
            TTEntails pl = new TTEntails();
            System.out.println(pl.ttEntails(kb,ask));
		}
    }
}
