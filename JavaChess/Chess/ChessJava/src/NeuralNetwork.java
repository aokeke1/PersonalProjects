import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import Jama.Matrix;

public class NeuralNetwork {
	public static Matrix weights1 = new Matrix(new double[21][18]);
	public static Matrix weights2 = new Matrix(new double[18][1]);
	
	public static int Scoring18(double[][] chessBoard){
		Matrix chessArray = new Matrix(chessBoard);
		Matrix Hsum = chessArray.times(weights1);
		Matrix Hresults = sigma(Hsum);
		Matrix Osum = Hresults.times(weights2);
		Matrix Oresult = sigma(Osum);
		double score = Oresult.get(0, 0);
		//System.out.println(score);
		return (int)(score*10000);
	}
	public static void loadWeights(){
		double[][] w1 = new double[21][18];
		double[][] w2 = new double[18][1];

		//Weights1
		Path fileLoc = Paths.get("C:/Users/arinz/Desktop/ChessNotes/NeuralNetworksForChess/weights1.out");
		Charset charset = Charset.forName("US-ASCII");
		try (BufferedReader reader = Files.newBufferedReader(fileLoc, charset)) {
		    String line = null;
		    int j=0;
		    while (((line = reader.readLine()) != null)) {
		    	String[] y = line.split("\\s+");
				for (int i=0;i<18;i++){
					w1[j][i] = Double.parseDouble(y[i]);
				}
				j++;
		    }
		} catch (IOException x) {
		    System.err.format("IOException: %s%n", x);
		}
		
		//Weights2
		Path fileLoc2 = Paths.get("C:/Users/arinz/Desktop/ChessNotes/NeuralNetworksForChess/weights2.out");
		try (BufferedReader reader = Files.newBufferedReader(fileLoc2, charset)) {
		    String line = null;
		    int j=0;
		    while (((line = reader.readLine()) != null)) {
		    	//System.out.println(j+" : "+line);
				w2[j][0] = Double.parseDouble(line);
				j++;
		    }
		} catch (IOException x) {
		    System.err.format("IOException: %s%n", x);
		}
		
		weights1 = new Matrix(w1);
		weights2 = new Matrix(w2);
	}
	public static Matrix sigma(Matrix a){
		double[][] a2 = a.getArray();
		double[][] b = new double[a2.length][a2[0].length];
		for(int i=0;i<a2[0].length;i++){
			for(int j=0;j<a2.length;j++){
				b[j][i] = 1.0/(1.0+Math.exp(a2[j][i]));
			}
		}
		return new Matrix(b);
	}
}
