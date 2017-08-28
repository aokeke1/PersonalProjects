import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;

public class Scratchwork {
	private static List<Integer> bitPositions(long number) {
	    List<Integer> positions = new ArrayList<>();
	    int position = 63;
	    while (number != 0) {
	        if ((number & 1) != 0) {
	            positions.add(position);
	        }
	        position--;
	        number = number >>> 1;
	    }
	    return positions;
	}

	public static void printGrid(String[][] board){
	   for(int i = 0; i < 8; i++)
	   {
	      for(int j = 0; j < 8; j++)
	      {
	         System.out.printf("%5s ", board[i][j]);
	      }
	      System.out.println();
	   }
	}
	public static ArrayList<String> testMutations(ArrayList<String> testList,int depth,int maxDepth){
		testList.add("1");
		System.out.println("test List"+testList.size());
		if (depth==maxDepth){
			return testList;
		}
		
		ArrayList<String> returnedList = testMutations(testList,depth+1,maxDepth);
		System.out.println("returned List"+ returnedList.size());
		System.out.println("test List"+ testList.size());
		return returnedList;
		}
	public static String gridToString(String[][] board){
		String val = new String();
		val = "\ta\tb\tc\td\te\tf\tg\th\n";
		   for(int i = 0; i < 8; i++)
		   { val = val + Integer.toString(8-i);
		      for(int j = 0; j < 8; j++)
		      {
		    	  val = val + "\t" + board[i][j];
		      }
		      val = val + "\n";
		   }
		   return val;
		}
	public static void drawBitboard(long bitBoard){
		String[][] chessBoard = new String [8][8];
		for (int i=0;i<64;i++){
			chessBoard[7-(i/8)][i%8]="";
		}
		for (int i=0;i<64;i++){
			if(((bitBoard>>>i)&1)==1){
				chessBoard[7-(i/8)][i%8]="P";
			}
			else{
				chessBoard[7-(i/8)][i%8]=" ";
			}
		}
		for(int i=0;i<8;i++){
		   System.out.println(Arrays.toString(chessBoard[i]));
		}
	}
	public static int[] gridToString(int a,int b){
		int[] combined = {a,b};
		   return combined;
		}
	public static void main(String [] args){
		//int x = 1;
		//System.out.println(x);
		/*
		long x = (long) 0b0000000000000000000000000000000000000000000000001111111111111111L;
		long y = (long) 0b101111110011111111L;
		long z = (long) (x&y);
		long blackRook   = 0b1000000100000000000000000000000000000000000000000000000000000000L;
		
		System.out.println(Long.numberOfLeadingZeros(x));
		System.out.println(Long.toBinaryString(x));
		System.out.println(x);
		System.out.println(Long.numberOfLeadingZeros(y));
		System.out.println(Long.toBinaryString(y));
		System.out.println(y);
		System.out.println(Long.numberOfLeadingZeros(z));
		System.out.println(Long.toBinaryString(z));
		System.out.println(z);
		System.out.println(Long.toBinaryString(x<<3));
		System.out.println(bitPositions(y));
		System.out.println(blackRook);
		System.out.println(bitPositions(blackRook));
		
		String [][] chessBoard = new String[8][8];
		chessBoard[5][2] = (String) "BR";
		System.out.println(chessBoard[7][7]);
		System.out.println(chessBoard[1][7]);
		printGrid(chessBoard);
		
		System.out.println(7/8);
		System.out.println(7%8);
		*/
		/*
		Chessboard myBoard = new Chessboard();
		myBoard.showBoard();
		*/
		/*
		String [][] chessBoard = new String[8][8];
		chessBoard[5][2] = (String) "BR";
		
		String val = new String();
		val = gridToString(chessBoard);
		System.out.println(val);
		*/
		/*
		Chessboard myBoard = new Chessboard();
		System.out.println(myBoard);
		
		Long whiteMoves = myBoard.generatePawnMoves (1);
		Long blackMoves = myBoard.generatePawnMoves (0);
		System.out.println(Long.toBinaryString(whiteMoves));
		System.out.println(Long.toBinaryString(blackMoves));
		*/
		/*
		long y = (long) 0b101111110011111111L;
		System.out.println(Long.toBinaryString(y));
		List<Integer> x = bitPositions(y);
		List<Integer> z = new ArrayList<Integer> (x.size());
		for (int i=0;i<x.size();i++){
			z.add(63-x.get(i));
		}
		System.out.println(x);
		System.out.println(z);
		*/
		/*
		Chessboard myBoard = new Chessboard();
		Long bitboard = 0b0000000100000001000000010000000100000001000000010000000100000001L;
		Long expectedResult = 0b0000000000000000000000000000000000000000000000000000000011111111L;
		Long result = myBoard.rotateCW90Deg (bitboard);
		System.out.println(Long.toBinaryString(expectedResult));
		System.out.println(Long.toBinaryString(result));
		System.out.println(result==expectedResult);
		System.out.println(result.equals(expectedResult));
		*/
		/*
		System.out.println(5/3);
		System.out.println(5.0/3);
		System.out.println(5);
		*/
		/*
		Chessboard myBoard = new Chessboard();
		System.out.println(myBoard.diagOccupancyMoves);
		*/
		/*
		long row8   = 0b1111111100000000000000000000000000000000000000000000000000000000L;
		long row7   = 0b0000000011111111000000000000000000000000000000000000000000000000L;
		long row6   = 0b0000000000000000111111110000000000000000000000000000000000000000L;
		long row5   = 0b0000000000000000000000001111111100000000000000000000000000000000L;
		long row4   = 0b0000000000000000000000000000000011111111000000000000000000000000L;
		long row3   = 0b0000000000000000000000000000000000000000111111110000000000000000L;
		long row2   = 0b0000000000000000000000000000000000000000000000001111111100000000L;
		long row1   = 0b0000000000000000000000000000000000000000000000000000000011111111L;
		System.out.println(row8);
		System.out.println(row7);
		System.out.println(row6);
		System.out.println(row5);
		System.out.println(row4);
		System.out.println(row3);
		System.out.println(row2);
		System.out.println(row1);
		
		long col8   = 0b1000000010000000100000001000000010000000100000001000000010000000L;
		long col7   = 0b0100000001000000010000000100000001000000010000000100000001000000L;
		long col6   = 0b0010000000100000001000000010000000100000001000000010000000100000L;
		long col5   = 0b0001000000010000000100000001000000010000000100000001000000010000L;
		long col4   = 0b0000100000001000000010000000100000001000000010000000100000001000L;
		long col3   = 0b0000010000000100000001000000010000000100000001000000010000000100L;
		long col2   = 0b0000001000000010000000100000001000000010000000100000001000000010L;
		long col1   = 0b0000000100000001000000010000000100000001000000010000000100000001L;
		System.out.println(col8);
		System.out.println(col7);
		System.out.println(col6);
		System.out.println(col5);
		System.out.println(col4);
		System.out.println(col3);
		System.out.println(col2);
		System.out.println(col1);
		System.out.println("pause");
		drawBitboard(col1);
		System.out.println("pause");
		drawBitboard(col8);
		System.out.println("pause");
		drawBitboard(row1);
		System.out.println("pause");
		*/
		/*
		long center   = 0b0000000000000000000000000001100000011000000000000000000000000000L;
		long extendedcenter   = 0b0000000000000000001111000011110000111100001111000000000000000000L;
		long kingside   = 0b1111000000000000000000000000000000000000000000000000000011110000L;
		long queenside  = 0b0000111100000000000000000000000000000000000000000000000000001111L;
		System.out.println(center);
		System.out.println(extendedcenter);
		System.out.println(kingside);
		System.out.println(queenside);
		System.out.println("pause");
		drawBitboard(center);
		System.out.println("pause");
		drawBitboard(extendedcenter);
		System.out.println("pause");
		drawBitboard(kingside);
		System.out.println("pause");
		drawBitboard(queenside);
		*/
		/*
		Chessboard myBoard = new Chessboard(1);
		System.out.println(myBoard);
		myBoard = new Chessboard(0);
		System.out.println(myBoard);
		*/
		/*
		Chessboard myBoard = new Chessboard(-1);
		System.out.println(myBoard);
		String moves = Moves.possibleMovesW(myBoard.WP, myBoard.WN, myBoard.WB, myBoard.WR, myBoard.WQ, myBoard.WK, myBoard.BP, myBoard.BN, myBoard.BB, myBoard.BR, myBoard.BQ, myBoard.BK, myBoard.EP, myBoard.CWK, myBoard.CWQ, myBoard.CBK, myBoard.CBQ);
		System.out.println(moves);
		moves = Moves.possibleMovesB(myBoard.WP, myBoard.WN, myBoard.WB, myBoard.WR, myBoard.WQ, myBoard.WK, myBoard.BP, myBoard.BN, myBoard.BB, myBoard.BR, myBoard.BQ, myBoard.BK, myBoard.EP, myBoard.CWK, myBoard.CWQ, myBoard.CBK, myBoard.CBQ);
		System.out.println(moves);
		*/
		/*
		Long WR             = 0b0000100000000000000000000000000000100000000000000000000000000001L;
		Long WP             = 0b0000001000000010010000000000000000001000000010000000000000000000L;
		long[] givenBoardInformation = {0b0L,0b0L,0b0L,0b0L,WR,WP,0b0L,0b0L,0b0L,0b0L,0b0L,0b0L};
		Chessboard myBoard = new Chessboard(givenBoardInformation);
		Long result;
		
        int loopLength=1000;
        long startTime=System.currentTimeMillis();
        for (int i=0;i<loopLength;i++){
        	result = myBoard.generateRookMoves(1);
        }
        long endTime=System.currentTimeMillis();
        System.out.println("That took "+(endTime-startTime)+" milliseconds for the first method");
        startTime=System.currentTimeMillis();
        for (int i=0;i<loopLength;i++){
        	result = myBoard.generateRookMoves2(1);
        }
        endTime=System.currentTimeMillis();
        System.out.println("That took "+(endTime-startTime)+" milliseconds for the second method");
		*/
		/*
		Chessboard myBoard = new Chessboard(-1);
		System.out.println(myBoard);
		Perft checker = new Perft();
		checker.perftMaxDepth = 6;
		checker.perftMoveCounter = 0;
		boolean whiteToMove = false;
		checker.perft(myBoard.WP, myBoard.WN, myBoard.WB, myBoard.WR, myBoard.WQ, myBoard.WK, myBoard.BP, myBoard.BN, myBoard.BB, myBoard.BR, myBoard.BQ, myBoard.BK, myBoard.EP, myBoard.CWK, myBoard.CWQ, myBoard.CBK, myBoard.CBQ, whiteToMove, 0);
		System.out.println(checker.perftMoveCounter);
		*/
		/*
		String fenString1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
		String fenString2 = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2";
		Chessboard myBoard = new Chessboard(fenString1);
		Chessboard myBoard2 = new Chessboard(fenString2);
		System.out.println(myBoard);
		System.out.println(myBoard2);
		*/
		/*
		String fenString = "3r4/1p1k3n/r1p3p1/2p4p/6b1/5R2/8/6KR b - - 5 44";
		BoardGeneration.importFEN(fenString);
		//System.out.println(myBoard);
		Perft.perftMaxDepth = 5;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,true);
		*/
		 /*
		
		String moves = "242374736564161516147664765576576352637263546345050005010502050305040515050605073707371737273747375737673777363536453626364636273647";
		for (int i=0;i<moves.length();i+=4) {
			System.out.println(moves.substring(i,i+4));
			System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4)));
			System.out.println("Break");
		}*/
		/*
		System.out.println(Math.random());
		Zobrist.testDistribution();
		*/
		/*
		String moveList = "1.c4 g6 2.d4 Bg7 3.Nc3 d6 4.e4 Nf6 5.f3 O-O 6.Be3 e5 7.Nge2 c6 8.d5 cxd5 "
				+ "9.cxd5 a6 10.Qd2 Nbd7 11.Nc1 Nh5 12.Nd3 f5 13.O-O-O Nb6 14.Nb4 Bd7 15.Kb1 Rc8 "
				+ "16.Qf2 Na4 17.Nxa4 Bxa4 18.b3 Bd7 19.Bb6 Qe8 20.Qd2 fxe4 21.fxe4 Bb5 22.Nd3 Nf6 "
				+ "23.Qb4 Qe7 24.Nb2 Bh6 25.Bxb5 axb5 26.Rhe1 Qd7 27.h3 Ne8 28.Nd3 Nc7 29.Be3 Bxe3 "
				+ "30.Rxe3 Na6 31.Qd2 Nc5  1/2-1/2";
		Orion.HISTORY2 = new ArrayList<Long[]>();
		BoardGeneration.importFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
		Orion.HISTORY2.add(BoardGeneration.getBoardInformation());
		BoardGeneration.parseMoveList(moveList);
		*/
		/*
		int count =0;
		Path fileLoc = Paths.get("C:\\Users\\arinz\\Desktop\\ChessNotes\\smallPracticeSet.pgn");
		//Path fileLoc = Paths.get("C:/Users/arinz/OneDrive/Documents/GitHub/ChessBot/Chess/New/Modern/Modern.pgn");
		String data ="";
		Charset charset = Charset.forName("US-ASCII");
		try (BufferedReader reader = Files.newBufferedReader(fileLoc, charset)) {
		    String line = null;
		    while (((line = reader.readLine()) != null)&&(count<=20)) {
		        System.out.println(line);
		        
		        data += " "+line;
		    }
		} catch (IOException x) {
		    System.err.format("IOException: %s%n", x);
		}
		System.out.println(data);
		System.out.println(data.substring(data.indexOf("1."), data.indexOf("[", data.indexOf("1."))));
		*/
		double [][] x = new double[5][5];
		x[1][4] = 3;
		for (int i=0;i<5;i++){
			System.out.println(Arrays.toString(x[i]));
		}
		String myString = "3.5130668e+00   2.8033160e+00  -1.0957304e+00   7.4403603e-01   7.0291312e-02  -8.2969735e-01   1.3404502e+00  -7.1290354e-01   1.4903272e-01   7.5476133e-01  -1.7062872e+00   1.3661470e+00   4.2599127e+00  -2.6305152e-02   4.1120264e-01  -5.1173689e-02  -8.4546847e-01   1.1441765e-02";
		String[] y = new String[18];
		double[] z = new double[18];
		y = myString.split("\\s+");
		for (int i=0;i<18;i++){
			z[i] = Double.parseDouble(y[i]);
		}
		System.out.println(Arrays.toString(y));
		System.out.println(Arrays.toString(z));
		
		System.out.println("Weights 1");
		//System.out.println(NeuralNetwork.weights1);
		System.out.println("Weights 2");
		//System.out.println(NeuralNetwork.weights2);
		NeuralNetwork.loadWeights();

	}
	

}
