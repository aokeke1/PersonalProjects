import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public class Orion {
	// Pieces
    static long WP=0L,WN=0L,WB=0L,WR=0L,WQ=0L,WK=0L,BP=0L,BN=0L,BB=0L,BR=0L,BQ=0L,BK=0L,EP=0L;
    //Castling Rights and whose turn it is
    static boolean CWK=true,CWQ=true,CBK=true,CBQ=true,WhiteToMove=true;//true=castle is possible
    //???
    /*
    static long UniversalWP=0L,UniversalWN=0L,UniversalWB=0L,UniversalWR=0L,
            UniversalWQ=0L,UniversalWK=0L,UniversalBP=0L,UniversalBN=0L,
            UniversalBB=0L,UniversalBR=0L,UniversalBQ=0L,UniversalBK=0L,
            UniversalEP=0L;
    */
    //Other Needed Constants
    static int searchDepth=4,moveCounter=0,fiftyMoveCounter=0,nodesSearchedCounter=0;
    static int MATE_SCORE=5000,NULL_INT=Integer.MIN_VALUE;
    //static ArrayList<String> HISTORY = new ArrayList<String> ();
    static HashMap<String,Integer> ThreeMoveRep = new HashMap<String,Integer>();
    static HashMap<Long,Integer> ThreeMoveRepCheck = new HashMap<Long,Integer>();
    static ArrayList<ArrayList> HISTORY2 = new ArrayList<ArrayList> ();
    static boolean WhiteHasCastled = false;
    static boolean BlackHasCastled = false;
    public static void main(String[] args) {
        //Zobrist.zobristFillArray();
        //BoardGeneration.importFEN("");
        //UCI.inputPrint();
    	//Test take piece (best move f4e5)
        //BoardGeneration.importFEN("r1bqkb2/2pp1p1r/p3p2p/1p2n1pn/NPP1PP2/3P4/P1Q1N1PP/R1B1KB1R w KQq - 1 11");
        //UCI.inputPrint();
    	//Test Avoid Stalemate and black can checkmate (do not d2c2)
        //BoardGeneration.importFEN("8/6k1/8/8/8/8/3q1bp1/K7 b - - 2 1");
        //BoardGeneration.importFEN("k7/3Q1BP1/8/8/8/8/6K1/8 w - - 2 1 ");
        //UCI.inputPrint();
    	//Test Avoid checkmate in 2 moves and black can checkmate (do not protect knight)
        //BoardGeneration.importFEN("r3k1n1/p2pppb1/bpn3p1/4P3/5P1P/1PPq4/P2PN1P1/RN2K2R w q - 3 20");
        //BoardGeneration.importFEN("rn2k2r/p2pn1p1/1ppQ4/5p1p/4p3/BPN3P1/P2PPPB1/R3K1N1 b Qkq - 3 1");
        //UCI.inputPrint();
    	//Mate in 3?
    	//BoardGeneration.importFEN("rnbk1Q2/8/4p3/pBB1Np2/P7/2P5/5PPP/R4K1R b - - 0 28");
    	
    	//Test, don't take the pawn.
        //BoardGeneration.importFEN("r1bqkbnr/ppppppp1/2n5/7p/8/P3P1P1/1PPP1P1P/RNBQKBNR w KQkq - 0 4");
        //BoardGeneration.importFEN("rnbqkbnr/1ppp1p1p/p3p1p1/8/7P/2N5/PPPPPPP1/R1BQKBNR b KQkq - 0 1");
        //UCI.inputPrint();
    	 
    	//BoardGeneration.importFEN("4k2R/r4pp1/nppbp1p1/p2p4/P2Pn1r1/1NP1PN2/1P1B1PP1/R3K3 b Q - 5 21");
    	//UCI.inputPrint();
    	
    	//Test, black queen threatened by knight. Queen should run away. Don't capture pawn (f6d4)
    	//BoardGeneration.importFEN("1n2k2r/1Q2np1p/p3pqp1/3p4/3P1PN1/B3P1PB/3K3P/R4R2 b k - 2 26");
    	//UCI.inputPrint();
    	
    	
        //long startTime = System.currentTimeMillis();
        //System.out.println(PrincipalVariation.pvSearch(-1000,1000,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,!WhiteToMove,0));
        //System.out.println("Searched "+moveCounter+" moves");
        //long endTime = System.currentTimeMillis();
        //System.out.println("That took " + (endTime - startTime) + " milliseconds");
    	
    	//Testing stalemate good when score is bad
    	//String inputString = "position startpos moves e2e4 g8f6 b1c3 c7c6 f2f3 b7b5 a2a4 b5b4 c3a2 e7e6 a2b4 f8b4 c2c3 b4c5 b2b4 c5b6 d2d4 h7h6 c1e3 d7d6 g2g4 e8g8 d1d2 a7a5 g1h3 a5b4 c3b4 g8h8 h3f4 g7g5 f4h5 f6h5 g4h5 f7f6 f1h3 c8a6 e1c1 d8c7 a4a5 b6a7 h3e6 a6b5 d2c2 c7e7 e6c4 b5c4 c2c4 d6d5 c4b3 d5e4 f3e4 e7e4 h1e1 e4d5 b3c2 c6c5 d4c5 d5e5 c2g6 e5c3 c1b1 c3b4 b1c2 b4c4 c2d2 f8d8 g6d3 c4d3 d2c1 d3c4 c1b2 c4b4 b2c2 b4c4 c2b2 c4b4 b2c2 b4c4";
    	
    	//String inputString = "position startpos moves e2e3 g8f6 f1d3 c7c6 b1c3 b7b5 d3f1 b5b4 d1f3 b4c3 b2c3 d7d5 a2a3 d8a5 a1b1 h7h6 h2h4 h8g8 h4h5 g8h8 c3c4 b8a6 c4d5 a8b8 b1b8 a6b8 f3f4 a5b6 d5c6 b6b1 e1d1 b8c6 f4c7 b1b7 c7b7 c8b7 h1h4 a7a6 h4a4 f6h5 a4h4 h5f6 g1h3 h8g8 c1b2 f6d7 f1d3 g7g5 d3h7 e8d8 h7g8 g5h4 g8f7 c6b8 h3f4 d8c8 f7e6 c8c7 e6f5 c7d6 d1e2 a6a5 b2h8 d7c5 f4g6 b8d7 h8d4 e7e5 d4c5 d7c5 g6f8 b7g2 f8g6 h4h3 d2d4 e5d4 e3d4 c5a6 c2c4 h3h2 f5c8 h2h1q c4c5 a6c5 d4c5 d6c5 g6f4 h1f1 e2d2 f1f2 f4e2 g2f1 c8a6 c5d6 a6d3 d6e5 a3a4 e5d6 d3a6 d6e5 a6d3 e5d6 d3a6 d6e7 a6d3";
    	//String inputString = "position startpos moves e2e3 g8f6 d2d4 e7e6 c1d2 f6e4 b1c3 e4d2 d1d2 f8b4 e1c1 d8g5 f2f4 g5h5 g1f3 b7b6 a2a3 b4e7 h2h3 c8b7 g2g4 h5h6 e3e4 e8g8 d4d5 g8h8 g4g5 h6h5 f1e2 b7a6 e2a6 h5f3 a6b7 e7a3 b7a8 e6d5 d1f1 f3h5 c3d5 c7c6 b2a3 c6d5 a8d5 f8c8 d5b7 c8e8 e4e5 f7f5 d2d6 h5e2 h3h4 b6b5 h4h5 b5b4 a3b4 e2b5 d6d5 b5b4 g5g6 b4a3 c1d2 a3b4 c2c3 b4b2 d2d3 e8e7 g6h7 h8h7 h5h6 g7g5 f4g5 d7d6 f1f5 d6e5 f5e5 e7d7 g5g6 h7g6 d3e4 d7d5 e4d5 b2b7 d5d4 b7h1 e5e8 h1d1 d4c4 d1a4 c4d3 a4e8 h6h7 g6h7 c3c4 e8e5 c4c5 e5c5 d3e4 h7g7 e4f4 c5d5 f4e3 b8d7 e3f4 d7f6 f4e3 f6e4 e3f4 g7g6 f4e3 g6g7 e3f4 g7g6 f4e3 g6g7";
    	
    	//d7e8 is bad because of three fold repetition
    	//String inputString = "position startpos moves e2e3 d7d5 d1f3 d8d6 f1e2 h7h5 e2b5 c7c6 f3e2 c6b5 e2b5 d6c6 a2a4 e7e6 g1e2 c6b5 a4b5 f8d6 b5b6 b8d7 a1a7 d7b6 a7a8 b6a8 c2c3 b7b6 h2h4 e6e5 h1g1 c8f5 b1a3 f5d3 b2b4 d6e7 g1h1 g8f6 e2g3 a8c7 f2f3 e8d7 e1f2 h8a8 f2g1 g7g6 c1b2 f6h7 h1h3 c7e6 h3h2 e5e4 f3f4 f7f5 h2h1 d7c8 g1f2 h7f6 f2e1 f6g4 h1h3 e7f6 h3h1 c8d8 h1h3 d8e8 h3h1 e8e7 h1h3 e7e8 b2c1 e8d7 c1b2";
    	
    	//Mate in 3
    	//String inputString = "position fen 1r3Q2/3k3N/8/n1PK4/3p4/3P4/5R2/8 b - - 2 56";
    	//UCI.inputIsReady();
    	//UCI.inputPosition(inputString);
    	//UCI.inputPrint();
    	//UCI.inputGo("go");
    	
        UCI.uciCommunication();
    }
}