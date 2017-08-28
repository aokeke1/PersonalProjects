import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class MachineLearning {
	@SuppressWarnings({ "unchecked", "rawtypes" })
	public static void main(String[] args){
		/*
		//String fileName = "C:/Users/arinz/Desktop/ChessNotes/smallPracticeSet.pgn";
		//String[] outputFileNames = {"C:/Users/arinz/Desktop/ChessNotes/evaluationTable.csv","C:/Users/arinz/Desktop/ChessNotes/movesPerGame.csv","C:/Users/arinz/Desktop/ChessNotes/results.csv"};
		//First 1002 games
		String fileName = "C:/Users/arinz/OneDrive/Documents/GitHub/ChessBot/Chess/New/Modern/ModernPart1.pgn";
		//String[] outputFileNames = {"C:/Users/arinz/Desktop/ChessNotes/evaluationTable.txt","C:/Users/arinz/Desktop/ChessNotes/movesPerGame.txt","C:/Users/arinz/Desktop/ChessNotes/results.txt"};
		String[] outputFileNames = {"C:/Users/arinz/Desktop/ChessNotes/evaluationTable2.csv","C:/Users/arinz/Desktop/ChessNotes/movesPerGame2.csv","C:/Users/arinz/Desktop/ChessNotes/results2.csv"};
		ArrayList<ArrayList> finalValues = splitFileIntoMoveData(fileName);
		ArrayList<String> allGameMoveLists = finalValues.get(0);
		ArrayList<Integer> results = finalValues.get(1);
		System.out.println(allGameMoveLists.size()+" matches found.");
		
		System.out.println("Winner of match 1: "+results.get(0));
		System.out.println("Moves of match 1: "+allGameMoveLists.get(0));
		ArrayList allBoardEvaluations = new ArrayList();
		int[] numberOfMovesPerGame = new int[allGameMoveLists.size()];
		
		for(int i=0;i<allGameMoveLists.size();i++){
			System.out.println("Evaluating game "+(i+1)+" out of "+allGameMoveLists.size());
			BoardGeneration.loadGamePGN(allGameMoveLists.get(i));
			numberOfMovesPerGame[i] = Orion.HISTORY2.size();
			for (int j=0;j<Orion.HISTORY2.size();j++){
				allBoardEvaluations.add(evaluate1(Orion.HISTORY2.get(j)));
			}
		}
		System.out.println("Exporting to Text Files For Use in MATLAB.");
		exportToMATLABReadable(outputFileNames,allBoardEvaluations,numberOfMovesPerGame,results);
		System.out.println("Done.");
		*/
		
	}
	@SuppressWarnings("rawtypes")
	public static ArrayList<ArrayList> splitFileIntoMoveData(String filePathString){
		//Store data for each game
		ArrayList<String> allGameMoveLists = new ArrayList<String>();
		ArrayList<Integer> results = new ArrayList<Integer>();

		Path fileLoc = Paths.get(filePathString);
		String fullData ="";
		Charset charset = Charset.forName("US-ASCII");
		try (BufferedReader reader = Files.newBufferedReader(fileLoc, charset)) {
		    String line = null;
		    while (((line = reader.readLine()) != null)) {
		        fullData += " "+line;
		    }
		} catch (IOException x) {
		    System.err.format("IOException: %s%n", x);
		}
		String currGameData; 
		int start,end;
		fullData = fullData.substring(ordinalIndexOf(fullData,"]",10)+1);
		while (fullData.indexOf("[", fullData.indexOf("1."))!=-1){
			start = fullData.indexOf("1.");
			end = fullData.indexOf("[", start); //look for the next open bracket after the first move
			currGameData = fullData.substring(start,end);
			allGameMoveLists.add(currGameData);
			if(currGameData.contains("1-0")){
				results.add(1);
			}else if(currGameData.contains("0-1")){
				results.add(-1);
			}else{
				results.add(0);
			}
			
			fullData = fullData.substring(end);
			//Jump past any dates or round numbers that may contain "1."
			fullData = fullData.substring(ordinalIndexOf(fullData,"]",10)+1);
		}
		//Catch the last game that doesnt have an open bracket after it
		start = fullData.indexOf("1.");
		currGameData = fullData.substring(start);
		allGameMoveLists.add(currGameData);
		if(currGameData.contains("1-0")){
			results.add(1);
		}else if(currGameData.contains("0-1")){
			results.add(-1);
		}else{
			results.add(0);
		}
		ArrayList<ArrayList> finalValues = new ArrayList<ArrayList>();
		finalValues.add(allGameMoveLists);
		finalValues.add(results);
		
		return finalValues;
	}
	public static int ordinalIndexOf(String str, String substr, int n) {
	    int pos = str.indexOf(substr);
	    while (--n > 0 && pos != -1)
	        pos = str.indexOf(substr, pos + 1);
	    return pos;
	}
	
	@SuppressWarnings("rawtypes")
	public static int[] evaluate1(ArrayList boardInformation){
		/* (order is the same as they are passed to the function) (White then black)
		 * a. count number of each type of piece for each color (12),
		 * b1. number of moves each piece can do (12),
		 * b2. number of castling moves white and black have (2),
		 * c1. number of each white piece type being protected(6)
		 * c2. number of each white piece type being threatened(6)
		 * c3. number of each black piece type being protected(6)
		 * c4. number of each black piece type being threatened(6)
		 * d. 840*sumOfDistanceFromPawnToEnd/numRemainingPawns (2)
		 * e. numberOfStackedPawns (2)
		 * f. CWK, CWQ, CBK, CBQ, WhiteHasCastled,BlackHasCastled (6)
		 * 	  total = 60 parameters considered
		 * 
		 * 		boardInformation = [WK,WQ,WB,WN,WR,WP,BK,BQ,BB,BN,BR,BP,EP,CWK,CWQ,CBK,CBQ,WhiteHasCastled,BlackHasCastled,WhiteToMove];
		 */
		int[] calculatedValues = new int[60];
		//Assign values
		long WK=(long) boardInformation.get(0),WQ=(long) boardInformation.get(1),WB=(long) boardInformation.get(2),WN=(long) boardInformation.get(3),
				WR=(long) boardInformation.get(4),WP=(long) boardInformation.get(5),BK=(long) boardInformation.get(6),BQ=(long) boardInformation.get(7),
				BB=(long) boardInformation.get(8),BN=(long) boardInformation.get(9),BR=(long) boardInformation.get(10),BP=(long) boardInformation.get(11),
				EP=(long) boardInformation.get(12);
		boolean CWK=(boolean) boardInformation.get(13),CWQ=(boolean) boardInformation.get(14),CBK=(boolean) boardInformation.get(15),CBQ=(boolean) boardInformation.get(16),
		WhiteHasCastled=(boolean) boardInformation.get(17),BlackHasCastled=(boolean) boardInformation.get(18);
		// Part A
		for (int i=0;i<12;i++){
			calculatedValues[i] = Rating.bitCount((long) boardInformation.get(i));
		}
		
		//Part B1&B2
		Moves.NOT_MY_PIECES = ~(WP|WN|WB|WR|WQ|WK|BK); //Added BK to avoid illegal capture
		Moves.MY_PIECES = WP|WN|WB|WR|WQ;//omitted WK to avoid illegal capture
		Moves.OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
		Moves.EMPTY = ~Moves.OCCUPIED;
		calculatedValues[12] = Moves.possibleK(Moves.OCCUPIED,WK).length();
		calculatedValues[13] = Moves.possibleQ(Moves.OCCUPIED,WQ).length();
		calculatedValues[14] = Moves.possibleB(Moves.OCCUPIED,WB).length();
		calculatedValues[15] = Moves.possibleN(Moves.OCCUPIED,WN).length();
		calculatedValues[16] = Moves.possibleR(Moves.OCCUPIED,WR).length();
		calculatedValues[17] = Moves.possibleWP(WP,BP,EP).length();
		calculatedValues[24] = Moves.possibleCW(WR,CWK,CWQ,WK).length();

		Moves.NOT_MY_PIECES = ~(BP|BN|BB|BR|BQ|BK|WK); //Added WK to avoid illegal capture
		Moves.MY_PIECES = BP|BN|BB|BR|BQ;//omitted WK to avoid illegal capture
		Moves.OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
		Moves.EMPTY = ~Moves.OCCUPIED;
		calculatedValues[18] = Moves.possibleK(Moves.OCCUPIED,WK).length();
		calculatedValues[19] = Moves.possibleQ(Moves.OCCUPIED,WQ).length();
		calculatedValues[20] = Moves.possibleB(Moves.OCCUPIED,WB).length();
		calculatedValues[21] = Moves.possibleN(Moves.OCCUPIED,BN).length();
		calculatedValues[22] = Moves.possibleR(Moves.OCCUPIED,WR).length();
		calculatedValues[23] = Moves.possibleBP(BP,WP,EP).length();
		calculatedValues[25] = Moves.possibleCB(BR,CBK,CBQ,BK).length();
		
    	long unsafeForWhite=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
    	long unsafeForBlack=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
		//Part C1 white pieces protected
		for (int i=0;i<6;i++){
			calculatedValues[26+i] = Rating.bitCount((long) boardInformation.get(i)&unsafeForWhite);
		}
		//Part C2 white pieces threatened
		for (int i=0;i<6;i++){
			calculatedValues[32+i] = Rating.bitCount((long) boardInformation.get(i)&unsafeForBlack);
		}
		//Part C3 black pieces protected
		for (int i=0;i<6;i++){
			calculatedValues[38+i] = Rating.bitCount((long) boardInformation.get(i+6)&unsafeForBlack);
		}
		//Part C4 black pieces threatened
		for (int i=0;i<6;i++){
			calculatedValues[44+i] = Rating.bitCount((long) boardInformation.get(i+6)&unsafeForWhite);
		}

    	//Part D
		if(calculatedValues[5]==0){
			//No White Pawns
			calculatedValues[50] = 840*8;
		}
		else{
        	List<Integer> pawnLocations = BoardGeneration.bitPositions(WP);
        	int sumDistances = 0;
        	for (int i:pawnLocations){
            	//Distance between pawn and rank 8
        		sumDistances += (7-i/8);
        	}
			calculatedValues[50] = 840*sumDistances/calculatedValues[5];
		}
		if(calculatedValues[11]==0){
			//No Black Pawns
			calculatedValues[51] = 840*8;
		}
		else{
        	List<Integer> pawnLocations = BoardGeneration.bitPositions(BP);
        	int sumDistances = 0;
        	for (int i:pawnLocations){
            	//Distance between pawn and rank 1
        		sumDistances += (i/8);
        	}
			calculatedValues[51] = 840*sumDistances/calculatedValues[11];
		}
    	//Part E Number of White Stacked Pawns, Number of Black Stacked Pawns
		int stackedWhite = 0;
		int stackedBlack = 0;
		
		for(int i=0;i<8;i++){
			stackedWhite = stackedWhite + Math.max(0, Rating.bitCount(WP&Moves.FileMasks8[i]) - 1);
			stackedBlack = stackedBlack + Math.max(0, Rating.bitCount(BP&Moves.FileMasks8[i]) - 1);
		}
		
		calculatedValues[52] = stackedWhite;
		calculatedValues[53] = stackedBlack;
		
    	//Part F
		calculatedValues[54] = (CWK) ? 1 : 0;
		calculatedValues[55] = (CWQ) ? 1 : 0;
		calculatedValues[56] = (CBK) ? 1 : 0;
		calculatedValues[57] = (CBQ) ? 1 : 0;
		calculatedValues[58] = (WhiteHasCastled) ? 1 : 0;
		calculatedValues[59] = (BlackHasCastled) ? 1 : 0;
		return calculatedValues;
	}
	public static void exportToMATLABReadable(String[] outputFileNames,ArrayList allBoardEvaluations,int[] numberOfMovesPerGame,ArrayList<Integer> results){
		//mxn matrix where m=number of boards (sum over number of boards for each game) and n = number of properties evaluated
		System.out.println("Making evaluation matrix.");
		String evaluationString = "";
		int printFreq = allBoardEvaluations.size()/100;

		
		try {
			File file = new File(outputFileNames[0]);
			FileWriter fileWriter = new FileWriter(file);
			
			for (int i=0;i<allBoardEvaluations.size();i++){
				if(i%printFreq==0){
					System.out.println("Making string of board "+(i+1)+" out of "+allBoardEvaluations.size());
				}
				
				for (int j=0;j<((int[])allBoardEvaluations.get(0)).length;j++){
					evaluationString+=((int[])allBoardEvaluations.get(i))[j];
					evaluationString += "\t";
				}
				evaluationString += "\n";
				if (evaluationString.length()>=10000){
					//System.out.println("Writing to file.");
					fileWriter.write(evaluationString);
					evaluationString = "";
					fileWriter.flush();
				}
			}
			//System.out.println(evaluationString);
			
			System.out.println("Writing to file.");
			fileWriter.write(evaluationString);
			evaluationString = "";
			fileWriter.flush();
			fileWriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		System.out.println("Making number of moves per game vector.");
		//Column vector
		String numberOfMovesPerGameString = "";
		for (int i=0;i<numberOfMovesPerGame.length;i++){
			numberOfMovesPerGameString += numberOfMovesPerGame[i];
			numberOfMovesPerGameString += "\n";
		}
		//System.out.println(numberOfMovesPerGameString);
		
		try {
			File file = new File(outputFileNames[1]);
			FileWriter fileWriter = new FileWriter(file);
			fileWriter.write(numberOfMovesPerGameString);
			fileWriter.flush();
			fileWriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		System.out.println("Making results matrix.");
		//Column vector
		String resultsString = "";
		for (int i=0;i<results.size();i++){
			resultsString += results.get(i);
			resultsString += "\n";
		}
		//System.out.println(resultsString);

		try {
			File file = new File(outputFileNames[2]);
			FileWriter fileWriter = new FileWriter(file);
			fileWriter.write(resultsString);
			fileWriter.flush();
			fileWriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static double[] loadMachineLearningCoeffs(String fileName,int numCoeffs){
		double[] coeffs = new double[numCoeffs];
		Path fileLoc = Paths.get(fileName);
		int count = 0;
		Charset charset = Charset.forName("US-ASCII");
		try (BufferedReader reader = Files.newBufferedReader(fileLoc, charset)) {
		    String line = null;
		    while (((line = reader.readLine()) != null)) {
		        coeffs[count] = Double.parseDouble(line);
		        count++;
		    }
		} catch (IOException x) {
		    System.err.format("IOException: %s%n", x);
		}
		return coeffs;
	}
}
