import java.util.Arrays;

public class Moves {
	//Sections of the board
	static long FILE_A = 72340172838076673L;
	static long FILE_B = 144680345676153346L;
	static long FILE_C = 289360691352306692L;
	static long FILE_D = 578721382704613384L;
	static long FILE_E = 1157442765409226768L;
	static long FILE_F = 2314885530818453536L;
	static long FILE_G = 4629771061636907072L;
	static long FILE_H = -9187201950435737472L;
	static long FILE_AB = 217020518514230019L;
	static long FILE_GH = -4557430888798830400L;
	static long RANK_1 = 255L;
	static long RANK_2 = 65280L;
	static long RANK_3 = 16711680L;
	static long RANK_4 = 4278190080L;
	static long RANK_5 = 1095216660480L;
	static long RANK_6 = 280375465082880L;
	static long RANK_7 = 71776119061217280L;
	static long RANK_8 = -72057594037927936L;
	static long RANK_12 = 65535L;
	static long RANK_78 = -281474976710656L;
	//static long CENTER = 103481868288L;
	//static long EXTENDED_CENTER = 66229406269440L;
	
	//For Castling
	static long[] CASTLE_ROOKS ={7,0,63,56}; //WKs, WQs, BKs, BQs
	static long[] squaresBetweenKR = {12,96,864691128455135232L,6917529027641081856L,14,1008806316530991104L}; //WQ,WK,BQ,BK (safes), WQ, BQ (empties)
	//static long KING_SIDE = -1152921504606846736L;
	//static long QUEEN_SIDE = 1080863910568919055L;
	
	//King and Knight Move Generation
	static long KING_SPAN = 460039L;
	static long KNIGHT_SPAN=43234889994L;
	
	//Needed Statics
	static long NOT_MY_PIECES;
	static long MY_PIECES;
	static long EMPTY;
	static long OCCUPIED;
	static long UNSAFE;
	
	//Masks for sliding pieces
	static long[]	FileMasks8 = {FILE_A,FILE_B,FILE_C,FILE_D,FILE_E,FILE_F,FILE_G,FILE_H};
	static long[]	RankMasks8 = {RANK_1,RANK_2,RANK_3,RANK_4,RANK_5,RANK_6,RANK_7,RANK_8};
	static long[]	A8H1DiagMasks15 = 
		{
			1L,
			258L,66052L,
			16909320L,4328785936L,1108169199648L,
			283691315109952L,72624976668147840L,145249953336295424L,290499906672525312L,
			580999813328273408L,1161999622361579520L,2323998145211531264L,4647714815446351872L,-9223372036854775808L
		};
	static long[]	A1H8DiagMasks15 = 
		{
			128L,
			32832L,8405024L,
			2151686160L,550831656968L,141012904183812L,
			36099303471055874L,-9205322385119247871L,4620710844295151872L,2310355422147575808L,
			1155177711073755136L,577588855528488960L,288794425616760832L,144396663052566528L,72057594037927936L
		};

	//Move generation helper function for rooks, bishops, and knights
	static long HAndVMoves(int s){
		//(((o&m)-2*s) ^ ((o&m)'-2s')')&m;
		
		long binaryS = 1L<<s;
		long possibilitiesHorizontal = (OCCUPIED - 2*binaryS) ^ Long.reverse(Long.reverse(OCCUPIED)-2*Long.reverse(binaryS));
		long possibilitiesVertical = ((OCCUPIED&FileMasks8[s%8]) - (2*binaryS)) ^ Long.reverse(Long.reverse(OCCUPIED&FileMasks8[s%8]) - (2*Long.reverse(binaryS)));
		return ((possibilitiesHorizontal&RankMasks8[s/8])|(possibilitiesVertical&FileMasks8[s%8]));
	}
	static long DAndAntiDMoves(int s){
        long binaryS=1L<<s;
        long possibilitiesA8H1 = ((OCCUPIED&A8H1DiagMasks15[(s / 8) + (s % 8)]) - (2 * binaryS)) ^ Long.reverse(Long.reverse(OCCUPIED&A8H1DiagMasks15[(s / 8) + (s % 8)]) - (2 * Long.reverse(binaryS)));
        long possibilitiesA1H8 = ((OCCUPIED&A1H8DiagMasks15[(s / 8) + 7 - (s % 8)]) - (2 * binaryS)) ^ Long.reverse(Long.reverse(OCCUPIED&A1H8DiagMasks15[(s / 8) + 7 - (s % 8)]) - (2 * Long.reverse(binaryS)));
        return (possibilitiesA8H1&A8H1DiagMasks15[(s / 8) + (s % 8)]) | (possibilitiesA1H8&A1H8DiagMasks15[(s / 8) + 7 - (s % 8)]);
	}
	
