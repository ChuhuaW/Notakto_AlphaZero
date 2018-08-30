package tictactoe;

import java.util.Arrays;
import java.util.Comparator;
import java.util.HashSet;
import java.util.TreeSet;

public class TicTacToe {
    TreeSet<int[][]> set;
    TreeSet<int[][]> all;
    int size;
    int c = 0;
    int[][] board;
    final static int[]X = {0,1};
    final static int[]Y = {0,1};
    public TicTacToe(int n){
        this.size = n;
        this.set = new TreeSet<>(new Comparator<int[][]>() {
            @Override
            public int compare(int[][] o1, int[][] o2) {
                if(Arrays.deepEquals(o1,o2)){
                    return 0;
                }
                return 1;
            }
        });
        this.all = new TreeSet<>(new Comparator<int[][]>() {
            @Override
            public int compare(int[][] o1, int[][] o2) {
                if(Arrays.deepEquals(o1,o2)){
                    return 0;
                }
                return 1;
            }
        });

        this.board = new int[size][size];
        for(int i=0;i<this.size;i++){
            for(int j=0;j<this.size;j++){
                board[i][j] = 1;
            }
        }

    }
    public TreeSet<int[][]> findAll(){
        find(this.board,0,0);
        return this.set;
    }
    private void find(int[][]current, int x, int y){

        int[][] new1 = copy(current);
        if(!contains(all,new1)) {
            all.add(new1);
            //printGame(new1);

            int ret = check(new1);
            //System.out.println(ret);
            if (ret == 0) {
                if (!contains(this.set,new1)) {
                    //printGame(new1);
                    c++;
                    //System.out.println(c);
                    this.set.add(new1);
                }
            } else if (ret == 1) {
                for (int i = 0; i < 2; i++) {
                    for (int j = 0; j < 2; j++) {
                        if (i == 0 && j == 0) continue;
                        //System.out.println("XXXXXXXXXXX");
                        find(new1, (x + X[i] + this.size) % this.size,
                                (y + Y[j] + this.size) % this.size);
                    }
                }
            }
        }

        //System.out.println("AAAAAAAAAAAAAA");
        int[][] new2 = copy(current);
        new2[x][y] = 0;
        //printGame(new2);
        //System.out.println(all.contains(new2));
        if(!contains(all,new2)) {
            all.add(new2);
            //printGame(new2);

            int ret = check(new2);
            if (ret == 0) {
                if (!contains(this.set,new2)) {
                    //printGame(new1);
                    c++;
                    //System.out.println(c);
                    this.set.add(new2);
                }
            } else if (ret == 1) {
                for (int i = 0; i < 2; i++) {
                    for (int j = 0; j < 2; j++) {
                        if (i == 0 && j == 0) continue;
                        //System.out.println("OOOOOOOOOOOO");
                        find(new2, (x + X[i] + this.size) % this.size,
                                (y + Y[j] + this.size) % this.size);
                    }
                }
            }
        }

    }

    /**
     * return 0 if it is exactly what we want
     * return 1 if a row or column or diagonal is 7
     * return -1 if a row or column or diagonal is 6 or less
     * @param board
     * @return
     */
    private int check(int[][] board){
        Tuple[][] tuples = this.count(board);
        int ret = 0;
        for(int i=0;i<this.size;i++){
            for(int j=0;j<this.size;j++){
                Tuple tuple = tuples[i][j];
                if(tuple.row==this.size||tuple.col==this.size||
                        tuple.diagonal==this.size||tuple.diagonal2==this.size){
                    ret = 1;
                    break;
                }
                if(board[i][j]==0){


                    if(tuple.row<this.size-1&&tuple.col<this.size-1&&
                            tuple.diagonal<this.size-1&&tuple.diagonal2<this.size-1){
                        ret = -1;
                        break;
                    }



                }
            }
        }
        return ret;
    }


    public void printGame(int[][] board){
        for(int i=0;i<this.size;i++){
            for(int j=0;j<this.size;j++){
                System.out.print(board[i][j]);
            }
            System.out.println();
        }
    }
    public int[][]copy(int[][]a){
        int[][]b = new int[this.size][this.size];
        for(int i=0;i<this.size;i++){
            for(int j=0;j<this.size;j++){
                b[i][j] = a[i][j];
            }

        }
        return b;
    }
    public boolean contains(TreeSet<int[][]> set, int[][]obj){
        boolean ret;
        boolean flag=true;
        for(int[][]g:set){
            flag = true;
            for(int i=0;i<this.size;i++){
                for(int j=0;j<this.size;j++){
                    if(obj[i][j] != g[i][j]){
                        flag = false;
                    }
                }
            }
            if(flag)return flag;
        }
        return false;
    }

    public Tuple[][] count(int[][]board){
        Tuple[][] tuples = new Tuple[this.size][this.size];
        int temp3 = 0; //diagonal
        int temp4 = 0;
        for(int i=0;i<this.size;i++){
            for(int j=0;j<this.size;j++){
                tuples[i][j] = new Tuple();
            }
        }
        for(int i=0;i<this.size;i++){
            int temp1 = 0;
            int temp2 = 0;

            for(int j=0;j<this.size;j++){

                if(board[i][j]==1)temp1++; //row
                if(board[j][i]==1)temp2++; //col
                tuples[i][j].diagonal = -1;
                tuples[i][j].diagonal2 = -1;
            }
            for(int j=0;j<this.size;j++){
                tuples[i][j].row = temp1;
                tuples[j][i].col = temp2;
            }
            if(board[i][i]==1)temp3++;
            if(board[i][this.size-i-1]==1)temp4++;
        }
        for(int i=0;i<this.size;i++){
            tuples[i][i].diagonal = temp3;
            tuples[i][this.size-i-1].diagonal2 =temp4;
        }
        return tuples;
    }

    public TreeSet<int[][]> rotate(int[][]board){
        TreeSet<int[][]> result = new TreeSet<>(new Comparator<int[][]>() {
            @Override
            public int compare(int[][] o1, int[][] o2) {
                if(Arrays.deepEquals(o1,o2)){
                    return 0;
                }
                return 1;
            }
        });
        result.add(board);
        for(int k=0;k<3;k++){
            int[][] temp = new int[size][size];
            for(int i=0;i<this.size;i++){
                for(int j=0;j<this.size;j++){

                }
            }
        }
        return result;
    }
}
