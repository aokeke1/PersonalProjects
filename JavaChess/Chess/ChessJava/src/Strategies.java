import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Strategies {
	public static String bestMove;
	public static String Strategy1(String moves){
		int index=(int)(Math.floor(Math.random()*(moves.length()/4))*4);
		return moves.substring(index,index+4);
	}
	public static String Strategy2(String moves){
        /*
         * Always checkmate if possible. Otherwise choose a random move.
         */
		int index=(int)(Math.floor(Math.random()*(moves.length()/4))*4);
		String defaultMove = moves.substring(index,index+4);
        String bestMove = "";
        int start=0,end=0;
        for (int i=0;i<moves.length();i+=4) {
        	//Get the start and end position for checking castling
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
            //Always check if we are breaking the castling rights
            boolean CWKt=Orion.CWK,CWQt=Orion.CWQ,CBKt=Orion.CBK,CBQt=Orion.CBQ;
            if (((1L<<start)&Orion.WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start)&Orion.BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<56))!=0) {CBQt=false;}
            
            //Do the moves
            long EPt=Moves.makeMoveEP(Orion.WP|Orion.BP,moves.substring(i,i+4)),
            WPt=Moves.makeMove(Orion.WP, moves.substring(i,i+4), 'P'),
            WNt=Moves.makeMove(Orion.WN, moves.substring(i,i+4), 'N'),
            WBt=Moves.makeMove(Orion.WB, moves.substring(i,i+4), 'B'),
            WRt=Moves.makeMove(Orion.WR, moves.substring(i,i+4), 'R'),
            WQt=Moves.makeMove(Orion.WQ, moves.substring(i,i+4), 'Q'),
            WKt=Moves.makeMove(Orion.WK, moves.substring(i,i+4), 'K'),
            BPt=Moves.makeMove(Orion.BP, moves.substring(i,i+4), 'p'),
            BNt=Moves.makeMove(Orion.BN, moves.substring(i,i+4), 'n'),
            BBt=Moves.makeMove(Orion.BB, moves.substring(i,i+4), 'b'),
            BRt=Moves.makeMove(Orion.BR, moves.substring(i,i+4), 'r'),
            BQt=Moves.makeMove(Orion.BQ, moves.substring(i,i+4), 'q'),
            BKt=Moves.makeMove(Orion.BK, moves.substring(i,i+4), 'k');
            WRt=Moves.makeMoveCastle(Orion.WR, Orion.WK|Orion.BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(Orion.BR, Orion.WK|Orion.BK, moves.substring(i,i+4), 'r');
            boolean WhiteToMovet=!Orion.WhiteToMove;
            String nextMoves = "";
            boolean isChecked;
            if (WhiteToMovet) {
            	nextMoves=Moves.possibleMovesW(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt);
            	isChecked = (WKt&Moves.unsafeForWhite(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt, BKt))!=0;
            } else {
            	nextMoves=Moves.possibleMovesB(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt);
            	isChecked = (BKt&Moves.unsafeForBlack(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt, BKt))!=0;
            }
            //If opponent will have no moves, then do that move.
            nextMoves = Moves.filterMoves(nextMoves,WhiteToMovet,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt);
            if (nextMoves.length()==0&&isChecked){
            	return moves.substring(i,i+4);
            }
        }
        //If no checkmates were possible
        return defaultMove;
	}
	
	public static String Strategy3(String moves){
        /*
         * Always checkmate if possible. Then choose a move to minimize the value of the opponents pieces. Otherwise choose a random move.
         */
		int bestScore = -100;
        String bestMove = "";
        int start=0,end=0;
        for (int i=0;i<moves.length();i+=4) {
        	//Get the start and end position for checking castling
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
            //Always check if we are breaking the castling rights
            boolean CWKt=Orion.CWK,CWQt=Orion.CWQ,CBKt=Orion.CBK,CBQt=Orion.CBQ;
            if (((1L<<start)&Orion.WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start)&Orion.BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<56))!=0) {CBQt=false;}
            
            //Do the moves
            long EPt=Moves.makeMoveEP(Orion.WP|Orion.BP,moves.substring(i,i+4)),
            WPt=Moves.makeMove(Orion.WP, moves.substring(i,i+4), 'P'),
            WNt=Moves.makeMove(Orion.WN, moves.substring(i,i+4), 'N'),
            WBt=Moves.makeMove(Orion.WB, moves.substring(i,i+4), 'B'),
            WRt=Moves.makeMove(Orion.WR, moves.substring(i,i+4), 'R'),
            WQt=Moves.makeMove(Orion.WQ, moves.substring(i,i+4), 'Q'),
            WKt=Moves.makeMove(Orion.WK, moves.substring(i,i+4), 'K'),
            BPt=Moves.makeMove(Orion.BP, moves.substring(i,i+4), 'p'),
            BNt=Moves.makeMove(Orion.BN, moves.substring(i,i+4), 'n'),
            BBt=Moves.makeMove(Orion.BB, moves.substring(i,i+4), 'b'),
            BRt=Moves.makeMove(Orion.BR, moves.substring(i,i+4), 'r'),
            BQt=Moves.makeMove(Orion.BQ, moves.substring(i,i+4), 'q'),
            BKt=Moves.makeMove(Orion.BK, moves.substring(i,i+4), 'k');
            WRt=Moves.makeMoveCastle(WRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'r');
            boolean WhiteToMovet=!Orion.WhiteToMove;
            String nextMoves = "";
            boolean isChecked;
            if (WhiteToMovet) {
            	nextMoves=Moves.possibleMovesW(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt);
            	isChecked = (WKt&Moves.unsafeForWhite(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt, BKt))!=0;
            } else {
            	nextMoves=Moves.possibleMovesB(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt);
            	isChecked = (BKt&Moves.unsafeForBlack(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt, BKt))!=0;
            }
            //If opponent will have no moves, then do that move.
            nextMoves = Moves.filterMoves(nextMoves,WhiteToMovet,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt);
            if (nextMoves.length()==0&&isChecked){
            	System.out.println("info score 100");
            	return moves.substring(i,i+4);
            }
            
            //Count opponents pieces.
            int numQueens,numRooks,numBishops,numKnights,numPawns;
            if (Orion.WhiteToMove) {
            	numQueens = Rating.bitCount(BQt);
            	numRooks = Rating.bitCount(BRt);
            	numBishops = Rating.bitCount(BBt);
            	numKnights = Rating.bitCount(BNt);
            	numPawns = Rating.bitCount(BPt);
            }else{
            	numQueens = Rating.bitCount(WQt);
            	numRooks = Rating.bitCount(WRt);
            	numBishops = Rating.bitCount(WBt);
            	numKnights = Rating.bitCount(WNt);
            	numPawns = Rating.bitCount(WPt);
            	
            }
            int score = 100-numQueens*9-numRooks*5-(numKnights+numBishops)*3-numPawns;
            if (nextMoves.length()==0){
            	score-=50;
            }
            if (score>bestScore||bestScore==-100){
            	bestScore = score;
            	bestMove = moves.substring(i,i+4);
            }
            else if(score==bestScore){
            	bestMove = bestMove.concat(moves.substring(i,i+4));
            }
        }
		int index=(int)(Math.floor(Math.random()*(bestMove.length()/4))*4);
		System.out.println("info score cp "+bestScore);
		return bestMove.substring(index,index+4);
	}
	public static String Strategy4(String moves){
        /*
         * Always checkmate if possible. Then choose a move to minimize the value of the opponents pieces. Otherwise choose a random move.
         * Also factors in own pieces.
         */
		int bestScore = -100;
        String bestMove = "";
        int start=0,end=0;
        for (int i=0;i<moves.length();i+=4) {
        	//Get the start and end position for checking castling
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
            //Always check if we are breaking the castling rights
            boolean CWKt=Orion.CWK,CWQt=Orion.CWQ,CBKt=Orion.CBK,CBQt=Orion.CBQ;
            if (((1L<<start)&Orion.WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start)&Orion.BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<56))!=0) {CBQt=false;}
            
            //Do the moves
            long EPt=Moves.makeMoveEP(Orion.WP|Orion.BP,moves.substring(i,i+4)),
            WPt=Moves.makeMove(Orion.WP, moves.substring(i,i+4), 'P'),
            WNt=Moves.makeMove(Orion.WN, moves.substring(i,i+4), 'N'),
            WBt=Moves.makeMove(Orion.WB, moves.substring(i,i+4), 'B'),
            WRt=Moves.makeMove(Orion.WR, moves.substring(i,i+4), 'R'),
            WQt=Moves.makeMove(Orion.WQ, moves.substring(i,i+4), 'Q'),
            WKt=Moves.makeMove(Orion.WK, moves.substring(i,i+4), 'K'),
            BPt=Moves.makeMove(Orion.BP, moves.substring(i,i+4), 'p'),
            BNt=Moves.makeMove(Orion.BN, moves.substring(i,i+4), 'n'),
            BBt=Moves.makeMove(Orion.BB, moves.substring(i,i+4), 'b'),
            BRt=Moves.makeMove(Orion.BR, moves.substring(i,i+4), 'r'),
            BQt=Moves.makeMove(Orion.BQ, moves.substring(i,i+4), 'q'),
            BKt=Moves.makeMove(Orion.BK, moves.substring(i,i+4), 'k');
            WRt=Moves.makeMoveCastle(WRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'r');
            boolean WhiteToMovet=!Orion.WhiteToMove;
            String nextMoves = "";
            boolean isChecked;
            if (WhiteToMovet) {
            	nextMoves=Moves.possibleMovesW(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt);
            	isChecked = (WKt&Moves.unsafeForWhite(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt, BKt))!=0;
            } else {
            	nextMoves=Moves.possibleMovesB(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt);
            	isChecked = (BKt&Moves.unsafeForBlack(WPt, WNt, WBt, WRt, WQt, WKt, BPt, BNt, BBt, BRt, BQt, BKt))!=0;
            }
            //If opponent will have no moves, then do that move.
            nextMoves = Moves.filterMoves(nextMoves,WhiteToMovet,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt);
            if (nextMoves.length()==0&&isChecked){
            	System.out.println("info score 100");
            	return moves.substring(i,i+4);
            }
            
            //Count opponents pieces.
            int numQueens,numRooks,numBishops,numKnights,numPawns,numMyQueens,numMyRooks,numMyBishops,numMyKnights,numMyPawns;
            if (Orion.WhiteToMove) {
            	numQueens = Rating.bitCount(BQt);
            	numRooks = Rating.bitCount(BRt);
            	numBishops = Rating.bitCount(BBt);
            	numKnights = Rating.bitCount(BNt);
            	numPawns = Rating.bitCount(BPt);
            	numMyQueens = Rating.bitCount(WQt);
            	numMyRooks = Rating.bitCount(WRt);
            	numMyBishops = Rating.bitCount(WBt);
            	numMyKnights = Rating.bitCount(WNt);
            	numMyPawns = Rating.bitCount(WPt);
            }else{
            	numQueens = Rating.bitCount(WQt);
            	numRooks = Rating.bitCount(WRt);
            	numBishops = Rating.bitCount(WBt);
            	numKnights = Rating.bitCount(WNt);
            	numPawns = Rating.bitCount(WPt);
            	numMyQueens = Rating.bitCount(BQt);
            	numMyRooks = Rating.bitCount(BRt);
            	numMyBishops = Rating.bitCount(BBt);
            	numMyKnights = Rating.bitCount(BNt);
            	numMyPawns = Rating.bitCount(BPt);
            	
            }
            int score = -numQueens*9-numRooks*5-(numKnights+numBishops)*3-numPawns;
            score = score+numMyQueens*9+numMyRooks*5+(numMyKnights+numMyBishops)*3+numMyPawns;
            if (nextMoves.length()==0){
            	score-=50;
            }
            if (score>bestScore||bestScore==-100){
            	bestScore = score;
            	bestMove = moves.substring(i,i+4);
            }
            else if(score==bestScore){
            	bestMove = bestMove.concat(moves.substring(i,i+4));
            }
        }
		int index=(int)(Math.floor(Math.random()*(bestMove.length()/4))*4);
		System.out.println("info score cp "+bestScore);
		return bestMove.substring(index,index+4);
	}
	
	public static String Strategy5(String moves){
        /*
         * Uses principal variation with random rating.
         */
		long startTime = System.currentTimeMillis();
		int bestScore = Integer.MIN_VALUE;
        String bestMove = "";
        int start=0,end=0;
        for (int i=0;i<moves.length();i+=4) {
        	//Get the start and end position for checking castling
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
            //Always check if we are breaking the castling rights
            boolean CWKt=Orion.CWK,CWQt=Orion.CWQ,CBKt=Orion.CBK,CBQt=Orion.CBQ;
            if (((1L<<start)&Orion.WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start)&Orion.BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<56))!=0) {CBQt=false;}
            
            //Do the moves
            long EPt=Moves.makeMoveEP(Orion.WP|Orion.BP,moves.substring(i,i+4)),
            WPt=Moves.makeMove(Orion.WP, moves.substring(i,i+4), 'P'),
            WNt=Moves.makeMove(Orion.WN, moves.substring(i,i+4), 'N'),
            WBt=Moves.makeMove(Orion.WB, moves.substring(i,i+4), 'B'),
            WRt=Moves.makeMove(Orion.WR, moves.substring(i,i+4), 'R'),
            WQt=Moves.makeMove(Orion.WQ, moves.substring(i,i+4), 'Q'),
            WKt=Moves.makeMove(Orion.WK, moves.substring(i,i+4), 'K'),
            BPt=Moves.makeMove(Orion.BP, moves.substring(i,i+4), 'p'),
            BNt=Moves.makeMove(Orion.BN, moves.substring(i,i+4), 'n'),
            BBt=Moves.makeMove(Orion.BB, moves.substring(i,i+4), 'b'),
            BRt=Moves.makeMove(Orion.BR, moves.substring(i,i+4), 'r'),
            BQt=Moves.makeMove(Orion.BQ, moves.substring(i,i+4), 'q'),
            BKt=Moves.makeMove(Orion.BK, moves.substring(i,i+4), 'k');
            WRt=Moves.makeMoveCastle(WRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'r');
            int numPiecesBefore = Rating.bitCount(Orion.WP|Orion.WN|Orion.WB|Orion.WR|Orion.WQ|Orion.WK|Orion.BP|Orion.BN|Orion.BB|Orion.BR|Orion.BQ|Orion.BK);
            int numPiecesAfter = Rating.bitCount(WPt|WNt|WBt|WRt|WQt|WKt|BPt|BNt|BBt|BRt|BQt|BKt);
            int fiftyMoveCountert;
            if ((numPiecesBefore==numPiecesAfter)&&(Orion.WP==WPt)&&(Orion.BP==BPt)){
            	fiftyMoveCountert = Orion.fiftyMoveCounter+1;
            }
            else{
            	fiftyMoveCountert = 0;
            }
            //Score the move
            int scoreOfMove = -PrincipalVariation.pvSearch2(-100000,100000,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!Orion.WhiteToMove,1,Orion.WhiteToMove,fiftyMoveCountert,Orion.moveCounter+1);
            //System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4))+" had a score of :"+scoreOfMove);
            if (scoreOfMove>bestScore){
            	bestScore = scoreOfMove;
            	bestMove = moves.substring(i,i+4);
            }
            else if(scoreOfMove==bestScore){
            	bestMove = bestMove.concat(moves.substring(i,i+4));
            }
        }
        long endTime = System.currentTimeMillis();
        long timeSpent = Math.max(1, (endTime-startTime)/1000);
        long nps = Orion.nodesSearchedCounter/(timeSpent);
        //Choose randomly from the best moves
		int index=(int)(Math.floor(Math.random()*(bestMove.length()/4))*4);
		System.out.println("info score cp "+bestScore+" nodes "+Orion.nodesSearchedCounter +" nps "+nps);
		return bestMove.substring(index,index+4);
	}
	
	public static String Strategy6(String moves){
        /*
         * Uses principal variation with random rating.
         */
		int bestScore = Integer.MIN_VALUE;
        String bestMove = "";
        int start=0,end=0;
        for (int i=0;i<moves.length();i+=4) {
        	String currMove = moves.substring(i, i+4);
        	String returnedValue = PrincipalVariation.alphaBeta(Orion.searchDepth,Integer.MIN_VALUE, Integer.MAX_VALUE,currMove,1,Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove);
        	int scoreOfMove =Integer.parseInt(returnedValue.substring(4));
        	String currMove2 = returnedValue.substring(0,4);
        			
            if (scoreOfMove>bestScore){
            	bestScore = scoreOfMove;
            	bestMove = moves.substring(i,i+4);
            }
            else if(scoreOfMove==bestScore){
            	bestMove = bestMove.concat(moves.substring(i,i+4));
            }
        }
        //Choose randomly from the best moves
		int index=(int)(Math.floor(Math.random()*(bestMove.length()/4))*4);
		System.out.println("info score cp "+bestScore);
		return bestMove.substring(index,index+4);
	}
	
	public static String Strategy7(String moves){
        /*
         * Uses negamax with random rating.
         */
		System.out.println(moves);
		int bestScore = -10000;
        String bestMove = "";
        int start=0,end=0;
        int coefficient = 1;
        if (Orion.searchDepth%2==0){
        	coefficient = -1;
        }
        for (int i=0;i<moves.length();i+=4) {
        	//Get the start and end position for checking castling
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
            //Always check if we are breaking the castling rights
            boolean CWKt=Orion.CWK,CWQt=Orion.CWQ,CBKt=Orion.CBK,CBQt=Orion.CBQ;
            if (((1L<<start)&Orion.WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start)&Orion.BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<56))!=0) {CBQt=false;}
            
            //Do the moves
            long EPt=Moves.makeMoveEP(Orion.WP|Orion.BP,moves.substring(i,i+4)),
            WPt=Moves.makeMove(Orion.WP, moves.substring(i,i+4), 'P'),
            WNt=Moves.makeMove(Orion.WN, moves.substring(i,i+4), 'N'),
            WBt=Moves.makeMove(Orion.WB, moves.substring(i,i+4), 'B'),
            WRt=Moves.makeMove(Orion.WR, moves.substring(i,i+4), 'R'),
            WQt=Moves.makeMove(Orion.WQ, moves.substring(i,i+4), 'Q'),
            WKt=Moves.makeMove(Orion.WK, moves.substring(i,i+4), 'K'),
            BPt=Moves.makeMove(Orion.BP, moves.substring(i,i+4), 'p'),
            BNt=Moves.makeMove(Orion.BN, moves.substring(i,i+4), 'n'),
            BBt=Moves.makeMove(Orion.BB, moves.substring(i,i+4), 'b'),
            BRt=Moves.makeMove(Orion.BR, moves.substring(i,i+4), 'r'),
            BQt=Moves.makeMove(Orion.BQ, moves.substring(i,i+4), 'q'),
            BKt=Moves.makeMove(Orion.BK, moves.substring(i,i+4), 'k');
            WRt=Moves.makeMoveCastle(WRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'r');
            
            //Score the move
            //int scoreOfMove = PrincipalVariation.negaMax(-10000,10000,0,1,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!Orion.WhiteToMove);
            int scoreOfMove = coefficient*PrincipalVariation.negaMax(10000,-10000,1,-1,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!Orion.WhiteToMove);
            System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4))+" had a score of :"+scoreOfMove);
            if (scoreOfMove>bestScore||bestMove.length()==0){
            	bestScore = scoreOfMove;
            	bestMove = moves.substring(i,i+4);
            }
            else if(scoreOfMove==bestScore){
            	bestMove = bestMove.concat(moves.substring(i,i+4));
            }
        }
        //Choose randomly from the best moves
        System.out.println("All best moves: "+bestMove);
		int index=(int)(Math.floor(Math.random()*(bestMove.length()/4))*4);
		System.out.println("info score cp "+bestScore);
		return bestMove.substring(index,index+4);
	}
	

	public static String Strategy8(String moves){
        /*
         * Uses principal variation.
         */
		long startTime = System.currentTimeMillis();
		int bestScore = Integer.MIN_VALUE;
        String bestMove = "";
        int start=0,end=0;
        for (int i=0;i<moves.length();i+=4) {
        	//Get the start and end position for checking castling
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
            //Always check if we are breaking the castling rights
            boolean CWKt=Orion.CWK,CWQt=Orion.CWQ,CBKt=Orion.CBK,CBQt=Orion.CBQ;
            if (((1L<<start)&Orion.WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start)&Orion.BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start)|(1L<<end))&Orion.BR&(1L<<56))!=0) {CBQt=false;}
            
            //Do the moves
            long EPt=Moves.makeMoveEP(Orion.WP|Orion.BP,moves.substring(i,i+4)),
            WPt=Moves.makeMove(Orion.WP, moves.substring(i,i+4), 'P'),
            WNt=Moves.makeMove(Orion.WN, moves.substring(i,i+4), 'N'),
            WBt=Moves.makeMove(Orion.WB, moves.substring(i,i+4), 'B'),
            WRt=Moves.makeMove(Orion.WR, moves.substring(i,i+4), 'R'),
            WQt=Moves.makeMove(Orion.WQ, moves.substring(i,i+4), 'Q'),
            WKt=Moves.makeMove(Orion.WK, moves.substring(i,i+4), 'K'),
            BPt=Moves.makeMove(Orion.BP, moves.substring(i,i+4), 'p'),
            BNt=Moves.makeMove(Orion.BN, moves.substring(i,i+4), 'n'),
            BBt=Moves.makeMove(Orion.BB, moves.substring(i,i+4), 'b'),
            BRt=Moves.makeMove(Orion.BR, moves.substring(i,i+4), 'r'),
            BQt=Moves.makeMove(Orion.BQ, moves.substring(i,i+4), 'q'),
            BKt=Moves.makeMove(Orion.BK, moves.substring(i,i+4), 'k');
            WRt=Moves.makeMoveCastle(WRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, Orion.WK|Orion.BK, moves.substring(i,i+4), 'r');
            int numPiecesBefore = Rating.bitCount(Orion.WP|Orion.WN|Orion.WB|Orion.WR|Orion.WQ|Orion.WK|Orion.BP|Orion.BN|Orion.BB|Orion.BR|Orion.BQ|Orion.BK);
            int numPiecesAfter = Rating.bitCount(WPt|WNt|WBt|WRt|WQt|WKt|BPt|BNt|BBt|BRt|BQt|BKt);
            int fiftyMoveCountert;
            if ((numPiecesBefore==numPiecesAfter)&&(Orion.WP==WPt)&&(Orion.BP==BPt)){
            	fiftyMoveCountert = Orion.fiftyMoveCounter+1;
            }
            else{
            	fiftyMoveCountert = 0;
            }
            //Score the move
            int scoreOfMove = -PrincipalVariation.pvSearch3(-100000,100000,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!Orion.WhiteToMove,1,Orion.WhiteToMove,fiftyMoveCountert,Orion.moveCounter+1);
            //System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4))+"* had a score of :"+scoreOfMove);
            if (scoreOfMove>bestScore){
            	bestScore = scoreOfMove;
            	bestMove = moves.substring(i,i+4);
            }
            else if(scoreOfMove==bestScore){
            	bestMove = bestMove.concat(moves.substring(i,i+4));
            }
        }
        long endTime = System.currentTimeMillis();
        long timeSpent = Math.max((endTime-startTime), 1);
        long nps = 1000*Orion.nodesSearchedCounter/timeSpent;
        //Choose randomly from the best moves
		int index=(int)(Math.floor(Math.random()*(bestMove.length()/4))*4);
		String infoString = "info depth "+Orion.searchDepth;
		infoString  = infoString /*+" time " + (endTime-startTime) */+ " score cp "+bestScore;
		if (Math.abs(Math.abs(bestScore)-Orion.MATE_SCORE)<=Orion.searchDepth){
			int myInt = (bestScore>0) ? 1 : -1;
			int mateMoves = myInt*(1+Orion.MATE_SCORE-Math.abs(bestScore))/2;
			infoString  = infoString +" mate "+ mateMoves;
		}
		infoString  = infoString +" nodes "+Orion.nodesSearchedCounter+" nps "+nps;
		
		System.out.println(infoString);
		return bestMove.substring(index,index+4);
	}
	public static void Strategy9(){
        /*
         * Uses principal variation.
         */
		Orion.nodesSearchedCounter=0;
		long startTime = System.currentTimeMillis();
		
		int bestScore = PrincipalVariation.pvSearch5(-100000,100000,Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove,Orion.searchDepth,Orion.WhiteToMove,Orion.fiftyMoveCounter,Orion.moveCounter);
		//int bestScore = PrincipalVariation.pvSearch6(-100000,100000,Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteHasCastled,Orion.BlackHasCastled,Orion.WhiteToMove,Orion.searchDepth,Orion.WhiteToMove,Orion.fiftyMoveCounter,Orion.moveCounter);
        
		long endTime = System.currentTimeMillis();
        long timeSpent = Math.max((endTime-startTime), 1);
        long nps = 1000*Orion.nodesSearchedCounter/timeSpent;
        //Choose randomly from the best moves
		System.out.println("bestScore:"+bestScore);
		String infoString = "info depth "+Orion.searchDepth;
		infoString  = infoString +" time " + (endTime-startTime) + " score";
		if (Math.abs(Math.abs(bestScore)-Orion.MATE_SCORE)<=Orion.searchDepth){
			int myInt = (bestScore>0) ? 1 : -1;
			int mateMoves = myInt*(1+(Orion.searchDepth - Math.abs(Orion.MATE_SCORE-Math.abs(bestScore))))/2;
			infoString  = infoString +" mate "+ mateMoves;
		}
		else{
			 infoString = infoString + " cp "+bestScore;
		}
		infoString  = infoString +" nodes "+Orion.nodesSearchedCounter+" nps "+nps;
		
		System.out.println(infoString);
		System.out.println("bestmove "+bestMove);
		return;
	}
	
}