	//Making moves
    /*
    long WPt=Moves.makeMove(WP, moves.substring(i,i+4), 'P'), WNt=Moves.makeMove(WN, moves.substring(i,i+4), 'N'),
    WBt=Moves.makeMove(WB, moves.substring(i,i+4), 'B'), WRt=Moves.makeMove(WR, moves.substring(i,i+4), 'R'),
    WQt=Moves.makeMove(WQ, moves.substring(i,i+4), 'Q'), WKt=Moves.makeMove(WK, moves.substring(i,i+4), 'K'),
    BPt=Moves.makeMove(BP, moves.substring(i,i+4), 'p'), BNt=Moves.makeMove(BN, moves.substring(i,i+4), 'n'),
    BBt=Moves.makeMove(BB, moves.substring(i,i+4), 'b'), BRt=Moves.makeMove(BR, moves.substring(i,i+4), 'r'),
    BQt=Moves.makeMove(BQ, moves.substring(i,i+4), 'q'), BKt=Moves.makeMove(BK, moves.substring(i,i+4), 'k'),
    EPt=Moves.makeMoveEP(WP|BP,moves.substring(i,i+4));
	WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(i,i+4), 'R');
	BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(i,i+4), 'r');
    */
	public static long makeMove(long board, String move, char type){
		if (Character.isDigit(move.charAt(3))){
			//Regular Move
			int start = Character.getNumericValue(move.charAt(1))*8 + Character.getNumericValue(move.charAt(0));
			int end = Character.getNumericValue(move.charAt(3))*8 + Character.getNumericValue(move.charAt(2));
			if (((board>>>start)&1)==1){
				board &=~(1L<<start);
				board |=(1L<<end);
			}
			else{
				board&=~(1L<<end);
			}
		}
		else if (move.charAt(3)=='P'){
			// Pawn Promotion
			int start, end;
            if (Character.isUpperCase(move.charAt(2))) {
                start=Long.numberOfTrailingZeros(FileMasks8[move.charAt(0)-'0']&RankMasks8[6]);
                end=Long.numberOfTrailingZeros(FileMasks8[move.charAt(1)-'0']&RankMasks8[7]);
            } else {
                start=Long.numberOfTrailingZeros(FileMasks8[move.charAt(0)-'0']&RankMasks8[1]);
                end=Long.numberOfTrailingZeros(FileMasks8[move.charAt(1)-'0']&RankMasks8[0]);
            }
            if (type=='p' || type=='P'){//remove the pawn from where it is
            	board&=~(1L<<start); 
            }
            else if (type==move.charAt(2)) {//Add the new piece to where it is going
            	board|=(1L<<end);
            } 
            else {//remove any piece being captured
            	board&=~(1L<<end);
            }
		}
		else if (move.charAt(3)=='E'){
			//En Passant
			int start, end;
            if (Character.isUpperCase(move.charAt(2))) {
                start=Long.numberOfTrailingZeros(FileMasks8[move.charAt(0)-'0']&RankMasks8[4]);
                end=Long.numberOfTrailingZeros(FileMasks8[move.charAt(1)-'0']&RankMasks8[5]);
                board&=~((FileMasks8[move.charAt(1)-'0']&RankMasks8[4]));
            } 
            else {
                start=Long.numberOfTrailingZeros(FileMasks8[move.charAt(0)-'0']&RankMasks8[3]);
                end=Long.numberOfTrailingZeros(FileMasks8[move.charAt(1)-'0']&RankMasks8[2]);
                board&=~((FileMasks8[move.charAt(1)-'0']&RankMasks8[3]));
            }
            if (((board>>>start)&1)==1) {
            	board&=~(1L<<start);
            	board|=(1L<<end);
            }
		}
		else{
			System.out.println("Error: Invalid move type");
		}
		return board;
	}
    public static long makeMoveCastle(long rookBoard, long kingBoard, String move, char type) {
        int start=(Character.getNumericValue(move.charAt(0)))+(Character.getNumericValue(move.charAt(1))*8);
        if ((((kingBoard>>>start)&1)==1)&&(("4020".equals(move))||("4060".equals(move))||("4727".equals(move))||("4767".equals(move)))) {//'regular' move
            if (type=='r') {
                switch (move) {
                    case "4727": rookBoard&=~(1L<<CASTLE_ROOKS[3]); rookBoard|=(1L<<(CASTLE_ROOKS[3]+3));
                        break;
                    case "4767": rookBoard&=~(1L<<CASTLE_ROOKS[2]); rookBoard|=(1L<<(CASTLE_ROOKS[2]-2));
                        break;
                }
            } else {
                switch (move) {
                    case "4020": rookBoard&=~(1L<<CASTLE_ROOKS[1]); rookBoard|=(1L<<(CASTLE_ROOKS[1]+3));
                        break;
                    case "4060": rookBoard&=~(1L<<CASTLE_ROOKS[0]); rookBoard|=(1L<<(CASTLE_ROOKS[0]-2));
                        break;
                }
            }
        }
        return rookBoard;
    }
	public static long makeMoveEP(long board,String move){
		//TODO
        if (Character.isDigit(move.charAt(3))) {
            int start=(Character.getNumericValue(move.charAt(1))*8)+(Character.getNumericValue(move.charAt(0)));
            //Boards being passed in are pawn boards
            if ((Math.abs(move.charAt(1)-move.charAt(3))==2)&&(((board>>>start)&1)==1)) {//pawn double push
                return FileMasks8[move.charAt(0)-'0'];
            }
        }
		return 0;
	}
	
