package tictactoe;

public class Tuple {

    public int row;
    public int col;
    public int diagonal;
    public int diagonal2;
    public Tuple(){

    }

    public Tuple(int row, int col,int diagonal){
        this.row = row;
        this.col = col;
        this.diagonal = diagonal;
    }
}
