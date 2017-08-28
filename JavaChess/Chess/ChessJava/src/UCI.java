import java.util.*;
public class UCI {
    static String ENGINENAME="ArinzeBot v1";
    public static void uciCommunication() {
    	@SuppressWarnings("resource")
		Scanner input = new Scanner(System.in);
        while (true)
        {
            String inputString=input.nextLine();
            if ("uci".equals(inputString))
            {
                inputUCI();
            }
            else if (inputString.startsWith("setoption"))
            {
                inputSetOption(inputString);
            }
            else if ("isready".equals(inputString))
            {
                inputIsReady();
            }
            else if ("ucinewgame".equals(inputString))
            {
                inputUCINewGame();
            }
            else if (inputString.startsWith("position"))
            {
                inputPosition(inputString);
            }
            else if (inputString.startsWith("go"))
            {
                inputGo(inputString);
            }
            else if (inputString.equals("quit"))
            {
                inputQuit();
            }
            else if ("print".equals(inputString))
            {
                inputPrint();
            }
        }
    }
    public static void inputUCI() {
        System.out.println("id name "+ENGINENAME);
        System.out.println("id author Arinze");
        //options go here
        System.out.println("uciok");
    }
    public static void inputSetOption(String inputString) {
        //set options
    }
    public static void inputIsReady() {
    	//Set up the Zobrist Keys
    	Zobrist.zobristFillArray();
    	//Initialize NeuralNetworkWeights
    	//NeuralNetwork.loadWeights();
    	//Initialize Machine Learning Coefficients
    	//Changed the signs on some of the values in the machine learning file to make a second version
    	//Rating.machineLearningCoefficients=MachineLearning.loadMachineLearningCoeffs("C:/Users/arinz/Desktop/ChessNotes/MachineLearningCoefficients2.csv", 60);
    	System.out.println("readyok");
    }
    public static void inputUCINewGame() {
        //add code here
    }
    public static void inputPosition(String input) {
        input=input.substring(9).concat(" ");
        if (input.contains("startpos ")) {
            input=input.substring(9);
            BoardGeneration.importFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
        }
        else if (input.contains("fen")) {
            input=input.substring(4);
            BoardGeneration.importFEN(input);
        }
        if (input.contains("moves")) {
            input=input.substring(input.indexOf("moves")+6);
            while (input.length()>2)//Used two instead of 0 in case we end with a single space at the end
            {
            	if(Orion.WhiteToMove){
            		Orion.moveCounter++;
            	}
                algebraToMove(input);
                input=input.substring(input.indexOf(' ')+1);
                BoardGeneration.addToHistory();
                
            }
            //Remove the last board because it is added during the move search process
            Long boardHash = Zobrist.getZobristHash(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove);
            Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)-1);
        }
    }
    public static void algebraToMove(String input) {
        int from=(input.charAt(0)-'a')+(8*(input.charAt(1)-'1'));
        int to=(input.charAt(2)-'a')+(8*(input.charAt(3)-'1'));
    	
        String moves;
        if (Orion.WhiteToMove) {
            moves=Moves.possibleMovesW(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ);
        } else {
            moves=Moves.possibleMovesB(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ);
        }
        
        int start=0,end=0;
        for (int i=0;i<moves.length();i+=4) {
            if (Character.isDigit(moves.charAt(i+3))) {//'regular' move
                start=(Character.getNumericValue(moves.charAt(i)))+(Character.getNumericValue(moves.charAt(i+1))*8);
                end=(Character.getNumericValue(moves.charAt(i+2)))+(Character.getNumericValue(moves.charAt(i+3))*8);;
            } else if (moves.charAt(i+3)=='P') {//pawn promotion
                if (Character.isUpperCase(moves.charAt(i+2))) {
                    start=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+0)-'0']&Moves.RankMasks8[6]);
                    end=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+1)-'0']&Moves.RankMasks8[7]);
                } else {
                    start=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+0)-'0']&Moves.RankMasks8[1]);
                    end=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+1)-'0']&Moves.RankMasks8[0]);
                }
            } else if (moves.charAt(i+3)=='E') {//en passant
                if (moves.charAt(i+2)=='W') {
                    start=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+0)-'0']&Moves.RankMasks8[4]);
                    end=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+1)-'0']&Moves.RankMasks8[5]);
                } else {
                    start=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+0)-'0']&Moves.RankMasks8[3]);
                    end=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+1)-'0']&Moves.RankMasks8[2]);
                }
            }
            else{
            	System.out.println("An unrecognizable move was generated");
            }
            if ((start==from) && (end==to)) {
            	//if it is not a promotion, or if the type of promotion is the same as the current move
                if ((input.charAt(4)==' ') || (Character.toUpperCase(input.charAt(4))==Character.toUpperCase(moves.charAt(i+2)))) {
                    //Always check if we are breaking the castling rights
                    //start=(Character.getNumericValue(moves.charAt(i))*8)+(Character.getNumericValue(moves.charAt(i+1)));
                    if (((1L<<start)&Orion.WK)!=0) {Orion.CWK=false; Orion.CWQ=false;}
                    if (((1L<<start)&Orion.BK)!=0) {Orion.CBK=false; Orion.CBQ=false;}
                    if ((((1L<<start)|(1L<<end))&Orion.WR&(1L<<7))!=0) {Orion.CWK=false;}
                    if ((((1L<<start)|(1L<<end))&Orion.WR&(1L))!=0) {Orion.CWQ=false;}
                    if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<63))!=0) {Orion.CBK=false;}
                    if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<56))!=0) {Orion.CBQ=false;}
                    
                    int numPiecesBefore = Rating.bitCount(Orion.WP|Orion.WN|Orion.WB|Orion.WR|Orion.WQ|Orion.WK|Orion.BP|Orion.BN|Orion.BB|Orion.BR|Orion.BQ|Orion.BK);
                    long WPBefore = Orion.WP;
                    long BPBefore = Orion.BP;
                    //Do the moves
                    Orion.EP=Moves.makeMoveEP(Orion.WP|Orion.BP,moves.substring(i,i+4));
                    long oldWR=Orion.WR,oldBR = Orion.BR;
                    Orion.WR=Moves.makeMoveCastle(Orion.WR, Orion.WK|Orion.BK, moves.substring(i,i+4), 'R');
                    Orion.BR=Moves.makeMoveCastle(Orion.BR, Orion.WK|Orion.BK, moves.substring(i,i+4), 'r');
                    if(oldWR!=Orion.WR){
                	    Orion.WhiteHasCastled = true;
                    }
                    if(oldBR!=Orion.BR){
                	    Orion.BlackHasCastled = true;
                    }
                    Orion.WP=Moves.makeMove(Orion.WP, moves.substring(i,i+4), 'P');
                    Orion.WN=Moves.makeMove(Orion.WN, moves.substring(i,i+4), 'N');
                    Orion.WB=Moves.makeMove(Orion.WB, moves.substring(i,i+4), 'B');
                    Orion.WR=Moves.makeMove(Orion.WR, moves.substring(i,i+4), 'R');
                    Orion.WQ=Moves.makeMove(Orion.WQ, moves.substring(i,i+4), 'Q');
                    Orion.WK=Moves.makeMove(Orion.WK, moves.substring(i,i+4), 'K');
                    Orion.BP=Moves.makeMove(Orion.BP, moves.substring(i,i+4), 'p');
                    Orion.BN=Moves.makeMove(Orion.BN, moves.substring(i,i+4), 'n');
                    Orion.BB=Moves.makeMove(Orion.BB, moves.substring(i,i+4), 'b');
                    Orion.BR=Moves.makeMove(Orion.BR, moves.substring(i,i+4), 'r');
                    Orion.BQ=Moves.makeMove(Orion.BQ, moves.substring(i,i+4), 'q');
                    Orion.BK=Moves.makeMove(Orion.BK, moves.substring(i,i+4), 'k');
                    Orion.WhiteToMove=!Orion.WhiteToMove;
                    
                    int numPiecesAfter = Rating.bitCount(Orion.WP|Orion.WN|Orion.WB|Orion.WR|Orion.WQ|Orion.WK|Orion.BP|Orion.BN|Orion.BB|Orion.BR|Orion.BQ|Orion.BK);
                    if ((numPiecesBefore==numPiecesAfter)&&(Orion.WP==WPBefore)&&(Orion.BP==BPBefore)){
                    	Orion.fiftyMoveCounter++;
                    }
                    else{
                    	Orion.fiftyMoveCounter = 0;
                    }
                    break;
                }
            }
        }
    }
	public static void inputGo(String input) {
		input=input.concat(" ");
		Orion.searchDepth = 4;
        if (input.contains("depth")) {
            input=input.substring(input.indexOf("depth")+6);
            Orion.searchDepth = Integer.parseInt(input.substring(0,input.indexOf(' ')));
        }
        //Search for the best move
        Orion.nodesSearchedCounter=0;
        /*
        String move;
        if (Orion.WhiteToMove) {
            move=Moves.possibleMovesW(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ);
        } else {
            move=Moves.possibleMovesB(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ);
        }
        //filter invalid moves
        move = Moves.filterMoves(move,Orion.WhiteToMove,Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP);
        //Select a random move for now.
        String bestMove = Strategies.Strategy8(move);
        System.out.println("bestmove "+moveToAlgebra(bestMove));
        */
        Strategies.Strategy9();
    }
    public static String moveToAlgebra(String move) {
        String returnMove="";
        if (Character.isDigit(move.charAt(3))) {//'regular' move
            returnMove+=(char)('a'+(move.charAt(0)-'0'));
            returnMove+=(char)('1'+(move.charAt(1)-'0'));
            returnMove+=(char)('a'+(move.charAt(2)-'0'));
            returnMove+=(char)('1'+(move.charAt(3)-'0'));
        } else if (move.charAt(3)=='P') {//pawn promotion
            returnMove+=(char)('a'+(move.charAt(0)-'0'));
            if (Character.isUpperCase(move.charAt(2))) {
                returnMove+='7';
                returnMove+=(char)('a'+(move.charAt(1)-'0')); 
                returnMove+='8';
            } else {
                returnMove+='2';
                returnMove+=(char)('a'+(move.charAt(1)-'0')); 
                returnMove+='1';
            }
            returnMove+=Character.toLowerCase(move.charAt(2));
        } else if (move.charAt(3)=='E') {//en passant
            returnMove+=(char)('a'+(move.charAt(0)-'0'));
            if (move.charAt(2)=='W') {
                returnMove+='5';
                returnMove+=(char)('a'+(move.charAt(1)-'0')); 
                returnMove+='6';

            } else {
                returnMove+='4';
                returnMove+=(char)('a'+(move.charAt(1)-'0')); 
                returnMove+='3';

            }
        }
        else{
        	System.out.println("An unrecognizable move was generated");
        }
        return returnMove;
    }
    public static void inputQuit() {
        System.exit(0);
    }
    public static void inputPrint() {
        BoardGeneration.drawArray(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK);
        String fenBoard = BoardGeneration.makeFullFEN(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove,Orion.fiftyMoveCounter,Orion.moveCounter);
        System.out.println(fenBoard);
        System.out.print("Zobrist Hash: ");
        System.out.println(Zobrist.getZobristHash(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove));
    }
}