	//Generating all possible moves
	public static String possibleMovesW(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ){
		NOT_MY_PIECES = ~(WP|WN|WB|WR|WQ|WK|BK); //Added BK to avoid illegal capture
		MY_PIECES = WP|WN|WB|WR|WQ;//omitted WK to avoid illegal capture
		OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
		EMPTY = ~OCCUPIED;
		//timeExperiment(WP);
		UNSAFE = unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
		String list = possibleWP(WP,BP,EP)+
		possibleN(OCCUPIED,WN)+
		possibleB(OCCUPIED,WB)+
		possibleR(OCCUPIED,WR)+
		possibleQ(OCCUPIED,WQ)+
		possibleK(OCCUPIED,WK)+
		possibleCW(WR,CWK,CWQ,WK);
		//unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
		return list;
	}
	public static String possibleMovesB(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ){
		NOT_MY_PIECES = ~(BP|BN|BB|BR|BQ|BK|WK); //Added WK to avoid illegal capture
		MY_PIECES = BP|BN|BB|BR|BQ;//omitted WK to avoid illegal capture
		OCCUPIED = WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
		EMPTY = ~OCCUPIED;
		UNSAFE = unsafeForBlack(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
		String list = possibleBP(BP,WP,EP)+
		possibleN(OCCUPIED,BN)+
		possibleB(OCCUPIED,BB)+
		possibleR(OCCUPIED,BR)+
		possibleQ(OCCUPIED,BQ)+
		possibleK(OCCUPIED,BK)+
		possibleCB(BR,CBK,CBQ,BK);
		//unsafeForWhite(WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK);
		return list;
	}
	
	//Get Pawn Moves - Dependent on Color
	public static String possibleWP(long WP,long BP,long EP){
		String list="";
		//x1,y1,x2,y2
		//Capture Right
		Long PAWN_MOVES  = ((WP& ~FILE_H) <<9) & NOT_MY_PIECES & OCCUPIED & ~RANK_8;
        long possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8-1)+(i/8-1)+(i%8)+(i/8);
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Capture Left
		PAWN_MOVES  = ((WP& ~FILE_A) <<7) & NOT_MY_PIECES & OCCUPIED & ~RANK_8;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8+1)+(i/8-1)+(i%8)+(i/8);
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Move 1 Forward
		PAWN_MOVES  =  (WP<<8) & EMPTY & ~RANK_8;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8)+(i/8-1)+(i%8)+(i/8);
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Move 2 Forward
		PAWN_MOVES  =  WP<<16 & EMPTY & (EMPTY<<8) & RANK_4;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8)+(i/8-2)+(i%8)+(i/8);
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//x1,x2,Promotion Type,"P"
		//Capture Right
		PAWN_MOVES  = ((WP& ~FILE_H) <<9) & NOT_MY_PIECES & OCCUPIED & RANK_8;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8-1)+(i%8)+"QP"+(i%8-1)+(i%8)+"RP"+(i%8-1)+(i%8)+"BP"+(i%8-1)+(i%8)+"NP";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Capture Left
		PAWN_MOVES  = ((WP& ~FILE_A) <<7) & NOT_MY_PIECES & OCCUPIED & RANK_8;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8+1)+(i%8)+"QP"+(i%8+1)+(i%8)+"RP"+(i%8+1)+(i%8)+"BP"+(i%8+1)+(i%8)+"NP";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Move 1 Forward
		PAWN_MOVES  =  (WP<<8) & EMPTY & RANK_8;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8)+(i%8)+"QP"+(i%8)+(i%8)+"RP"+(i%8)+(i%8)+"BP"+(i%8)+(i%8)+"NP";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//x1,x2,"WE"
		//en passant right
		possibility  =  (WP<<1)&BP&RANK_5 &~FILE_A&EP;
        if (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8-1)+(i%8)+"WE";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//en passant left
		possibility  =  (WP>>>1)&BP&RANK_5 &~FILE_H&EP;
        if (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8+1)+(i%8)+"WE";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }

        /*
        if (history.length()>=4){
        	if ( (history.charAt(history.length()-4) == history.charAt(history.length()-2)) && (Math.abs(history.charAt(history.length()-1)-history.charAt(history.length()-3))==2) ){
        		int eFile=history.charAt(history.length()-2)-'0';
        		//en passant right
        		possibility  =  (WP<<1)&BP&RANK_5 &~FILE_A&FileMasks8[eFile];
                if (possibility != 0)
                {
                    int i=Long.numberOfTrailingZeros(possibility);
                    list+= ""+(i%8-1)+(i%8)+" E";
                    PAWN_MOVES&=~(possibility);
                    possibility=PAWN_MOVES&~(PAWN_MOVES-1);
                }
        		//en passant left
        		possibility  =  (WP>>>1)&BP&RANK_5 &~FILE_H&FileMasks8[eFile];
                if (possibility != 0)
                {
                    int i=Long.numberOfTrailingZeros(possibility);
                    list+= ""+(i%8+1)+(i%8)+" E";
                    PAWN_MOVES&=~(possibility);
                    possibility=PAWN_MOVES&~(PAWN_MOVES-1);
                }
        	}
        }
        */
        
		return list;
	}
	public static String possibleBP(long BP,long WP,long EP){
		String list="";
		//x1,y1,x2,y2
		//Capture Right
		Long PAWN_MOVES  = ((BP& ~FILE_H) >>>7) & NOT_MY_PIECES & OCCUPIED & ~RANK_1;
        long possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8-1)+(i/8+1)+(i%8)+(i/8);
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Capture Left
		PAWN_MOVES  = ((BP& ~FILE_A) >>>9) & NOT_MY_PIECES & OCCUPIED & ~RANK_1;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8+1)+(i/8+1)+(i%8)+(i/8);
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Move 1 Forward
		PAWN_MOVES  =  (BP>>>8) & EMPTY & ~RANK_1;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8)+(i/8+1)+(i%8)+(i/8);
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Move 2 Forward
		PAWN_MOVES  =  BP>>>16 & EMPTY & (EMPTY>>>8) & RANK_5;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8)+(i/8+2)+(i%8)+(i/8);
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//x1,x2,Promotion Type,"P"
		//Capture Right
		PAWN_MOVES = ((BP& ~FILE_H) >>>7) & NOT_MY_PIECES & OCCUPIED & RANK_1;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8-1)+(i%8)+"qP"+(i%8-1)+(i%8)+"rP"+(i%8-1)+(i%8)+"bP"+(i%8-1)+(i%8)+"nP";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Capture Left
		PAWN_MOVES = ((BP& ~FILE_A) >>>9) & NOT_MY_PIECES & OCCUPIED & RANK_1;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8+1)+(i%8)+"qP"+(i%8+1)+(i%8)+"rP"+(i%8+1)+(i%8)+"bP"+(i%8+1)+(i%8)+"nP";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//Move 1 Forward
		PAWN_MOVES  =  (BP>>>8) & EMPTY & RANK_1;
		possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        while (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8)+(i%8)+"qP"+(i%8)+(i%8)+"rP"+(i%8)+(i%8)+"bP"+(i%8)+(i%8)+"nP";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//x1,x2,"bE"
      //en passant right
		possibility  =  (BP<<1)&WP&RANK_4 &~FILE_A&EP;
        if (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8-1)+(i%8)+"bE";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
		//en passant left
		possibility  =  (BP>>>1)&WP&RANK_4 &~FILE_H&EP;
        if (possibility != 0)
        {
            int i=Long.numberOfTrailingZeros(possibility);
            list+= ""+(i%8+1)+(i%8)+"bE";
            PAWN_MOVES&=~(possibility);
            possibility=PAWN_MOVES&~(PAWN_MOVES-1);
        }
        /*
        if (history.length()>=4){
        	if ( (history.charAt(history.length()-4) == history.charAt(history.length()-2)) && (Math.abs(history.charAt(history.length()-1)-history.charAt(history.length()-3))==2) ){
        		int eFile=history.charAt(history.length()-2)-'0';
        		//en passant right
        		possibility  =  (BP<<1)&WP&RANK_4 &~FILE_A&FileMasks8[eFile];
                if (possibility != 0)
                {
                    int i=Long.numberOfTrailingZeros(possibility);
                    list+= ""+(i%8-1)+(i%8)+"bE";
                    PAWN_MOVES&=~(possibility);
                    possibility=PAWN_MOVES&~(PAWN_MOVES-1);
                }
        		//en passant left
        		possibility  =  (BP>>>1)&WP&RANK_4 &~FILE_H&FileMasks8[eFile];
                if (possibility != 0)
                {
                    int i=Long.numberOfTrailingZeros(possibility);
                    list+= ""+(i%8+1)+(i%8)+"bE";
                    PAWN_MOVES&=~(possibility);
                    possibility=PAWN_MOVES&~(PAWN_MOVES-1);
                }
        	}
        }
         */
        
		return list;
	}
	
	//Moves for other pieces, color independent
    public static String possibleB(long OCCUPIED, long B){
        String list="";
        long i=B&~(B-1);
        long possibility;
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            possibility=DAndAntiDMoves(iLocation)&NOT_MY_PIECES;
            long j=possibility&~(possibility-1);
            while (j != 0)
            {
                int index=Long.numberOfTrailingZeros(j);
                list+=""+(iLocation%8)+(iLocation/8)+(index%8)+(index/8);
                possibility&=~j;
                j=possibility&~(possibility-1);
            }
            B&=~i;
            i=B&~(B-1);
        }
        return list;
    }
    public static String possibleR(long OCCUPIED, long R){
        String list="";
        long i=R&~(R-1);
        long possibility;
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            possibility=HAndVMoves(iLocation)&NOT_MY_PIECES;
            long j=possibility&~(possibility-1);
            while (j != 0)
            {
                int index=Long.numberOfTrailingZeros(j);
                list+=""+(iLocation%8)+(iLocation/8)+(index%8)+(index/8);
                possibility&=~j;
                j=possibility&~(possibility-1);
            }
            R&=~i;
            i=R&~(R-1);
        }
        return list;
    }
    public static String possibleQ(long OCCUPIED, long Q){
        String list="";
        long i=Q&~(Q-1);
        long possibility;
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            possibility=(HAndVMoves(iLocation)|DAndAntiDMoves(iLocation))&NOT_MY_PIECES;
            long j=possibility&~(possibility-1);
            while (j != 0)
            {
                int index=Long.numberOfTrailingZeros(j);
                list+=""+(iLocation%8)+(iLocation/8)+(index%8)+(index/8);
                possibility&=~j;
                j=possibility&~(possibility-1);
            }
            Q&=~i;
            i=Q&~(Q-1);
        }
        return list;
    }
    public static String possibleN(long OCCUPIED, long N){
        String list="";
        long i=N&~(N-1);
        long possibility;
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            
            if (iLocation>18)
            {
                possibility=KNIGHT_SPAN<<(iLocation-18);
            }
            else {
                possibility=KNIGHT_SPAN>>(18-iLocation);
            }
            if (iLocation%8<4)
            {
                possibility &=~FILE_GH&NOT_MY_PIECES;
            }
            else {
                possibility &=~FILE_AB&NOT_MY_PIECES;
            }
            
            long j=possibility&~(possibility-1);
            while (j != 0)
            {
                int index=Long.numberOfTrailingZeros(j);
                list+=""+(iLocation%8)+(iLocation/8)+(index%8)+(index/8);
                possibility&=~j;
                j=possibility&~(possibility-1);
            }
            N&=~i;
            i=N&~(N-1);
        }
        return list;
    }
    public static String possibleK(long OCCUPIED, long K){
        String list="";
        long i=K&~(K-1);
        long possibility;
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            
            if (iLocation>9)
            {
                possibility=KING_SPAN<<(iLocation-9);
            }
            else {
                possibility=KING_SPAN>>(9-iLocation);
            }
            if (iLocation%8<4)
            {
                possibility &=~FILE_GH&NOT_MY_PIECES;
            }
            else {
                possibility &=~FILE_AB&NOT_MY_PIECES;
            }
            
            long j=possibility&~(possibility-1);
            while (j != 0)
            {
                int index=Long.numberOfTrailingZeros(j);
                list+=""+(iLocation%8)+(iLocation/8)+(index%8)+(index/8);
                possibility&=~j;
                j=possibility&~(possibility-1);
            }
            K&=~i;
            i=K&~(K-1);
        }
        return list;
    }
    
    //Castling
    public static String possibleCW(long WR,boolean CWK,boolean CWQ,long WK)
    {
    	String list = "";
    	if ((UNSAFE&WK)==0) {
	    	if(CWK&&(((1L<<CASTLE_ROOKS[0])&WR)!=0)&&((((UNSAFE|OCCUPIED))&squaresBetweenKR[1])==0))
	    	{
	    		list+="4060";
	    	}
	    	if(CWQ&&(((1L<<CASTLE_ROOKS[1])&WR)!=0)&&(((UNSAFE&squaresBetweenKR[0])|(OCCUPIED&squaresBetweenKR[4]))==0))
	    	{
	    		list+="4020";
	    	}
    	}
    	return list;
    }
    public static String possibleCB(long BR,boolean CBK,boolean CBQ,long BK)
    {
    	String list = "";
    	//make sure CBK or CBQ is true, the rook is still in the right spot, and the squares between the king and rook are safe and unoccupied
    	if ((UNSAFE&BK)==0) {
	    	if(CBK&&(((1L<<CASTLE_ROOKS[2])&BR)!=0)&&((((UNSAFE|OCCUPIED))&squaresBetweenKR[3])==0))
	    	{
	    		list+="4767";
	    	}
	    	if(CBQ&&(((1L<<CASTLE_ROOKS[3])&BR)!=0)&&(((UNSAFE&squaresBetweenKR[2])|(OCCUPIED&squaresBetweenKR[5]))==0))
	    	{
	    		list+="4727";
	    	}
    	}
    	return list;
    }    
    //returns a long that shows all the squares that are unsafe for a color
    public static long unsafeForBlack(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK)
    {
        long unsafe;
        OCCUPIED=WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
        //pawn
        unsafe=((WP<<9)&~FILE_A);//pawn capture right
        unsafe|=((WP<<7)&~FILE_H);//pawn capture left
        long possibility;
        //knight
        long i=WN&~(WN-1);
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            if (iLocation>18)
            {
                possibility=KNIGHT_SPAN<<(iLocation-18);
            }
            else {
                possibility=KNIGHT_SPAN>>(18-iLocation);
            }
            if (iLocation%8<4)
            {
                possibility &=~FILE_GH;
            }
            else {
                possibility &=~FILE_AB;
            }
            unsafe |= possibility;
            WN&=~i;
            i=WN&~(WN-1);
        }
        //bishop/queen
        long QB=WQ|WB;
        i=QB&~(QB-1);
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            possibility=DAndAntiDMoves(iLocation);
            unsafe |= possibility;
            QB&=~i;
            i=QB&~(QB-1);
        }
        //rook/queen
        long QR=WQ|WR;
        i=QR&~(QR-1);
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            possibility=HAndVMoves(iLocation);
            unsafe |= possibility;
            QR&=~i;
            i=QR&~(QR-1);
        }
        //king
        int iLocation=Long.numberOfTrailingZeros(WK);
        if (iLocation>9)
        {
            possibility=KING_SPAN<<(iLocation-9);
        }
        else {
            possibility=KING_SPAN>>(9-iLocation);
        }
        if (iLocation%8<4)
        {
            possibility &=~FILE_GH;
        }
        else {
            possibility &=~FILE_AB;
        }
        unsafe |= possibility;
        //System.out.println();
        //drawBitboard(unsafe);
        return unsafe;
    }
    public static long unsafeForWhite(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK)
    {
        long unsafe;
        OCCUPIED=WP|WN|WB|WR|WQ|WK|BP|BN|BB|BR|BQ|BK;
        //pawn
        unsafe=((BP>>>7)&~FILE_A);//pawn capture right
        unsafe|=((BP>>>9)&~FILE_H);//pawn capture left
        long possibility;
        //knight
        long i=BN&~(BN-1);
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            if (iLocation>18)
            {
                possibility=KNIGHT_SPAN<<(iLocation-18);
            }
            else {
                possibility=KNIGHT_SPAN>>(18-iLocation);
            }
            if (iLocation%8<4)
            {
                possibility &=~FILE_GH;
            }
            else {
                possibility &=~FILE_AB;
            }
            unsafe |= possibility;
            BN&=~i;
            i=BN&~(BN-1);
        }
        //bishop/queen
        long QB=BQ|BB;
        i=QB&~(QB-1);
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            possibility=DAndAntiDMoves(iLocation);
            unsafe |= possibility;
            QB&=~i;
            i=QB&~(QB-1);
        }
        //rook/queen
        long QR=BQ|BR;
        i=QR&~(QR-1);
        while(i != 0)
        {
            int iLocation=Long.numberOfTrailingZeros(i);
            possibility=HAndVMoves(iLocation);
            unsafe |= possibility;
            QR&=~i;
            i=QR&~(QR-1);
        }
        //king
        int iLocation=Long.numberOfTrailingZeros(BK);
        if (iLocation>9)
        {
            possibility=KING_SPAN<<(iLocation-9);
        }
        else {
            possibility=KING_SPAN>>(9-iLocation);
        }
        if (iLocation%8<4)
        {
            possibility &=~FILE_GH;
        }
        else {
            possibility &=~FILE_AB;
        }
        unsafe |= possibility;
        //System.out.println();
        //drawBitboard(unsafe);
        return unsafe;
    }
    
    //Filter Unsafe Moves
    public static String filterMoves(String moves,boolean WhiteToMove,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP){
    	String safeMoves = "";
    	for (int i=0;i<moves.length();i+=4){
            long WPt=Moves.makeMove(WP, moves.substring(i,i+4), 'P'), WNt=Moves.makeMove(WN, moves.substring(i,i+4), 'N'),
                    WBt=Moves.makeMove(WB, moves.substring(i,i+4), 'B'), WRt=Moves.makeMove(WR, moves.substring(i,i+4), 'R'),
                    WQt=Moves.makeMove(WQ, moves.substring(i,i+4), 'Q'), WKt=Moves.makeMove(WK, moves.substring(i,i+4), 'K'),
                    BPt=Moves.makeMove(BP, moves.substring(i,i+4), 'p'), BNt=Moves.makeMove(BN, moves.substring(i,i+4), 'n'),
                    BBt=Moves.makeMove(BB, moves.substring(i,i+4), 'b'), BRt=Moves.makeMove(BR, moves.substring(i,i+4), 'r'),
                    BQt=Moves.makeMove(BQ, moves.substring(i,i+4), 'q'), BKt=Moves.makeMove(BK, moves.substring(i,i+4), 'k');
            WRt=Moves.makeMoveCastle(WRt, WK|BK, moves.substring(i,i+4), 'R');
            BRt=Moves.makeMoveCastle(BRt, WK|BK, moves.substring(i,i+4), 'r');
            if ((WhiteToMove&&((WKt&Moves.unsafeForWhite(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt))==0))||
                    (!WhiteToMove &&((BKt&Moves.unsafeForBlack(WPt,WNt,WBt,WRt,WQt,WKt,BPt,BNt,BBt,BRt,BQt,BKt))==0))) {
            	safeMoves +=moves.substring(i, i+4);
            }
            
    	}
		return safeMoves;
    }
    
    //Helper functions for debugging
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
    public static void timeExperiment(long WP) {
        int loopLength=1000;
        long startTime=System.currentTimeMillis();
        tEMethodA(loopLength, WP);
        long endTime=System.currentTimeMillis();
        System.out.println("That took "+(endTime-startTime)+" milliseconds for the first method");
        startTime=System.currentTimeMillis();
        tEMethodB(loopLength, WP);
        endTime=System.currentTimeMillis();
        System.out.println("That took "+(endTime-startTime)+" milliseconds for the second method");
    }
    public static void tEMethodA(int loopLength, long WP) {
        for (int loop=0;loop<loopLength;loop++)
        {
            long PAWN_MOVES=(WP>>7)&NOT_MY_PIECES&OCCUPIED&~RANK_8&~FILE_A;//capture right
            String list="";
            for (int i=0;i<64;i++) {
                if (((PAWN_MOVES>>i)&1)==1) {
                    list+=""+(i/8+1)+(i%8-1)+(i/8)+(i%8);
                }
            }
            System.out.println(list);
        }
    }
    public static void tEMethodB(int loopLength, long WP) {
        for (int loop=0;loop<loopLength;loop++)
        {
            long PAWN_MOVES=(WP>>7)&NOT_MY_PIECES&OCCUPIED&~RANK_8&~FILE_A;//capture right
            String list="";
            long possibility=PAWN_MOVES&~(PAWN_MOVES-1);
            while (possibility != 0)
            {
                int index=Long.numberOfTrailingZeros(possibility);
                list+=""+(index/8+1)+(index%8-1)+(index/8)+(index%8);
                PAWN_MOVES&=~(possibility);
                possibility=PAWN_MOVES&~(PAWN_MOVES-1);
            }
            System.out.println(list);   
        }
    }  

}
