package tictactoe;

import java.util.Arrays;
import java.util.Comparator;
import java.util.TreeSet;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.FileSystems;


public class Test {
    public static void main(String[] args){
        int n = 3;

        TicTacToe game = new TicTacToe(n);
        //b = game.copy(a);
        //b[1][1] = 200;
        //System.out.println(Arrays.deepEquals(a,b));
        TreeSet<int[][]>set = game.findAll();
        TreeSet<int[][]>all = game.all;
        TreeSet<int[][]>newSet = new TreeSet<>(new Comparator<int[][]>() {
            @Override
            public int compare(int[][] o1, int[][] o2) {
                if(Arrays.deepEquals(o1,o2)){
                    return 0;
                }
                return 1;
            }
        });
        //System.out.println(set.size());
        //System.out.println(all.size());
        try{
        Charset charset = Charset.forName("UTF-8");

        //BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("name.txt"), "UTF8"));
        Path path = FileSystems.getDefault().getPath("/nfs/zapdos/home/data/vision3/cw234/tictactoe/alpha-zero-general/tictactoe","states.txt");
        BufferedWriter writer = Files.newBufferedWriter(path, charset);
        for(int[][] g:set){
            game.printGame(g);
            for(int i=0;i<n;i++){
                for(int j=0;j<n;j++){
                    String piece = Integer.toString(g[i][j]);
                    writer.write(piece);

            }
            writer.newLine();
            }
            writer.newLine();
        }   
            System.out.println();
            writer.close();
        }
        
            catch(IOException e){
                e.printStackTrace();
                    }
        }

    


}
