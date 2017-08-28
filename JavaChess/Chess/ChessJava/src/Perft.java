
public class Perft {
    public static String moveToAlgebra(String move)
    {
        String moveString="";
        moveString+=""+(char)(move.charAt(0)+49);
        moveString+=""+(char)(move.charAt(1)+1);
        moveString+=""+(char)(move.charAt(2)+49);
        moveString+=""+(char)(move.charAt(3)+1);
        return moveString;
    }

    static long perftTotalMoveCounter = 0;
    static long perftMoveCounter=0;
    static int perftMaxDepth=1;
    
    
    public static void perftRoot(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int depth,boolean shouldPrint)
    {
    	
    	perftMoveCounter=0;
    	perftTotalMoveCounter = 0;
    	long startTime = System.currentTimeMillis();
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        for (int i=0;i<moves.length();i+=4) {
            long WPt=Moves.makeMove(WP, moves.substring(i,i+4), 'P'), WNt=Moves.makeMove(WN, moves.substring(i,i+4), 'N'),
                    WBt=Moves.makeMove(WB, moves.substring(i,i+4), 'B'), WRt=Moves.makeMove(WR, moves.substring(i,i+4), 'R'),
                    WQt=Moves.makeMove(WQ, moves.substring(i,i+4), 'Q'), WKt=Moves.makeMove(WK, moves.substring(i,i+4), 'K'),
                    BPt=Moves.makeMove(BP, moves.substring(i,i+4), 'p'), BNt=Moves.makeMove(BN, moves.substring(i,i+4), 'n'),
                    BBt=Moves.makeMove(BB, moves.substring(i,i+4), 'b'), BRt=Moves.makeMove(BR, moves.substring(i,i+4), 'r'),
                    BQt=Moves.makeMove(BQ, moves.substring(i,i+4), 'q'), BKt=Moves.makeMove(BK, moves.substring(i,i+4), 'k'),
                    EPt=Moves.makeMoveEP(WP|BP,moves.substring(i,i+4));
            WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(i,i+4), 'r');
            boolean CWKt=CWK,CWQt=CWQ,CBKt=CBK,CBQt=CBQ;
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
            if (((WKt&Moves.unsafeForWhite(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt))==0 && WhiteToMove) ||
                    ((BKt&Moves.unsafeForBlack(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt))==0 && !WhiteToMove)) {
                perft(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1);
                if(shouldPrint){
                	System.out.println(moveToAlgebra(moves.substring(i,i+4))+" "+perftMoveCounter);
                }
                perftTotalMoveCounter+=perftMoveCounter;
                perftMoveCounter=0;
            }
        }
        if(shouldPrint){
	        System.out.println("Total: " + perftTotalMoveCounter);
	        long endTime = System.currentTimeMillis();
	        double duration = (endTime - startTime)/1000.0;
	        long movesPerSec = (long) (perftTotalMoveCounter/duration);
	        System.out.println("Generated "+movesPerSec+" moves per second");
        }
    }
    
    public static void perft(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int depth)
    {
        if (depth<perftMaxDepth) {
            String moves;
            //Get the moves for the color whose turn it is
            if (WhiteToMove) {
                moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
            } else {
                moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
            }
            //System.out.println(moves);
            //String filteredMoves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, depth);
        	//System.out.println(filteredMoves.length()/4);
            /*String renamedFilteredMoves = "";
            for (int i=0;i<filteredMoves.length();i+=4) {
            	renamedFilteredMoves = renamedFilteredMoves + algebraToMove(filteredMoves.substring(i,i+4)) +"," ;
            }
            renamedFilteredMoves = renamedFilteredMoves.substring(0, renamedFilteredMoves.length()-1);
            System.out.println(renamedFilteredMoves);
            */
            
            //Make the move
            for (int i=0;i<moves.length();i+=4) {
            	//System.out.println(moves.substring(i, i+4));
                long WPt=Moves.makeMove(WP, moves.substring(i,i+4), 'P'), WNt=Moves.makeMove(WN, moves.substring(i,i+4), 'N'),
                        WBt=Moves.makeMove(WB, moves.substring(i,i+4), 'B'), WRt=Moves.makeMove(WR, moves.substring(i,i+4), 'R'),
                        WQt=Moves.makeMove(WQ, moves.substring(i,i+4), 'Q'), WKt=Moves.makeMove(WK, moves.substring(i,i+4), 'K'),
                        BPt=Moves.makeMove(BP, moves.substring(i,i+4), 'p'), BNt=Moves.makeMove(BN, moves.substring(i,i+4), 'n'),
                        BBt=Moves.makeMove(BB, moves.substring(i,i+4), 'b'), BRt=Moves.makeMove(BR, moves.substring(i,i+4), 'r'),
                        BQt=Moves.makeMove(BQ, moves.substring(i,i+4), 'q'), BKt=Moves.makeMove(BK, moves.substring(i,i+4), 'k'),
                        EPt=Moves.makeMoveEP(WP|BP,moves.substring(i,i+4));
                WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(i,i+4), 'R');
                BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(i,i+4), 'r');
                boolean CWKt=CWK,CWQt=CWQ,CBKt=CBK,CBQt=CBQ;
                if (Character.isDigit(moves.charAt(3))) {//'regular' move
                    int start=(Character.getNumericValue(moves.charAt(i)))+(Character.getNumericValue(moves.charAt(i+1))*8);
                    if (((1L<<start)&WK)!=0) {CWKt=false; CWQt=false;}
                    if (((1L<<start)&BK)!=0) {CBKt=false; CBQt=false;}
                    if (((1L<<start)&WR&(1L<<7))!=0) {CWKt=false;}
                    if (((1L<<start)&WR&(1L))!=0) {CWQt=false;}
                    if (((1L<<start)&BR&(1L<<63))!=0) {CBKt=false;}
                    if (((1L<<start)&BR&(1L<<56))!=0) {CBQt=false;}
                }
                if (((WKt&Moves.unsafeForWhite(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt))==0 && WhiteToMove) ||
                        ((BKt&Moves.unsafeForBlack(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt))==0 && !WhiteToMove)) {
                    
                    //else{System.out.println("Move count for "+algebraToMove(moves.substring(i, i+4))+":");}
                    //long[] givenBoardInformation = {WKt,WQt,WBt,WNt,WRt,WPt,BKt,BQt,BBt,BNt,BRt,BPt};
                    //Chessboard tempBoard = new Chessboard(givenBoardInformation);
                    //System.out.println(tempBoard);
                    
                    perft(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1);
                }

            }
        }
        else{perftMoveCounter++;}
    }
}
