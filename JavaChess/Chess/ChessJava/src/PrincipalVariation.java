import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

public class PrincipalVariation {
    public static int zWSearch(int beta,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int depth) {//fail-hard zero window search, returns either beta-1 or beta
        int score = Integer.MIN_VALUE;
        //alpha == beta - 1
        //this is either a cut- or all-node
        if (depth >= Orion.searchDepth)
        {
            score = Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
            return score;
        }
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        //sortMoves();
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
                score = -zWSearch(1 - beta,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1);
            }
            if (score >= beta)
            {
                return score;//fail-hard beta-cutoff
            }
        }
        return beta - 1;//fail-hard, return alpha
    }
    public static int getFirstLegalMove(String moves,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove) {
        for (int i=0;i<moves.length();i+=4) {
            long WPt=Moves.makeMove(WP, moves.substring(i,i+4), 'P'), WNt=Moves.makeMove(WN, moves.substring(i,i+4), 'N'),
                    WBt=Moves.makeMove(WB, moves.substring(i,i+4), 'B'), WRt=Moves.makeMove(WR, moves.substring(i,i+4), 'R'),
                    WQt=Moves.makeMove(WQ, moves.substring(i,i+4), 'Q'), WKt=Moves.makeMove(WK, moves.substring(i,i+4), 'K'),
                    BPt=Moves.makeMove(BP, moves.substring(i,i+4), 'p'), BNt=Moves.makeMove(BN, moves.substring(i,i+4), 'n'),
                    BBt=Moves.makeMove(BB, moves.substring(i,i+4), 'b'), BRt=Moves.makeMove(BR, moves.substring(i,i+4), 'r'),
                    BQt=Moves.makeMove(BQ, moves.substring(i,i+4), 'q'), BKt=Moves.makeMove(BK, moves.substring(i,i+4), 'k');
            WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(i,i+4), 'r');
            if (((WKt&Moves.unsafeForWhite(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt))==0 && WhiteToMove) ||
                    ((BKt&Moves.unsafeForBlack(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt))==0 && !WhiteToMove)) {
                return i;
            }
        }
        return -1;
    }
    public static int pvSearch(int alpha,int beta,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int depth,boolean selfColor) {//using fail soft with negamax
        int bestScore;
        int bestMoveIndex = -1;
        if (depth >= Orion.searchDepth)
        {
            bestScore = Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
            return bestScore;
        }
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        //sortMoves();
        int firstLegalMove = getFirstLegalMove(moves,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
        if (firstLegalMove == -1)
        {
        	boolean unsafe;
        	if (WhiteToMove){
        		unsafe = (WK&Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        	}
        	else{
        		unsafe = (BK&Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        	}
        	//Note: Scores are opposite of what would be expected because we are collecting the negative of pvs
        	if ((WhiteToMove==selfColor)&&unsafe){
        		//Checkmate on me
        		return Orion.MATE_SCORE;
        	}
        	else if ((WhiteToMove==selfColor)&& !unsafe){
        		//Avoid Stalemate
        		return -Orion.MATE_SCORE/2;
        	}
        	else if((WhiteToMove!=selfColor)&& !unsafe){
        		//Avoid Stalemate
        		return Orion.MATE_SCORE/2;
        	}
        	else{
        		//Checkmate on Opponent
        		return -Orion.MATE_SCORE;
        	}
            //return WhiteToMove ? Orion.MATE_SCORE : -Orion.MATE_SCORE;
        }
        long WPt=Moves.makeMove(WP, moves.substring(firstLegalMove,firstLegalMove+4), 'P'), WNt=Moves.makeMove(WN, moves.substring(firstLegalMove,firstLegalMove+4), 'N'),
                WBt=Moves.makeMove(WB, moves.substring(firstLegalMove,firstLegalMove+4), 'B'), WRt=Moves.makeMove(WR, moves.substring(firstLegalMove,firstLegalMove+4), 'R'),
                WQt=Moves.makeMove(WQ, moves.substring(firstLegalMove,firstLegalMove+4), 'Q'), WKt=Moves.makeMove(WK, moves.substring(firstLegalMove,firstLegalMove+4), 'K'),
                BPt=Moves.makeMove(BP, moves.substring(firstLegalMove,firstLegalMove+4), 'p'), BNt=Moves.makeMove(BN, moves.substring(firstLegalMove,firstLegalMove+4), 'n'),
                BBt=Moves.makeMove(BB, moves.substring(firstLegalMove,firstLegalMove+4), 'b'), BRt=Moves.makeMove(BR, moves.substring(firstLegalMove,firstLegalMove+4), 'r'),
                BQt=Moves.makeMove(BQ, moves.substring(firstLegalMove,firstLegalMove+4), 'q'), BKt=Moves.makeMove(BK, moves.substring(firstLegalMove,firstLegalMove+4), 'k'),
                EPt=Moves.makeMoveEP(WP|BP,moves.substring(firstLegalMove,firstLegalMove+4));
        WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(firstLegalMove,firstLegalMove+4), 'R');
        BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(firstLegalMove,firstLegalMove+4), 'r');
        boolean CWKt=CWK,CWQt=CWQ,CBKt=CBK,CBQt=CBQ;
        int start=0,end=0;
        if (Character.isDigit(moves.charAt(firstLegalMove+3))) {//'regular' move
            start=(Character.getNumericValue(moves.charAt(firstLegalMove)))+(Character.getNumericValue(moves.charAt(firstLegalMove+1))*8);
            end=(Character.getNumericValue(moves.charAt(firstLegalMove+2)))+(Character.getNumericValue(moves.charAt(firstLegalMove+3))*8);;
        } else if (moves.charAt(firstLegalMove+3)=='P') {//pawn promotion
            if (Character.isUpperCase(moves.charAt(firstLegalMove+2))) {
                start=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(firstLegalMove+0)-'0']&Moves.RankMasks8[6]);
                end=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(firstLegalMove+1)-'0']&Moves.RankMasks8[7]);
            } else {
                start=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(firstLegalMove+0)-'0']&Moves.RankMasks8[1]);
                end=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(firstLegalMove+1)-'0']&Moves.RankMasks8[0]);
            }
        } else if (moves.charAt(firstLegalMove+3)=='E') {//en passant
            if (moves.charAt(firstLegalMove+2)=='W') {
                start=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(firstLegalMove+0)-'0']&Moves.RankMasks8[4]);
                end=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(firstLegalMove+1)-'0']&Moves.RankMasks8[5]);
            } else {
                start=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(firstLegalMove+0)-'0']&Moves.RankMasks8[3]);
                end=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(firstLegalMove+1)-'0']&Moves.RankMasks8[2]);
            }
        }
        //Always check if we are breaking the castling
        if (((1L<<start)&WK)!=0) {CWKt=false; CWQt=false;}
        if (((1L<<start)&BK)!=0) {CBKt=false; CBQt=false;}
        if ((((1L<<start)|(1L<<end))&WR&(1L<<7))!=0) {CWKt=false;}
        if ((((1L<<start)|(1L<<end))&WR&(1L))!=0) {CWQt=false;}
        if ((((1L<<start)|(1L<<end))&BR&(1L<<63))!=0) {CBKt=false;}
        if ((((1L<<start)|(1L<<end))&BR&(1L<<56))!=0) {CBQt=false;}
        
        bestScore = -pvSearch(-beta,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1,selfColor);
        //System.out.println("Evaluation gave a score of: "+bestScore);
        //System.out.println("mark 1 --- alpha: "+alpha+", beta: "+beta);
        
        Orion.nodesSearchedCounter++;
        if (Math.abs(bestScore) == Orion.MATE_SCORE)
        {
            return bestScore;
        }
        if (bestScore > alpha)
        {
            if (bestScore >= beta)
            {
                //This is a refutation move
                //It is not a PV move
                //However, it will usually cause a cutoff so it can
                //be considered a best move if no other move is found
                //System.out.println("returning best score --- alpha: "+alpha+", beta: "+beta);
                return bestScore;
            }
            alpha = bestScore;
        }
        //System.out.println("mark 2 --- alpha: "+alpha+", beta: "+beta);
        bestMoveIndex = firstLegalMove;
        for (int i=firstLegalMove+4;i<moves.length();i+=4) {
            int score;
            Orion.nodesSearchedCounter++;
            //legal, non-castle move
            WPt=Moves.makeMove(WP, moves.substring(i,i+4), 'P');
            WNt=Moves.makeMove(WN, moves.substring(i,i+4), 'N');
            WBt=Moves.makeMove(WB, moves.substring(i,i+4), 'B');
            WRt=Moves.makeMove(WR, moves.substring(i,i+4), 'R');
            WQt=Moves.makeMove(WQ, moves.substring(i,i+4), 'Q');
            WKt=Moves.makeMove(WK, moves.substring(i,i+4), 'K');
            BPt=Moves.makeMove(BP, moves.substring(i,i+4), 'p');
            BNt=Moves.makeMove(BN, moves.substring(i,i+4), 'n');
            BBt=Moves.makeMove(BB, moves.substring(i,i+4), 'b');
            BRt=Moves.makeMove(BR, moves.substring(i,i+4), 'r');
            BQt=Moves.makeMove(BQ, moves.substring(i,i+4), 'q');
            BKt=Moves.makeMove(BK, moves.substring(i,i+4), 'k');
            EPt=Moves.makeMoveEP(WP|BP,moves.substring(i,i+4));
            WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(i,i+4), 'r');
            CWKt=CWK;
            CWQt=CWQ;
            CBKt=CBK;
            CBQt=CBQ;
            int start2=0,end2=0;
            if (Character.isDigit(moves.charAt(i+3))) {//'regular' move
                start2=(Character.getNumericValue(moves.charAt(i)))+(Character.getNumericValue(moves.charAt(i+1))*8);
                end2=(Character.getNumericValue(moves.charAt(i+2)))+(Character.getNumericValue(moves.charAt(i+3))*8);;
            } else if (moves.charAt(i+3)=='P') {//pawn promotion
                if (Character.isUpperCase(moves.charAt(i+2))) {
                    start2=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+0)-'0']&Moves.RankMasks8[6]);
                    end2=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+1)-'0']&Moves.RankMasks8[7]);
                } else {
                    start2=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+0)-'0']&Moves.RankMasks8[1]);
                    end2=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+1)-'0']&Moves.RankMasks8[0]);
                }
            } else if (moves.charAt(i+3)=='E') {//en passant
                if (moves.charAt(i+2)=='W') {
                    start2=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+0)-'0']&Moves.RankMasks8[4]);
                    end2=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+1)-'0']&Moves.RankMasks8[5]);
                } else {
                    start2=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+0)-'0']&Moves.RankMasks8[3]);
                    end2=Long.numberOfTrailingZeros(Moves.FileMasks8[moves.charAt(i+1)-'0']&Moves.RankMasks8[2]);
                }
            }
            //Always check if we are breaking the castling
            if (((1L<<start2)&WK)!=0) {CWKt=false; CWQt=false;}
            if (((1L<<start2)&BK)!=0) {CBKt=false; CBQt=false;}
            if ((((1L<<start2)|(1L<<end2))&WR&(1L<<7))!=0) {CWKt=false;}
            if ((((1L<<start2)|(1L<<end2))&WR&(1L))!=0) {CWQt=false;}
            if ((((1L<<start2)|(1L<<end2))&BR&(1L<<63))!=0) {CBKt=false;}
            if ((((1L<<start2)|(1L<<end2))&BR&(1L<<56))!=0) {CBQt=false;}
            score = -zWSearch(-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1);
            if ((score > alpha) && (score < beta))
            {
                //research with window [alpha;beta]
                bestScore = -pvSearch(-beta,-alpha,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,!WhiteToMove,depth+1,selfColor);
                //TODO change the score to bestScore
                if (score>alpha)
                {
                	//TODO change the score to bestScore
                    bestMoveIndex = i;
                    alpha = score;
                }
            }
            if ((score != Orion.NULL_INT) && (score > bestScore))
            {
                if (score >= beta)
                {
                    return score;
                }
                bestScore = score;
                if (Math.abs(bestScore) == Orion.MATE_SCORE)
                {
                    return bestScore;
                }
            }
        }
        return bestScore;
    }

    public static String alphaBeta(int depth, int alpha, int beta, String move,int player,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ, boolean WhiteToMove) {
        //return in the form of 1234b##########
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        if (depth==0 || moves.length()==0) {
        	return move+(Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove)*(player*2-1));}
        
        //sort later
        boolean WhiteToMovet = !WhiteToMove;
        player=1-player;//either 1 or 0
        
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
            String returnString=alphaBeta(depth-1,alpha,beta, moves.substring(i,i+4),player,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,WhiteToMovet);
            int value=Integer.valueOf(returnString.substring(4));
            if (player==0) {
                if (value<=beta) {beta=value; if (depth==Orion.searchDepth) {move=returnString.substring(0,4);}}
            } else {
                if (value>alpha) {alpha=value; if (depth==Orion.searchDepth) {move=returnString.substring(0,4);}}
            }
            if (alpha>=beta) {
                if (player==0) {return move+beta;} else {return move+alpha;}
            }
        }
        if (player==0) {return move+beta;} else {return move+alpha;}
    }
    
    public static int negaMax(int alpha,int beta,int depth,int player,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove) {//using fail soft with negamax
        int bestScore;
        if (depth == Orion.searchDepth)
        {
            bestScore = player*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
            return bestScore;
        }
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        
        if (moves.length()==0)
        {
        	//TODO differentiate checkmate and stalemate
            bestScore = player*Orion.MATE_SCORE;
            return bestScore;
        }
        //sortMoves();
        bestScore = -10000;
        for (int i=0;i<moves.length();i+=4) {
            int score;
            Orion.nodesSearchedCounter++;
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
            
            score = -negaMax(-beta,-alpha,depth+1,-player,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove);
            bestScore = Math.max(bestScore, score);
            alpha = Math.max(alpha, score);
            if (alpha>=beta){
            	break;
            }
        }
        
        return bestScore;
    }
    
    public static int pvSearch2(int alpha,int beta,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int depth,boolean selfColor,int fiftyMoveCounter,int moveCounter) {//using fail soft with negamax
    	Orion.nodesSearchedCounter++;
    	String fenBoard = BoardGeneration.makeHistoryFEN(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,fiftyMoveCounter,moveCounter);
        //Orion.HISTORY.add(fenBoard);
        if (Orion.ThreeMoveRep.containsKey(fenBoard)){
        	Orion.ThreeMoveRep.put(fenBoard, Orion.ThreeMoveRep.get(fenBoard)+1);
        }
        else{
        	Orion.ThreeMoveRep.put(fenBoard, 1);
        }
        if (fiftyMoveCounter==48||Orion.ThreeMoveRep.get(fenBoard)>=2){
    		//Stalemate 3 fold repetition
        	//Orion.HISTORY.remove(Orion.HISTORY.size()-1);
        	Orion.ThreeMoveRep.put(fenBoard, Orion.ThreeMoveRep.get(fenBoard)-1);
        	return Orion.MATE_SCORE/2;
        }
    	int bestScore;
        //int myInt = (selfColor==WhiteToMove) ? 1 : -1;
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);
        
        if (moves.length() == 0)
        {
        	
        	boolean unsafeMe;
        	if (WhiteToMove){
        		unsafeMe = (WK&Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        		
        	}
        	else{
        		unsafeMe = (BK&Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        	}
        	//Note: Scores are opposite of what would be expected because we are collecting the negative of pvs
        	if (unsafeMe){
        		//Checkmate
        		//Orion.HISTORY.remove(Orion.HISTORY.size()-1);
        		Orion.ThreeMoveRep.put(fenBoard, Orion.ThreeMoveRep.get(fenBoard)-1);
        		return -Orion.MATE_SCORE;
        	}
        	else{
        		//Stalemate
        		//Orion.HISTORY.remove(Orion.HISTORY.size()-1);
        		Orion.ThreeMoveRep.put(fenBoard, Orion.ThreeMoveRep.get(fenBoard)-1);
        		return Orion.MATE_SCORE/2;
        	}
        	/*
        	else if(!unsafeMe&&!unsafeThem){
        		//Avoid Stalemate
        		return -Orion.MATE_SCORE/2;
        	}
        	else{
        		//Checkmate on Opponent
        		return Orion.MATE_SCORE;
        	}*/
            //return WhiteToMove ? Orion.MATE_SCORE : -Orion.MATE_SCORE;
        }
        if (depth >= Orion.searchDepth)
        {
        	bestScore = Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
        	//bestScore = myInt*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
        	//System.out.println("bestScore: "+bestScore);
        	//Orion.HISTORY.remove(Orion.HISTORY.size()-1);
        	Orion.ThreeMoveRep.put(fenBoard, Orion.ThreeMoveRep.get(fenBoard)-1);
            return bestScore;
        }
        
        //sortMoves();
        
        for (int i=0;i<moves.length();i+=4) {
            int score;
            //legal, non-castle move
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
            
            int numPiecesBefore = Rating.bitCount(WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK);
            int numPiecesAfter = Rating.bitCount(WPt|WNt|WBt|WRt|WQt|WKt|BPt|BNt|BBt|BRt|BQt|BKt);
            int fiftyMoveCountert;
            if ((numPiecesBefore==numPiecesAfter)&&(WP==WPt)&&(BP==BPt)){
            	fiftyMoveCountert = fiftyMoveCounter+1;
            }
            else{
            	fiftyMoveCountert = 0;
            }
            
            if (i!=0){
            	score = -pvSearch2(-alpha-1,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1,selfColor,fiftyMoveCountert,moveCounter+1);
            	if (score>alpha && score<beta){
            		score = -pvSearch2(-beta,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1,selfColor,fiftyMoveCountert,moveCounter+1);
            	}
            }
            else{
            	score = -pvSearch2(-beta,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1,selfColor,fiftyMoveCountert,moveCounter+1);
            }
            alpha = Math.max(alpha, score);
            if (alpha>=beta){
            	break;
            }
        }
        //Orion.HISTORY.remove(Orion.HISTORY.size()-1);
        Orion.ThreeMoveRep.put(fenBoard, Orion.ThreeMoveRep.get(fenBoard)-1);
        return alpha;
    }
    
    public static int pvSearch3(int alpha,int beta,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int depth,boolean selfColorIsWhite,int fiftyMoveCounter,int moveCounter) {//using fail soft with negamax
    	Orion.nodesSearchedCounter++;
        Long boardHash = Zobrist.getZobristHash(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
        
        if (fiftyMoveCounter==48||(Orion.ThreeMoveRepCheck.containsKey(boardHash)&&Orion.ThreeMoveRepCheck.get(boardHash)>=1)){
    		//Stalemate 3 fold repetition
        	return Orion.MATE_SCORE/2;
        }
        
    	int bestScore;
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);

        if (moves.length() == 0)
        {
        	
        	boolean unsafeMe;
        	if (WhiteToMove){
        		unsafeMe = (WK&Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        		
        	}
        	else{
        		unsafeMe = (BK&Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        	}
        	//int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;
        	//Note: Scores are opposite of what would be expected because we are collecting the negative of pvs
        	if (unsafeMe){
        		//Checkmate
        		return -(Orion.MATE_SCORE-depth);//*myInt; //subtracted depth so moves that lead to checkmate faster are chosen
        	}
        	else{
        		//Stalemate
        		return -(depth-Orion.MATE_SCORE/2);//*myInt;
        	}

            //return WhiteToMove ? Orion.MATE_SCORE : -Orion.MATE_SCORE;
        }
        
        if (depth >= Orion.searchDepth)
        {
        	int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;
        	//bestScore = Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        	bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        	//System.out.println("bestScore: "+bestScore);

            return bestScore;
        }
        
        //sortMoves();
        moves = Rating.sortMoves(moves,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        
        //Update the hashmap that checks for three fold repetition
        if (Orion.ThreeMoveRepCheck.containsKey(boardHash)){
        	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)+1);
        }
        else{
        	Orion.ThreeMoveRepCheck.put(boardHash, 1);
        }
        
        for (int i=0;i<moves.length();i+=4) {
            int score;
            //legal, non-castle move
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
            
            int numPiecesBefore = Rating.bitCount(WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK);
            int numPiecesAfter = Rating.bitCount(WPt|WNt|WBt|WRt|WQt|WKt|BPt|BNt|BBt|BRt|BQt|BKt);
            int fiftyMoveCountert;
            if ((numPiecesBefore==numPiecesAfter)&&(WP==WPt)&&(BP==BPt)){
            	fiftyMoveCountert = fiftyMoveCounter+1;
            }
            else{
            	fiftyMoveCountert = 0;
            }

            
            if (i!=0){
            	score = -pvSearch3(-alpha-1,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            	if (score>alpha && score<beta){
            		score = -pvSearch3(-beta,-score,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            	}
            }
            else{
            	score = -pvSearch3(-beta,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth+1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            }

            //System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4))+" had a score of :"+score);
            alpha = Math.max(alpha, score);
            if (alpha>=beta){
            	break;
            }
        }
        //Remove the value from the 3 fold repetition checker
    	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)-1);
        return alpha;
    }
    
    public static int pvSearch4(int alpha,int beta,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int depth,boolean selfColorIsWhite,int fiftyMoveCounter,int moveCounter) {//using fail soft with negamax
    	/*
    	 * includes the first move in the alpha beta pruning process and speeds things up 2-4x compared to pvSearch3
    	 */
    	Orion.nodesSearchedCounter++;
        Long boardHash = Zobrist.getZobristHash(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
        int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;
        if (fiftyMoveCounter==48||(Orion.ThreeMoveRepCheck.containsKey(boardHash)&&Orion.ThreeMoveRepCheck.get(boardHash)>=2)){
    		//Stalemate 3 fold repetition
        	//return myInt*(-Orion.MATE_SCORE/2);
        	return depth+Orion.MATE_SCORE/2;
        }
        
    	int bestScore;
    	String bestMoves = "";
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);

        if (moves.length() == 0)
        {
        	boolean unsafeMe;
        	if (WhiteToMove){
        		unsafeMe = (WK&Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        		
        	}
        	else{
        		unsafeMe = (BK&Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        	}
        	//int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;
        	//Note: Scores are opposite of what would be expected because we are collecting the negative of pvs
        	if (unsafeMe){
        		//Checkmate
        		return -(Orion.MATE_SCORE+depth);//*myInt; //subtracted depth so moves that lead to checkmate faster are chosen
        	}
        	else{
        		//Stalemate
        		return -(-depth-Orion.MATE_SCORE/2);//*myInt;
        	}

            //return WhiteToMove ? Orion.MATE_SCORE : -Orion.MATE_SCORE;
        }
        
        if (depth == 0)
        {
        	bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        	//bestScore = myInt*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,selfColorIsWhite);
            return bestScore;
        }
        
        //sortMoves();
        moves = Rating.sortMoves(moves,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        
        //Update the hashmap that checks for three fold repetition
        if (Orion.ThreeMoveRepCheck.containsKey(boardHash)){
        	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)+1);
        }
        else{
        	Orion.ThreeMoveRepCheck.put(boardHash, 1);
        }
        
        for (int i=0;i<moves.length();i+=4) {
            int score;
            //legal, non-castle move
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
            
            int numPiecesBefore = Rating.bitCount(WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK);
            int numPiecesAfter = Rating.bitCount(WPt|WNt|WBt|WRt|WQt|WKt|BPt|BNt|BBt|BRt|BQt|BKt);
            int fiftyMoveCountert;
            if ((numPiecesBefore==numPiecesAfter)&&(WP==WPt)&&(BP==BPt)){
            	fiftyMoveCountert = fiftyMoveCounter+1;
            }
            else{
            	fiftyMoveCountert = 0;
            }

            //System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4)));
            if (i!=0){
            	score = -pvSearch4(-alpha-1,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            	if (score>alpha && score<beta){
            		score = -pvSearch4(-beta,-score,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            	}
            }
            else{
            	score = -pvSearch4(-beta,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            }
            /*if (depth==Orion.searchDepth){
            	System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4))+" had a score of :"+score);
            	//System.out.println("alpha:"+alpha+", beta"+beta);
            }*/
            
            //alpha = Math.max(alpha, score);
            if (score>alpha||i==0){
            	alpha=score;
            	bestMoves=moves.substring(i, i+4);
            }
            else if(score==alpha){
            	bestMoves+=moves.substring(i, i+4);
            }
            if (alpha>=beta){
            	break;
            }
        }
        //Remove the value from the 3 fold repetition checker
    	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)-1);
    	//If we have found the best Move
    	if (depth==Orion.searchDepth){
    		//System.out.println(bestMoves);
    		int index=(int)(Math.floor(Math.random()*(bestMoves.length()/4))*4);
    		Strategies.bestMove = UCI.moveToAlgebra(bestMoves.substring(index, index+4));
    		//System.out.println("bestmove "+UCI.moveToAlgebra(bestMoves.substring(index, index+4)));
    	}
        return alpha;
    }

    public static int pvSearch5(int alpha,int beta,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int depth,boolean selfColorIsWhite,int fiftyMoveCounter,int moveCounter) {//using fail soft with negamax
    	/*
    	 * Includes the first move in the alpha beta pruning process and speeds things up 2-4x compared to pvSearch3
    	 * Incorporates transposition tables.
    	 */
    	
    	Orion.nodesSearchedCounter++;
        Long boardHash = Zobrist.getZobristHash(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
        
        //Transposition Table Look-Up
        int alphaOrig = alpha;
        if (TranspositionTable.contains(boardHash)&&TranspositionTable.getDepth(boardHash)>=depth){
        	if ("EXACT".equals(TranspositionTable.getFlag(boardHash))){
        		
        	}
        	else if ("LOWERBOUND".equals(TranspositionTable.getFlag(boardHash))){
        		alpha = Math.max(alpha, TranspositionTable.getValue(boardHash));
        	}
        	else if("UPPERBOUND".equals(TranspositionTable.getFlag(boardHash))){
        		beta = Math.min(beta, TranspositionTable.getValue(boardHash));
        	}
        	if (alpha>=beta){
        		//System.out.println("Transposition return");
        		return TranspositionTable.getValue(boardHash);
        	}
        }
        
        int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;
        if ((!(Orion.searchDepth==depth))&&(fiftyMoveCounter==48||(Orion.ThreeMoveRepCheck.containsKey(boardHash)&&Orion.ThreeMoveRepCheck.get(boardHash)>=2))){
    		//Stalemate 3 fold repetition
        	//return myInt*(-Orion.MATE_SCORE/2);
        	//System.out.println("50move or 3rep return");
        	int bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        	//int bestScore = myInt*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,selfColorIsWhite);
        	//System.out.println(bestScore);
        	if (bestScore>=550){
        		//stalemate good
        		//System.out.println("Stalemate Good");
        		return -(depth+Orion.MATE_SCORE/2);
        	}
        	else{
        		//stalemate bad
        		//System.out.println("Stalemate Bad");
        		return (depth+Orion.MATE_SCORE/2);
        	}
        }
        
    	int bestScore;
    	String bestMoves = "";
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);

        if (moves.length() == 0)
        {
        	boolean unsafeMe;
        	if (WhiteToMove){
        		unsafeMe = (WK&Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        		
        	}
        	else{
        		unsafeMe = (BK&Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        	}
        	//int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;
        	//Note: Scores are opposite of what would be expected because we are collecting the negative of pvs
        	//System.out.println("no moves return");
        	if (unsafeMe){
        		//Checkmate
        		//System.out.println("Mate Found");
        		return -(Orion.MATE_SCORE+depth);//*myInt; //subtracted depth so moves that lead to checkmate faster are chosen
        	}
        	else{
        		//Stalemate
        		bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        		//bestScore = myInt*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,selfColorIsWhite);
        		//System.out.println("Stalemate found");
            	if (bestScore>=550){
            		//stalemate good
            		return -(depth+Orion.MATE_SCORE/2);
            	}
            	else{
            		//stalemate bad
            		return (depth+Orion.MATE_SCORE/2);
            	}
        		//return -(-depth-Orion.MATE_SCORE/2);//*myInt;
        	}

            //return WhiteToMove ? Orion.MATE_SCORE : -Orion.MATE_SCORE;
        }
        
        if (depth == 0)
        {
        	bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        	//bestScore = myInt*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,selfColorIsWhite);
        	
            return bestScore;
        }
        
        //sortMoves();
        moves = Rating.sortMoves(moves,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        
        //Update the hashmap that checks for three fold repetition
        if (Orion.ThreeMoveRepCheck.containsKey(boardHash)){
        	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)+1);
        }
        else{
        	Orion.ThreeMoveRepCheck.put(boardHash, 1);
        }
        
        for (int i=0;i<moves.length();i+=4) {
        	//System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4)));
            int score;
            //legal, non-castle move
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
            
            int numPiecesBefore = Rating.bitCount(WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK);
            int numPiecesAfter = Rating.bitCount(WPt|WNt|WBt|WRt|WQt|WKt|BPt|BNt|BBt|BRt|BQt|BKt);
            int fiftyMoveCountert;
            if ((numPiecesBefore==numPiecesAfter)&&(WP==WPt)&&(BP==BPt)){
            	fiftyMoveCountert = fiftyMoveCounter+1;
            }
            else{
            	fiftyMoveCountert = 0;
            }

            //System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4)));
            if (i!=0){
            	score = -pvSearch5(-alpha-1,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            	if (score>alpha && score<beta){
            		score = -pvSearch5(-beta,-score,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            	}
            }
            else{
            	score = -pvSearch5(-beta,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            }
            /*if (depth==Orion.searchDepth){
            	System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4))+" had a score of :"+score);
            	//System.out.println("alpha:"+alpha+", beta"+beta);
            }*/
            
            //alpha = Math.max(alpha, score);
            if (score>alpha||i==0){
            	alpha=score;
            	bestMoves=moves.substring(i, i+4);
            }
            else if(score==alpha){
            	bestMoves+=moves.substring(i, i+4);
            }
            if (alpha>=beta){
            	break;
            }
        }
        //Remove the value from the 3 fold repetition checker
    	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)-1);
    	//If we have found the best Move
    	if (depth==Orion.searchDepth){
    		//System.out.println(bestMoves);
    		int index=(int)(Math.floor(Math.random()*(bestMoves.length()/4))*4);
    		Strategies.bestMove = UCI.moveToAlgebra(bestMoves.substring(index, index+4));
    		//System.out.println("bestmove "+UCI.moveToAlgebra(bestMoves.substring(index, index+4)));
    	}
    	
    	//Store node in transposition table
    	int ttVal = alpha;
    	String ttFlag;
    	if (ttVal<=alphaOrig){
    		ttFlag = "UPPERBOUND";
    	}
    	else if (ttVal>=beta){
    		ttFlag = "LOWERBOUND";
    	}
    	else{
    		ttFlag = "EXACT";
    	}
    	TranspositionTable.addValue(boardHash, depth, ttFlag, ttVal);
    	//System.out.println("normal return");
        return alpha;
    }


    public static int pvSearch6(int alpha,int beta,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteHasCastled,boolean BlackHasCastled,boolean WhiteToMove,int depth,boolean selfColorIsWhite,int fiftyMoveCounter,int moveCounter) {//using fail soft with negamax
    	/*
    	 * Includes the first move in the alpha beta pruning process and speeds things up 2-4x compared to pvSearch3
    	 * Incorporates transposition tables.
    	 * Used for machine learning scoring
    	 */
    	
    	Orion.nodesSearchedCounter++;
        Long boardHash = Zobrist.getZobristHash(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove);
        
        //Transposition Table Look-Up
        int alphaOrig = alpha;
        if (TranspositionTable.contains(boardHash)&&TranspositionTable.getDepth(boardHash)>=depth){
        	if ("EXACT".equals(TranspositionTable.getFlag(boardHash))){
        		
        	}
        	else if ("LOWERBOUND".equals(TranspositionTable.getFlag(boardHash))){
        		alpha = Math.max(alpha, TranspositionTable.getValue(boardHash));
        	}
        	else if("UPPERBOUND".equals(TranspositionTable.getFlag(boardHash))){
        		beta = Math.min(beta, TranspositionTable.getValue(boardHash));
        	}
        	if (alpha>=beta){
        		//System.out.println("Transposition return");
        		return TranspositionTable.getValue(boardHash);
        	}
        }
        
        int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;
        if (fiftyMoveCounter==48||(Orion.ThreeMoveRepCheck.containsKey(boardHash)&&Orion.ThreeMoveRepCheck.get(boardHash)>=2)){
    		//Stalemate 3 fold repetition
        	//return myInt*(-Orion.MATE_SCORE/2);
        	//System.out.println("50move or 3rep return");
        	return depth+Orion.MATE_SCORE/2;
    		/*int bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteHasCastled,BlackHasCastled,WhiteToMove,selfColorIsWhite);
        	bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        	bestScore = myInt*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,selfColorIsWhite);
        	if (bestScore>=550){
        		//stalemate good
        		return -(depth+Orion.MATE_SCORE/2);
        	}
        	else{
        		//stalemate bad
        		return (depth+Orion.MATE_SCORE/2);
        	}*/
        }
        
    	int bestScore;
    	String bestMoves = "";
        String moves;
        if (WhiteToMove) {
            moves=Moves.possibleMovesW(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        } else {
            moves=Moves.possibleMovesB(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ);
        }
        moves = Moves.filterMoves(moves, WhiteToMove, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK, EP);

        if (moves.length() == 0)
        {
        	boolean unsafeMe;
        	if (WhiteToMove){
        		unsafeMe = (WK&Moves.unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        		
        	}
        	else{
        		unsafeMe = (BK&Moves.unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK))!=0;
        	}
        	//int myInt = (selfColorIsWhite==WhiteToMove) ? 1 : -1;
        	//Note: Scores are opposite of what would be expected because we are collecting the negative of pvs
        	//System.out.println("no moves return");
        	if (unsafeMe){
        		//Checkmate
        		
        		return -(Orion.MATE_SCORE+depth);//*myInt; //subtracted depth so moves that lead to checkmate faster are chosen
        	}
        	else{
        		//Stalemate
        		return -(-depth-Orion.MATE_SCORE/2);//*myInt;
        		/*bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteHasCastled,BlackHasCastled,WhiteToMove,selfColorIsWhite);
        		bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
        		bestScore = myInt*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,selfColorIsWhite);
            	if (bestScore>=550){
            		//stalemate good
            		return -(depth+Orion.MATE_SCORE/2);
            	}
            	else{
            		//stalemate bad
            		return (depth+Orion.MATE_SCORE/2);
            	}*/
        	}

            //return WhiteToMove ? Orion.MATE_SCORE : -Orion.MATE_SCORE;
        }
        
        if (depth == 0)
        {
        	bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteHasCastled,BlackHasCastled,WhiteToMove,selfColorIsWhite);
    		//bestScore = myInt*Rating.evaluate2(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteToMove,selfColorIsWhite);
    		//bestScore = myInt*Rating.evaluate(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,selfColorIsWhite);
            return bestScore;
        }
        
        //sortMoves();
        moves = Rating.sortMoves(moves,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK,EP,CWK,CWQ,CBK,CBQ,WhiteHasCastled,BlackHasCastled,WhiteToMove,selfColorIsWhite);
        
        //Update the hashmap that checks for three fold repetition
        if (Orion.ThreeMoveRepCheck.containsKey(boardHash)){
        	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)+1);
        }
        else{
        	Orion.ThreeMoveRepCheck.put(boardHash, 1);
        }
        
        for (int i=0;i<moves.length();i+=4) {
            int score;
            //legal, non-castle move
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
            
            int numPiecesBefore = Rating.bitCount(WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK);
            int numPiecesAfter = Rating.bitCount(WPt|WNt|WBt|WRt|WQt|WKt|BPt|BNt|BBt|BRt|BQt|BKt);
            int fiftyMoveCountert;
            if ((numPiecesBefore==numPiecesAfter)&&(WP==WPt)&&(BP==BPt)){
            	fiftyMoveCountert = fiftyMoveCounter+1;
            }
            else{
            	fiftyMoveCountert = 0;
            }

            //System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4)));
            if (i!=0){
            	score = -pvSearch6(-alpha-1,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,WhiteHasCastledt,BlackHasCastledt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            	if (score>alpha && score<beta){
            		score = -pvSearch6(-beta,-score,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,WhiteHasCastledt,BlackHasCastledt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            	}
            }
            else{
            	score = -pvSearch6(-beta,-alpha,WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt,EPt,CWKt,CWQt,CBKt,CBQt,WhiteHasCastledt,BlackHasCastledt,!WhiteToMove,depth-1,selfColorIsWhite,fiftyMoveCountert,moveCounter+1);
            }
            /*if (depth==Orion.searchDepth){
            	System.out.println(UCI.moveToAlgebra(moves.substring(i, i+4))+" had a score of :"+score);
            	//System.out.println("alpha:"+alpha+", beta"+beta);
            }*/
            
            //alpha = Math.max(alpha, score);
            if (score>alpha||i==0){
            	alpha=score;
            	bestMoves=moves.substring(i, i+4);
            }
            else if(score==alpha){
            	bestMoves+=moves.substring(i, i+4);
            }
            if (alpha>=beta){
            	break;
            }
        }
        //Remove the value from the 3 fold repetition checker
    	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)-1);
    	//If we have found the best Move
    	if (depth==Orion.searchDepth){
    		//System.out.println(bestMoves);
    		int index=(int)(Math.floor(Math.random()*(bestMoves.length()/4))*4);
    		Strategies.bestMove = UCI.moveToAlgebra(bestMoves.substring(index, index+4));
    		//System.out.println("bestmove "+UCI.moveToAlgebra(bestMoves.substring(index, index+4)));
    	}
    	
    	//Store node in transposition table
    	int ttVal = alpha;
    	String ttFlag;
    	if (ttVal<=alphaOrig){
    		ttFlag = "UPPERBOUND";
    	}
    	else if (ttVal>=beta){
    		ttFlag = "LOWERBOUND";
    	}
    	else{
    		ttFlag = "EXACT";
    	}
    	TranspositionTable.addValue(boardHash, depth, ttFlag, ttVal);
    	//System.out.println("normal return");
        return alpha;
    }


}
