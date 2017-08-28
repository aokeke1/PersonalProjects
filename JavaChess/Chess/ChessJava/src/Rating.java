import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class Rating {
    public static int evaluate(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove) {
        /*
         * Used for Scoring 1-7
         */
    	return Scoring6(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
    }
    public static int evaluate2(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite) {
        /*
         * Used for Scoring 8-15 and 17
         */
    	return Scoring15(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
    }
    public static int evaluate2(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean whiteHasCastled,boolean blackHasCastled,boolean WhiteToMove,boolean selfColorIsWhite) {
        /*
         * Used for Scoring 16 and 18
         */
    	return Scoring18(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,whiteHasCastled,blackHasCastled,WhiteToMove,selfColorIsWhite);
    }
    public static int Scoring2(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove){
    	/*
    	 * Uses a completely random system
    	 */
    	Random rand = new Random();
    	return rand.nextInt(101);
    }
    
    public static int Scoring3(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove){
    	/*
    	 * Minimized the scores of the opponent pieces
    	 */
        int numQueens,numRooks,numBishops,numKnights,numPawns;
        if (WhiteToMove) {
        	numQueens = bitCount(BQ);
        	numRooks = bitCount(BR);
        	numBishops = bitCount(BB);
        	numKnights = bitCount(BN);
        	numPawns = bitCount(BP);
        }else{
        	numQueens = bitCount(WQ);
        	numRooks = bitCount(WR);
        	numBishops = bitCount(WB);
        	numKnights = bitCount(WN);
        	numPawns = bitCount(WP);       	
        }
        int score = 100-numQueens*9-numRooks*5-(numKnights+numBishops)*3-numPawns;
    	return score;
    }
    public static int Scoring4(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove){
    	/*
    	 * Minimizes the score of the opponents pieces and maximizes the score of own pieces
    	 */
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (WhiteToMove) {
        	numQueens = bitCount(BQ);
        	numRooks = bitCount(BR);
        	numBishops = bitCount(BB);
        	numKnights = bitCount(BN);
        	numPawns = bitCount(BP);
        	numMyQueens = bitCount(WQ);
        	numMyRooks = bitCount(WR);
        	numMyBishops = bitCount(WB);
        	numMyKnights = bitCount(WN);
        	numMyPawns = bitCount(WP);
        }else{
        	numQueens = bitCount(WQ);
        	numRooks = bitCount(WR);
        	numBishops = bitCount(WB);
        	numKnights = bitCount(WN);
        	numPawns = bitCount(WP);
        	numMyQueens = bitCount(BQ);
        	numMyRooks = bitCount(BR);
        	numMyBishops = bitCount(BB);
        	numMyKnights = bitCount(BN);
        	numMyPawns = bitCount(BP);
        	
        }
        int score = 100 -numQueens*9-numRooks*5-(numKnights+numBishops)*3-numPawns;
        score = score+numMyQueens*9+numMyRooks*5+(numMyKnights+numMyBishops)*3+numMyPawns;
    	return score;
    }
    public static int Scoring5(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove){
    	/*
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces
    	 */
    	
    	//Number of available moves
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();

        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (WhiteToMove) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (WhiteToMove) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        
        score += unsafeScore/2;
    	return score;
    }
    
     public static int Scoring6(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove){
    	/*
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 */
    	
    	//Number of available moves
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();

        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (WhiteToMove) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (WhiteToMove) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        
        score += unsafeScore/4;
    	return score;
    }
    

    public static int Scoring7(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove){
    	/*
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Added consideration for threatening king
    	 */
    	
    	//Number of available moves
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = 5000 + moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (WhiteToMove) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (WhiteToMove) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        unsafeScore = unsafeScore + 1300*bitCount(yourKing&unsafeForYou) - 1300*bitCount(myKing&unsafeForMe);
        score += unsafeScore/2;
    	return score;
    }
   
    public static int Scoring8(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Added consideration for threatening king
    	 */
    	
    	//Number of available moves
        String moves;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        unsafeScore = unsafeScore + 900*bitCount(yourKing&unsafeForYou) - 900*bitCount(myKing&unsafeForMe);
        score += unsafeScore/4;
        //System.out.println(score);
    	return score;
    }
    public static int Scoring9(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Reduced consideration for threatening king
    	 * Added avoiding insufficient pieces draws
    	 * Added a bias for moving pawns forward.
    	 * Added points for protecting pieces
    	 */
    	
    	//Number of available moves
        String moves;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
    	//Should also check the color of the squares the bishops are on.
    	int usefulMyPieces = numMyQueens + numMyRooks + numMyPawns;
    	int usefulOpPieces = numQueens + numRooks + numPawns;
    	if (usefulMyPieces==0 && usefulOpPieces==0){
    		//Avoid insufficient pieces stalemate
    		if (((numMyKnights + numMyBishops)<=1)&&((numKnights + numBishops)<=1)){
    			return -Orion.MATE_SCORE/2;
    		}
    	}
    	else if (usefulMyPieces==0){
    		// Don't lose enough pieces to the point where I can't force a checkmate
    		if ((numMyKnights<=2 && numMyBishops==0)||(numMyKnights==0 && numMyBishops==1)){
    			return -Orion.MATE_SCORE;
    		}
    	}
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        unsafeScore = unsafeScore + 400*bitCount(yourKing&unsafeForYou) - 400*bitCount(myKing&unsafeForMe);
        score += unsafeScore/4;
        
        //Weigh Protections
        int safeScore = 64*bitCount(yourPawns&unsafeForMe) + 300*bitCount((yourBishops|yourKnights)&unsafeForMe) + 500*bitCount(yourRooks&unsafeForMe) + 900*bitCount(yourQueens&unsafeForMe);
        safeScore = safeScore - 64*bitCount(myPawns&unsafeForYou) - 300*bitCount((myBishops|myKnights)&unsafeForYou) - 500*bitCount(myRooks&unsafeForYou) - 900*bitCount(myQueens&unsafeForYou);
        safeScore = safeScore + 400*bitCount(yourKing&unsafeForMe) - 400*bitCount(myKing&unsafeForYou);
        score += safeScore/4;
        
        //Support moving pawns down toward promotion
        if (numMyPawns!=0){
        	List<Integer> myPawnLocations = BoardGeneration.bitPositions(myPawns);
        	double sumDistances = 0;
        	for (int i:myPawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 8*sumDistances/numMyPawns);
        }
        if (numPawns!=0){
        	List<Integer> yourPawnLocations = BoardGeneration.bitPositions(yourPawns);
        	double sumDistances = 0;
        	for (int i:yourPawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}
        	score = (int) (score - 8*sumDistances/numPawns);
        }
        
        //System.out.println(score);
    	return score;
    }

    public static int Scoring10(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Similar to Scoring6
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Removed king threatening considerations
    	 * Added avoiding insufficient pieces draws
    	 * Added a bias for moving pawns forward.
    	 * 
    	 */
    	
    	//Number of available moves
        String moves;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
    	//Should also check the color of the squares the bishops are on.
    	int usefulMyPieces = numMyQueens + numMyRooks + numMyPawns;
    	int usefulOpPieces = numQueens + numRooks + numPawns;
    	if (usefulMyPieces==0 && usefulOpPieces==0){
    		//Avoid insufficient pieces stalemate
    		if (((numMyKnights + numMyBishops)<=1)&&((numKnights + numBishops)<=1)){
    			return -Orion.MATE_SCORE/2;
    		}
    	}
    	else if (usefulMyPieces==0){
    		// Don't lose enough pieces to the point where I can't force a checkmate
    		if ((numMyKnights<=2 && numMyBishops==0)||(numMyKnights==0 && numMyBishops==1)){
    			return -Orion.MATE_SCORE;
    		}
    	}
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        score += unsafeScore/4;
        
        
        //Support moving pawns down toward promotion
        if (numMyPawns!=0){
        	List<Integer> myPawnLocations = BoardGeneration.bitPositions(myPawns);
        	double sumDistances = 0;
        	for (int i:myPawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 8*sumDistances/numMyPawns);
        }
        if (numPawns!=0){
        	List<Integer> yourPawnLocations = BoardGeneration.bitPositions(yourPawns);
        	double sumDistances = 0;
        	for (int i:yourPawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}
        	score = (int) (score - 8*sumDistances/numPawns);
        }
        
        //System.out.println(score);
    	return score;
    }


    public static int Scoring11(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Similar to Scoring6
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Removed king threatening considerations
    	 * Added avoiding insufficient pieces draws
    	 * Added a bias for moving pawns forward.
    	 * Considers protected pieces
    	 */
    	
    	//Number of available moves
        String moves;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
    	//Should also check the color of the squares the bishops are on.
    	int usefulMyPieces = numMyQueens + numMyRooks + numMyPawns;
    	int usefulOpPieces = numQueens + numRooks + numPawns;
    	if (usefulMyPieces==0 && usefulOpPieces==0){
    		//Avoid insufficient pieces stalemate
    		if (((numMyKnights + numMyBishops)<=1)&&((numKnights + numBishops)<=1)){
    			return -Orion.MATE_SCORE/2;
    		}
    	}
    	else if (usefulMyPieces==0){
    		// Don't lose enough pieces to the point where I can't force a checkmate
    		if ((numMyKnights<=2 && numMyBishops==0)||(numMyKnights==0 && numMyBishops==1)){
    			return -Orion.MATE_SCORE;
    		}
    	}
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        score += unsafeScore/4;
        
        //Weigh Protections
        int safeScore = 64*bitCount(yourPawns&unsafeForMe) + 300*bitCount((yourBishops|yourKnights)&unsafeForMe) + 500*bitCount(yourRooks&unsafeForMe) + 900*bitCount(yourQueens&unsafeForMe);
        safeScore = safeScore - 64*bitCount(myPawns&unsafeForYou) - 300*bitCount((myBishops|myKnights)&unsafeForYou) - 500*bitCount(myRooks&unsafeForYou) - 900*bitCount(myQueens&unsafeForYou);
        score += safeScore/4;
        
        //Support moving pawns down toward promotion
        if (numMyPawns!=0){
        	List<Integer> myPawnLocations = BoardGeneration.bitPositions(myPawns);
        	double sumDistances = 0;
        	for (int i:myPawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 8*sumDistances/numMyPawns);
        }
        if (numPawns!=0){
        	List<Integer> yourPawnLocations = BoardGeneration.bitPositions(yourPawns);
        	double sumDistances = 0;
        	for (int i:yourPawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}
        	score = (int) (score - 8*sumDistances/numPawns);
        }
        
        //System.out.println(score);
    	return score;
    }


    public static int Scoring12(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Similar to Scoring6 and Scoring10
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Removed king threatening considerations
    	 * Added avoiding insufficient pieces draws
    	 * Added a bias for moving pawns forward.
    	 *  --> slight increase in weight of pawn distance from promotion from 8 to 12
    	 */
    	
    	//Number of available moves
        String moves;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
    	//Should also check the color of the squares the bishops are on.
    	int usefulMyPieces = numMyQueens + numMyRooks + numMyPawns;
    	int usefulOpPieces = numQueens + numRooks + numPawns;
    	if (usefulMyPieces==0 && usefulOpPieces==0){
    		//Avoid insufficient pieces stalemate
    		if (((numMyKnights + numMyBishops)<=1)&&((numKnights + numBishops)<=1)){
    			return -Orion.MATE_SCORE/2;
    		}
    	}
    	else if (usefulMyPieces==0){
    		// Don't lose enough pieces to the point where I can't force a checkmate
    		if ((numMyKnights<=2 && numMyBishops==0)||(numMyKnights==0 && numMyBishops==1)){
    			return -Orion.MATE_SCORE;
    		}
    	}
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        score += unsafeScore/4;
        
        
        //Support moving pawns down toward promotion and penalize allowing opponent to move pawns
        if ((numMyPawns|numPawns)!=0){
        	List<Integer> pawnLocations = BoardGeneration.bitPositions(myPawns|numPawns);
        	double sumDistances = 0;
        	for (int i:pawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 12*sumDistances/(numMyPawns+numPawns));
        }
        
        //System.out.println(score);
    	return score;
    }


    public static int Scoring13(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Similar to Scoring12
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Removed king threatening considerations
    	 * Added avoiding insufficient pieces draws
    	 * Added a bias for moving pawns forward.
    	 *  --> slight increase in weight of pawn distance from promotion from 8 to 12
    	 *  discourages use of queen when (knights+bishops)>2 -- this oversimplifies a more complicated component
    	 *
    	 */
    	
    	//Number of available moves
        String moves;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        //moves = Moves.filterMoves(moves, selfColorIsWhite, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
    	//Should also check the color of the squares the bishops are on.
    	int usefulMyPieces = numMyQueens + numMyRooks + numMyPawns;
    	int usefulOpPieces = numQueens + numRooks + numPawns;
    	if (usefulMyPieces==0 && usefulOpPieces==0){
    		//Avoid insufficient pieces stalemate
    		if (((numMyKnights + numMyBishops)<=1)&&((numKnights + numBishops)<=1)){
    			return -Orion.MATE_SCORE/2;
    		}
    	}
    	else if (usefulMyPieces==0){
    		// Don't lose enough pieces to the point where I can't force a checkmate
    		if ((numMyKnights<=2 && numMyBishops==0)||(numMyKnights==0 && numMyBishops==1)){
    			return -Orion.MATE_SCORE;
    		}
    	}
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        score += unsafeScore/4;
        
        
        //Support moving pawns down toward promotion and penalize allowing opponent to move pawns
        if ((numMyPawns|numPawns)!=0){
        	List<Integer> pawnLocations = BoardGeneration.bitPositions(myPawns|numPawns);
        	double sumDistances = 0;
        	for (int i:pawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 12*sumDistances/(numMyPawns+numPawns));
        }
        
        //Discourage premature queen usage. Only start developing queen after I have lost two pieces from bishop and knight
        if ((numMyBishops+numMyKnights)>2){
        	String queenMoves;
        	if(selfColorIsWhite){
        		Moves.NOT_MY_PIECES = ~(WP|WN|WB|WR|WQ|WK|BK); //Added BK to avoid illegal capture
        		Moves.MY_PIECES = WP|WN|WB|WR|WQ;//omitted WK to avoid illegal capture
        		Moves.OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
        		Moves.EMPTY = ~Moves.OCCUPIED;
        		queenMoves = Moves.possibleQ(Moves.OCCUPIED,WQ);
        	}
        	else{
        		Moves.NOT_MY_PIECES = ~(BP|BN|BB|BR|BQ|BK|WK); //Added WK to avoid illegal capture
        		Moves.MY_PIECES = BP|BN|BB|BR|BQ;//omitted WK to avoid illegal capture
        		Moves.OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
        		Moves.EMPTY = ~Moves.OCCUPIED;
        		queenMoves = Moves.possibleQ(Moves.OCCUPIED,BQ);
        	}
    		queenMoves = Moves.filterMoves(queenMoves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
    		//queenMoves = Moves.filterMoves(queenMoves, selfColorIsWhite, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        	score-=queenMoves.length();
        }
        
        //System.out.println(score);
    	return score;
    }
    
    public static int Scoring14(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Similar to Scoring12 --> changed the move filtering to what I think will actually work
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Removed king threatening considerations
    	 * Added avoiding insufficient pieces draws
    	 * Added a bias for moving pawns forward.
    	 *  --> slight increase in weight of pawn distance from promotion from 8 to 12
    	 */
    	
    	//Number of available moves
        String moves;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, selfColorIsWhite, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
    	//Should also check the color of the squares the bishops are on.
    	int usefulMyPieces = numMyQueens + numMyRooks + numMyPawns;
    	int usefulOpPieces = numQueens + numRooks + numPawns;
    	if (usefulMyPieces==0 && usefulOpPieces==0){
    		//Avoid insufficient pieces stalemate
    		if (((numMyKnights + numMyBishops)<=1)&&((numKnights + numBishops)<=1)){
    			return -Orion.MATE_SCORE/2;
    		}
    	}
    	else if (usefulMyPieces==0){
    		// Don't lose enough pieces to the point where I can't force a checkmate
    		if ((numMyKnights<=2 && numMyBishops==0)||(numMyKnights==0 && numMyBishops==1)){
    			return -Orion.MATE_SCORE;
    		}
    	}
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        score += unsafeScore/4;
        
        
        //Support moving pawns down toward promotion and penalize allowing opponent to move pawns
        if ((numMyPawns|numPawns)!=0){
        	List<Integer> pawnLocations = BoardGeneration.bitPositions(myPawns|numPawns);
        	double sumDistances = 0;
        	for (int i:pawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 12*sumDistances/(numMyPawns+numPawns));
        }
        
        //System.out.println(score);
    	return score;
    }
    
    public static int Scoring15(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Similar to Scoring13
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Removed king threatening considerations
    	 * Added avoiding insufficient pieces draws
    	 * Added a bias for moving pawns forward.
    	 *  --> slight increase in weight of pawn distance from promotion from 8 to 12
    	 *  discourages use of queen when (knights+bishops)>2 -- this oversimplifies a more complicated component
    	 *  --> difference from 14: considers number of moves opponent can make
    	 */
    	
    	//Number of available moves
        String moves,movesOp;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
            movesOp=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
        	movesOp=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        	moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        movesOp = Moves.filterMoves(movesOp, !WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        //moves = Moves.filterMoves(moves, selfColorIsWhite, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        //movesOp = Moves.filterMoves(movesOp, !selfColorIsWhite, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        score -= movesOp.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
    	//Should also check the color of the squares the bishops are on.
    	int usefulMyPieces = numMyQueens + numMyRooks + numMyPawns;
    	int usefulOpPieces = numQueens + numRooks + numPawns;
    	if (usefulMyPieces==0 && usefulOpPieces==0){
    		//Avoid insufficient pieces stalemate
    		if (((numMyKnights + numMyBishops)<=1)&&((numKnights + numBishops)<=1)){
    			return -Orion.MATE_SCORE/2;
    		}
    	}
    	else if (usefulMyPieces==0){
    		// Don't lose enough pieces to the point where I can't force a checkmate
    		if ((numMyKnights<=2 && numMyBishops==0)||(numMyKnights==0 && numMyBishops==1)){
    			return -Orion.MATE_SCORE+1+Orion.searchDepth;
    		}
    	}
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        score += unsafeScore/4;
        
        
        //Support moving pawns down toward promotion and penalize allowing opponent to move pawns
        if ((numMyPawns|numPawns)!=0){
        	List<Integer> pawnLocations = BoardGeneration.bitPositions(myPawns|numPawns);
        	double sumDistances = 0;
        	for (int i:pawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 12*sumDistances/(numMyPawns+numPawns));
        }
        
        //Discourage premature queen usage. Only start developing queen after I have lost two pieces from bishop and knight
        if ((numMyBishops+numMyKnights)>2){
        	String queenMoves;
        	if(selfColorIsWhite){
        		Moves.NOT_MY_PIECES = ~(WP|WN|WB|WR|WQ|WK|BK); //Added BK to avoid illegal capture
        		Moves.MY_PIECES = WP|WN|WB|WR|WQ;//omitted WK to avoid illegal capture
        		Moves.OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
        		Moves.EMPTY = ~Moves.OCCUPIED;
        		queenMoves = Moves.possibleQ(Moves.OCCUPIED,WQ);

        	}
        	else{
        		Moves.NOT_MY_PIECES = ~(BP|BN|BB|BR|BQ|BK|WK); //Added WK to avoid illegal capture
        		Moves.MY_PIECES = BP|BN|BB|BR|BQ;//omitted WK to avoid illegal capture
        		Moves.OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
        		Moves.EMPTY = ~Moves.OCCUPIED;
        		queenMoves = Moves.possibleQ(Moves.OCCUPIED,BQ);
        	}
    		queenMoves = Moves.filterMoves(queenMoves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
    		//queenMoves = Moves.filterMoves(queenMoves, selfColorIsWhite, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        	score-=queenMoves.length();
        }
        //Do the same for the opponent's queen
        if ((numBishops+numKnights)>2){
        	String queenMoves;
        	if(!selfColorIsWhite){
        		Moves.NOT_MY_PIECES = ~(WP|WN|WB|WR|WQ|WK|BK); //Added BK to avoid illegal capture
        		Moves.MY_PIECES = WP|WN|WB|WR|WQ;//omitted WK to avoid illegal capture
        		Moves.OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
        		Moves.EMPTY = ~Moves.OCCUPIED;
        		queenMoves = Moves.possibleQ(Moves.OCCUPIED,WQ);
        	}
        	else{
        		Moves.NOT_MY_PIECES = ~(BP|BN|BB|BR|BQ|BK|WK); //Added WK to avoid illegal capture
        		Moves.MY_PIECES = BP|BN|BB|BR|BQ;//omitted WK to avoid illegal capture
        		Moves.OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
        		Moves.EMPTY = ~Moves.OCCUPIED;
        		queenMoves = Moves.possibleQ(Moves.OCCUPIED,BQ);
        	}
    		queenMoves = Moves.filterMoves(queenMoves, !WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
    		//queenMoves = Moves.filterMoves(queenMoves, !selfColorIsWhite, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        	score+=queenMoves.length();
        }
        
        //System.out.println(score);
    	return score;
    }
    
    public static double [] machineLearningCoefficients = {};
    
    @SuppressWarnings({ "rawtypes", "unchecked" })
	public static int Scoring16(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteHasCastled,boolean BlackHasCastled,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Uses the results of the machine learning to try and score the board
    	 */
    	
    	//Number of available moves
    	double score=0;
		ArrayList boardInformation = new ArrayList();
		boardInformation.add(WK);
		boardInformation.add(WQ);
		boardInformation.add(WB);
		boardInformation.add(WN);
		boardInformation.add(WR);
		boardInformation.add(WP);
		boardInformation.add(BK);
		boardInformation.add(BQ);
		boardInformation.add(BB);
		boardInformation.add(BN);
		boardInformation.add(BR);
		boardInformation.add(BP);
		boardInformation.add(EP);
		boardInformation.add(CWK);
		boardInformation.add(CWQ);
		boardInformation.add(CBK);
		boardInformation.add(CBQ);
		boardInformation.add(WhiteHasCastled);
		boardInformation.add(BlackHasCastled);
		boardInformation.add(WhiteToMove);
		int[] values = MachineLearning.evaluate1(boardInformation);
		for (int i=0;i<values.length;i++){
			score += machineLearningCoefficients[i]*values[i];
		}
		if (!selfColorIsWhite){
			//flip the score if black
			score = -score;
		}
        //System.out.println(score);
    	return (int) score;
    }
    

    public static int Scoring17(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Similar to Scoring6 and Scoring10 but without the insufficient piece checking
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Removed king threatening considerations
    	 * Added a bias for moving pawns forward.
    	 *  --> slight increase in weight of pawn distance from promotion from 8 to 12
    	 */
    	
    	//Number of available moves
        String moves;
        if (selfColorIsWhite) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (selfColorIsWhite) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (selfColorIsWhite) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        score += unsafeScore/4;
        
        
        //Support moving pawns down toward promotion and penalize allowing opponent to move pawns
        if ((numMyPawns|numPawns)!=0){
        	List<Integer> pawnLocations = BoardGeneration.bitPositions(myPawns|numPawns);
        	double sumDistances = 0;
        	for (int i:pawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (selfColorIsWhite){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 12*sumDistances/(numMyPawns+numPawns));
        	//System.out.println(score);
        }
        //System.out.println(score);
        //System.out.println(score);
    	return score;
    }
    public static int Scoring17b(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Similar to Scoring6 and Scoring10 but without the insufficient piece checking
    	 * Weighs material value and number of available moves.
    	 * Also considers threatened pieces.
    	 * Less emphasis on threatened pieces than Scoring5
    	 * Removed king threatening considerations
    	 * Added a bias for moving pawns forward.
    	 *  --> slight increase in weight of pawn distance from promotion from 8 to 12
    	 *  --> same as 17 but uses WhiteToMove instead of selfColorIsWhite
    	 */
    	
    	//Number of available moves
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        int score = moves.length();
        //Material value
        long myQueens,yourQueens,myRooks,yourRooks,myKnights,yourKnights,myBishops,yourBishops,myPawns,yourPawns,myKing,yourKing;
        int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
        if (WhiteToMove) {
        	myQueens=WQ;yourQueens=BQ;
        	myRooks=WR;yourRooks=BR;
        	myKnights=WN;yourKnights=BN;
        	myBishops=WB;yourBishops=BB;
        	myPawns=WP;yourPawns=BP;
        	myKing=WK;yourKing=BK;
        	
        }else{
        	myQueens=BQ;yourQueens=WQ;
        	myRooks=BR;yourRooks=WR;
        	myKnights=BN;yourKnights=WN;
        	myBishops=BB;yourBishops=WB;
        	myPawns=BP;yourPawns=WP;
        	myKing=BK;yourKing=WK;
        }
    	numQueens = bitCount(yourQueens);
    	numRooks = bitCount(yourRooks);
    	numBishops = bitCount(yourBishops);
    	numKnights = bitCount(yourKnights);
    	numPawns = bitCount(yourPawns);
    	numMyQueens = bitCount(myQueens);
    	numMyRooks = bitCount(myRooks);
    	numMyBishops = bitCount(myBishops);
    	numMyKnights = bitCount(myKnights);
    	numMyPawns = bitCount(myPawns);
    	
        score = score - 900*numQueens-500*numRooks-300*numKnights-100*numPawns;
        score = score+900*numMyQueens+500*numMyRooks+300*numMyKnights+100*numMyPawns;
        if (numMyBishops>=2){
        	score+=numMyBishops*300;
        }
        else{
        	score+=numMyBishops*250;
        }
        if (numBishops>=2){
        	score-=numBishops*300;
        }
        else{
        	score-=numBishops*250;
        }
        
        //Weigh Threats
        long unsafeForMe,unsafeForYou;
        if (WhiteToMove) {
        	unsafeForMe=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForYou=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        } else {
        	unsafeForYou=Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        	unsafeForMe=Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
        }
        
        int unsafeScore = 64*bitCount(yourPawns&unsafeForYou) + 300*bitCount((yourBishops|yourKnights)&unsafeForYou) + 500*bitCount(yourRooks&unsafeForYou) + 900*bitCount(yourQueens&unsafeForYou);
        unsafeScore = unsafeScore - 64*bitCount(myPawns&unsafeForMe) - 300*bitCount((myBishops|myKnights)&unsafeForMe) - 500*bitCount(myRooks&unsafeForMe) - 900*bitCount(myQueens&unsafeForMe);
        score += unsafeScore/4;
        
        
        //Support moving pawns down toward promotion and penalize allowing opponent to move pawns
        if ((numMyPawns|numPawns)!=0){
        	List<Integer> pawnLocations = BoardGeneration.bitPositions(myPawns|numPawns);
        	double sumDistances = 0;
        	for (int i:pawnLocations){
            	//If I am white, minimize the distance between pawn and rank 1
        		if (WhiteToMove){
        			sumDistances += (7-i/8);
        		}
            	//If I am black, minimize the distance between pawn and rank 8
        		else{
        			sumDistances += (i/8);
        		}
        	}

        	score = (int) (score - 12*sumDistances/numMyPawns);
        }
        
        //System.out.println(score);
    	return score;
    }

    
    @SuppressWarnings({ "rawtypes", "unchecked" })
	public static int Scoring18(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteHasCastled,boolean BlackHasCastled,boolean WhiteToMove,boolean selfColorIsWhite){
    	/*
    	 * Uses the results of the machine learning to try and score the board
    	 */
    	
    	//Number of available moves
    	double score=0;
		ArrayList boardInformation = new ArrayList();
		boardInformation.add(WK);
		boardInformation.add(WQ);
		boardInformation.add(WB);
		boardInformation.add(WN);
		boardInformation.add(WR);
		boardInformation.add(WP);
		boardInformation.add(BK);
		boardInformation.add(BQ);
		boardInformation.add(BB);
		boardInformation.add(BN);
		boardInformation.add(BR);
		boardInformation.add(BP);
		boardInformation.add(EP);
		boardInformation.add(CWK);
		boardInformation.add(CWQ);
		boardInformation.add(CBK);
		boardInformation.add(CBQ);
		boardInformation.add(WhiteHasCastled);
		boardInformation.add(BlackHasCastled);
		boardInformation.add(WhiteToMove);
		int[] values = MachineLearning.evaluate1(boardInformation);
		double[][] newValues = new double [1][21];
		//Difference in pieces ignoring kings
		for(int i=0;i<5;i++){
			newValues[0][i] = values[i+1]-values[i+7];
		}
		//Protected white-threatened white
		//Protected black-threatened black
		for(int i=0;i<6;i++){
			newValues[0][i+5] = values[i+26]-values[i+32];
			newValues[0][i+11] = values[i+38]-values[i+44];
		}
		
		//white has castled
		newValues[0][17] = values[58];
		//black has castled
		newValues[0][18] = values[59];
		//pawn distances/840
		newValues[0][19] = (values[50]-values[51])/840.0;
		// (whiteMoves-blackMoves)/20
		int sumOfMoves = 0;
		for(int i=0;i<6;i++){
			sumOfMoves = sumOfMoves + values[i+12]-values[i+18];//regular moves
		}
		sumOfMoves = sumOfMoves + values[24]-values[25];//add castling
		newValues[0][20] = sumOfMoves/20.0;
		
		//System.out.println(Arrays.toString(newValues[0]));
		score = NeuralNetwork.Scoring18(newValues);
		if (!selfColorIsWhite){
			//flip the score if black
			score = -score;
		}
        //System.out.println(score);
    	return (int) score;
    }
    
    public static int bitCount(long i) {
	    /*
	     * Counts the number of 1's in the binary form of a long.
	     */
		int count = 0;
		while (i!=0){
			count++;
			i = (i>>>Long.numberOfTrailingZeros(i))>>>1;
		}
	    return count;
	}
	
	public static String sortMoves(String moves,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,boolean selfColorIsWhite){
		int firstBestScore = -100000;
		int secondBestScore = -100000;
		String firstBestMove = "";
		String secondBestMove = "";
		String otherMoves ="";
		int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;

		for (int i=0;i<moves.length();i+=4){
			//Make move
            long 
            WPt=Moves.makeMove(WP, moves.substring(i,i+4), 'P'),
            WNt=Moves.makeMove(WN, moves.substring(i,i+4), 'N'),
            WBt=Moves.makeMove(WB, moves.substring(i,i+4), 'B'),
            WRt=Moves.makeMove(WR, moves.substring(i,i+4), 'R'),
            WQt=Moves.makeMove(WQ, moves.substring(i,i+4), 'Q'),
            WKt=Moves.makeMove(WK, moves.substring(i,i+4), 'K'),
            BPt=Moves.makeMove(BP, moves.substring(i,i+4), 'p'),
            BNt=Moves.makeMove(BN, moves.substring(i,i+4), 'n'),
            BBt=Moves.makeMove(BB, moves.substring(i,i+4), 'b'),
            BRt=Moves.makeMove(BR, moves.substring(i,i+4), 'r'),
            BQt=Moves.makeMove(BQ, moves.substring(i,i+4), 'q'),
            BKt=Moves.makeMove(BK, moves.substring(i,i+4), 'k'),
            EPt=Moves.makeMoveEP(WP|BP,moves.substring(i,i+4));
            WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(i,i+4), 'r');
            boolean CWKt=CWK,
            CWQt=CWQ,
            CBKt=CBK,
            CBQt=CBQ;
            int start=0,end=0;
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
            //Always check if we are breaking the castling
            if (((1L<<start)&WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start)&BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start)|(1L<<end))&WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start)|(1L<<end))&WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start)|(1L<<end))&BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start)|(1L<<end))&BR&(1L<<56))!=0) {CBQt=false;}

			//Score move
        	int score = myInt*Rating.evaluate2(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,selfColorIsWhite);
			if (score>=firstBestScore){
				otherMoves = secondBestMove + otherMoves;
				secondBestMove = firstBestMove;
				secondBestScore= firstBestScore;
				firstBestMove = moves.substring(i, i+4);
				firstBestScore = score;
			}
			else if (score>=secondBestScore){
				otherMoves = secondBestMove + otherMoves;
				secondBestMove = moves.substring(i, i+4);
				secondBestScore= score;
			}
			else{
				otherMoves += moves.substring(i, i+4);
			}
		}
		return firstBestMove+secondBestMove+otherMoves;
	}

	public static String sortMoves(String moves,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteHasCastled,boolean BlackHasCastled,boolean WhiteToMove,boolean selfColorIsWhite){
		int firstBestScore = -100000;
		int secondBestScore = -100000;
		String firstBestMove = "";
		String secondBestMove = "";
		String otherMoves ="";
		int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;

		for (int i=0;i<moves.length();i+=4){
			//Make move
            boolean WhiteHasCastledt=WhiteHasCastled,
            		BlackHasCastledt=BlackHasCastled;
            long 
            WPt=Moves.makeMove(WP, moves.substring(i,i+4), 'P'),
            WNt=Moves.makeMove(WN, moves.substring(i,i+4), 'N'),
            WBt=Moves.makeMove(WB, moves.substring(i,i+4), 'B'),
            WRt=Moves.makeMove(WR, moves.substring(i,i+4), 'R'),
            WQt=Moves.makeMove(WQ, moves.substring(i,i+4), 'Q'),
            WKt=Moves.makeMove(WK, moves.substring(i,i+4), 'K'),
            BPt=Moves.makeMove(BP, moves.substring(i,i+4), 'p'),
            BNt=Moves.makeMove(BN, moves.substring(i,i+4), 'n'),
            BBt=Moves.makeMove(BB, moves.substring(i,i+4), 'b'),
            BRt=Moves.makeMove(BR, moves.substring(i,i+4), 'r'),
            BQt=Moves.makeMove(BQ, moves.substring(i,i+4), 'q'),
            BKt=Moves.makeMove(BK, moves.substring(i,i+4), 'k'),
            EPt=Moves.makeMoveEP(WP|BP,moves.substring(i,i+4));
            long oldWR=WRt,oldBR = BRt;
            WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(i,i+4), 'r');
            if(oldWR!=WRt){
        	    WhiteHasCastledt = true;
            }
            if(oldBR!=BRt){
        	    BlackHasCastledt = true;
            }
            boolean CWKt=CWK,
            CWQt=CWQ,
            CBKt=CBK,
            CBQt=CBQ;
            int start=0,end=0;
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
            //Always check if we are breaking the castling
            if (((1L<<start)&WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start)&BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start)|(1L<<end))&WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start)|(1L<<end))&WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start)|(1L<<end))&BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start)|(1L<<end))&BR&(1L<<56))!=0) {CBQt=false;}

			//Score move
        	int score = myInt*Rating.evaluate2(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,WhiteHasCastledt,BlackHasCastledt,!WhiteToMove,selfColorIsWhite);
			if (score>=firstBestScore){
				otherMoves = secondBestMove + otherMoves;
				secondBestMove = firstBestMove;
				secondBestScore= firstBestScore;
				firstBestMove = moves.substring(i, i+4);
				firstBestScore = score;
			}
			else if (score>=secondBestScore){
				otherMoves = secondBestMove + otherMoves;
				secondBestMove = moves.substring(i, i+4);
				secondBestScore= score;
			}
			else{
				otherMoves += moves.substring(i, i+4);
			}
		}
		return firstBestMove+secondBestMove+otherMoves;
	}
}
