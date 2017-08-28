import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class BoardGeneration {

	//Board Instantiation
	@SuppressWarnings("rawtypes")
	public static void loadGamePGN(String moveInformation){
		//To load a chess game.
		importFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
		parseMoveList(moveInformation);
	}

	public static void parseMoveList(String moveList){
		//System.out.println(moveList);
		//System.out.println();
		//Find index of "1/2-1/2" or "1-0" or "0-1" and cut off string there leaving one space at the end
		if (moveList.indexOf(" 1-0")!=-1){
			//White
			moveList = moveList.substring(0, moveList.indexOf(" 1-0"));
		}
		else if(moveList.indexOf(" 0-1")!=-1){
			//Black wins
			moveList = moveList.substring(0, moveList.indexOf(" 0-1"));
		}
		else{
			//Draw
			moveList = moveList.substring(0, moveList.indexOf(" 1/2-1/2"));
		}
		//System.out.println(moveList);
		//System.out.println();
		//Strip out all the numbers
		int moveCount = 1;
		String moveCountString = "1.";
		while (moveList.indexOf(moveCountString)!=-1){
			int index1 = moveList.indexOf(moveCountString);
			int index2 = moveList.indexOf(".", index1);
			moveList = moveList.substring(0, index1) + moveList.substring(index2+1); 
			moveCount++;
			moveCountString = moveCount + ".";
		}
		//System.out.println(moveList);
		//System.out.println();
		
		//Remove checks and captures
		moveList = moveList.replace("+", "");
		moveList = moveList.replace("x", "");
		
		//System.out.println(moveList);
		//System.out.println();
		
		int nextSpace;
		String move;
		String coordinateMove;
		while(moveList.length()>1){
			nextSpace = moveList.indexOf(' ');
			move = moveList.substring(0,nextSpace);
			moveList = moveList.substring(nextSpace+1);
			//System.out.println(move);
			//Castling "O-O-O" "O-O"
			if(move.equals("O-O-O")||move.equals("O-O")){
				String x1="4",y1,x2,y2;
				if(move.equals("O-O-O")){x2 = "2";}else{x2 = "6";}
				if(Orion.WhiteToMove){y1 = "0";y2="0";Orion.WhiteHasCastled=true;}else{y1 = "7";y2="7";Orion.BlackHasCastled=true;}
				coordinateMove = x1+y1+x2+y2;
			}
			//Pawn Promotion "a8=Q+" "gxh1=Q+" "a1=Q" "dxe8=Q"--> "a8=Q" "gh1=Q" "a1=Q" "de8=Q"
			else if(move.contains("=")){
				String frontHalf;
				if(move.length()==4){
					//Capture
					frontHalf = (char)('0'+move.charAt(0)-'a') +""+ (char)('0'+move.charAt(0)-'a');
				}
				else{
					//Move Forward
					frontHalf = (char)('0'+move.charAt(0)-'a') +""+ (char)('0'+move.charAt(1)-'a');
				}
				char selectedTransformation = move.charAt(move.length()-1);
				if (!Orion.WhiteToMove){selectedTransformation = Character.toLowerCase(selectedTransformation);}
				String backHalf = selectedTransformation+"P";
				coordinateMove = frontHalf+backHalf;
			}
			//Regular moves
			//(only end square given) "Na6" "g6" "Rxc7+" --> "Na6" "g6" "Rc7"
			//(start file given) "Rhe1" "cxd5" "Nge2" --> "Rhe1" "cd5" "Nge2"
			//(start rank given) "R1h5" "R1e7+" -- > "R1h5" "R1e7"
			//(start square given) "Rh1h5" just in case
			else{
				String frontHalf;
				String backHalf = ""+(char)('0'+move.charAt(move.length()-2)-'a') + (char)('0'+move.charAt(move.length()-1)-'1');
				if(Character.isUpperCase(move.charAt(0))){
					//Back row piece movement
					if (move.length()==5){
						//rank and file specified
						frontHalf = ""+(char)(move.charAt('0'+move.length()-4)-'a') + (char)('0'+move.charAt(move.length()-3)-'1');
					}
					else{
						long backRow;
						if (Orion.WhiteToMove){
							backRow=Orion.WR|Orion.WB|Orion.WN|Orion.WQ|Orion.WK;
							}
						else{
							backRow=Orion.BR|Orion.BB|Orion.BN|Orion.BQ|Orion.BK;
						}
						long rooks = Orion.WR|Orion.BR,bishops = Orion.WB|Orion.BB,
								knights = Orion.WN|Orion.BN,queens=Orion.WQ|Orion.BQ,
								kings=Orion.WK|Orion.BK;
						if (move.length()==4){
							long mask;
							//rank or file specified
							if (Character.isDigit(move.charAt(1))){
								mask = Moves.RankMasks8[move.charAt(1)-'1'];
							}
							else{
								mask = Moves.FileMasks8[move.charAt(1)-'a'];
							}	
							rooks &= mask;
							bishops &= mask;
							knights &= mask;
							queens &= mask;
							kings &= mask;
						}
						int x2 = backHalf.charAt(0)-'0';
						int y2 = backHalf.charAt(1)-'0';
						int iLocation = y2*8 + x2%8;
						long movesForPiece;
						long foundPiece;
						if (move.charAt(0)=='R'){
							//Rook
							movesForPiece = Moves.HAndVMoves(iLocation); //rook
							foundPiece = movesForPiece&backRow&rooks;
						}
						else if(move.charAt(0)=='B'){
							//Bishop
							movesForPiece = Moves.DAndAntiDMoves(iLocation); //bishop
							foundPiece = movesForPiece&backRow&bishops;
						}
						else if(move.charAt(0)=='N'){
							//Knight
				            if (iLocation>18)
				            {
				            	movesForPiece=Moves.KNIGHT_SPAN<<(iLocation-18);
				            }
				            else {
				            	movesForPiece=Moves.KNIGHT_SPAN>>(18-iLocation);
				            }
				            if (iLocation%8<4)
				            {
				            	movesForPiece &=~Moves.FILE_GH;
				            }
				            else {
				            	movesForPiece &=~Moves.FILE_AB;
				            }
				            
							foundPiece = movesForPiece&backRow&knights;
						}
						else if(move.charAt(0)=='Q'){
							//Queen
							movesForPiece = Moves.DAndAntiDMoves(iLocation)|Moves.HAndVMoves(iLocation); //queens
							foundPiece = movesForPiece&backRow&queens;
						}
						else{
							//King
				            if (iLocation>9)
				            {
				            	movesForPiece=Moves.KING_SPAN<<(iLocation-9);
				            }
				            else {
				            	movesForPiece=Moves.KING_SPAN>>(9-iLocation);
				            }
				            if (iLocation%8<4)
				            {
				            	movesForPiece &=~Moves.FILE_GH;
				            }
				            else {
				            	movesForPiece &=~Moves.FILE_AB;
				            }
							foundPiece = movesForPiece&backRow&kings;
						}
						int x1 = Long.numberOfTrailingZeros(foundPiece)%8;
						int y1 = Long.numberOfTrailingZeros(foundPiece)/8;
						//get piece moves depending on piece type. And with piece type and back row to get the location of the piece
						frontHalf = ""+x1+y1;
					}
				}
				else{
					//Moving piece is a pawn.
					if (move.length()==3){
						//Piece Capture
						int x2 = backHalf.charAt(0)-'0';
						int y2 = backHalf.charAt(1)-'0';
						long attackedSquare = 1L<<(y2*8 + x2%8);
						long allPieces = Orion.WP|Orion.WR|Orion.WB|Orion.WN|Orion.WQ|Orion.WK|Orion.BP|Orion.BR|Orion.BB|Orion.BN|Orion.BQ|Orion.BK;
						if ((attackedSquare&allPieces)==0){
							//En Passant
							if (Orion.WhiteToMove){backHalf = "WE";}else{backHalf = "bE";}
							frontHalf = ""+(char)('0'+move.charAt(0)-'a') + (char)('0'+move.charAt(1)-'a');
						}
						else{
							//regular capture
							int dy;
							if (Orion.WhiteToMove){dy = -1;}else{dy=1;}
							frontHalf = ""+(char)('0'+move.charAt(0)-'a') + (char)('0'+move.charAt(2)-'1'+dy);
						}
					}
					else{
						int x1 = backHalf.charAt(0)-'0'; //same as x2
						int dy,y1;
						long pawns;
						if (Orion.WhiteToMove){dy = -1;pawns=Orion.WP;}else{dy=1;pawns=Orion.BP;}
						int possibleFirsty1 = backHalf.charAt(1)-'0' + dy; //singlePawnPush
						int possibleSecondy1= backHalf.charAt(1)-'0' + 2*dy; //doublePawnPush
						if (((pawns>>(possibleFirsty1*8 + x1%8))&1L)!=0){
							y1 = possibleFirsty1;
						}
						else{
							y1 = possibleSecondy1;
						}
						frontHalf = ""+x1+y1;
						//Pawn forward move
						//Check one square back
						//Check two squares back
					}
				}
				coordinateMove = frontHalf+backHalf;
				//System.out.println(coordinateMove);
			}
			
			//Make move
			int start=0,end=0;
	        {
	        	//Get start and end positions to check that we are not breaking castling rights
	            if (Character.isDigit(coordinateMove.charAt(3))) {//'regular' move
	                start=(Character.getNumericValue(coordinateMove.charAt(0)))+(Character.getNumericValue(coordinateMove.charAt(1))*8);
	                end=(Character.getNumericValue(coordinateMove.charAt(2)))+(Character.getNumericValue(coordinateMove.charAt(3))*8);;
	            } else if (coordinateMove.charAt(3)=='P') {//pawn promotion
	                if (Character.isUpperCase(coordinateMove.charAt(2))) {
	                    start=Long.numberOfTrailingZeros(Moves.FileMasks8[coordinateMove.charAt(0)-'0']&Moves.RankMasks8[6]);
	                    end=Long.numberOfTrailingZeros(Moves.FileMasks8[coordinateMove.charAt(1)-'0']&Moves.RankMasks8[7]);
	                } else {
	                    start=Long.numberOfTrailingZeros(Moves.FileMasks8[coordinateMove.charAt(0)-'0']&Moves.RankMasks8[1]);
	                    end=Long.numberOfTrailingZeros(Moves.FileMasks8[coordinateMove.charAt(1)-'0']&Moves.RankMasks8[0]);
	                }
	            } else if (coordinateMove.charAt(3)=='E') {//en passant
	                if (coordinateMove.charAt(2)=='W') {
	                    start=Long.numberOfTrailingZeros(Moves.FileMasks8[coordinateMove.charAt(0)-'0']&Moves.RankMasks8[4]);
	                    end=Long.numberOfTrailingZeros(Moves.FileMasks8[coordinateMove.charAt(1)-'0']&Moves.RankMasks8[5]);
	                } else {
	                    start=Long.numberOfTrailingZeros(Moves.FileMasks8[coordinateMove.charAt(0)-'0']&Moves.RankMasks8[3]);
	                    end=Long.numberOfTrailingZeros(Moves.FileMasks8[coordinateMove.charAt(1)-'0']&Moves.RankMasks8[2]);
	                }
	            }
	            else{
	            	System.out.println("An unrecognizable move was generated");
	            }
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
                Orion.EP=Moves.makeMoveEP(Orion.WP|Orion.BP,coordinateMove);
                Orion.WR=Moves.makeMoveCastle(Orion.WR, Orion.WK|Orion.BK, coordinateMove, 'R');
                Orion.BR=Moves.makeMoveCastle(Orion.BR, Orion.WK|Orion.BK, coordinateMove, 'r');
                Orion.WP=Moves.makeMove(Orion.WP, coordinateMove, 'P');
                Orion.WN=Moves.makeMove(Orion.WN, coordinateMove, 'N');
                Orion.WB=Moves.makeMove(Orion.WB, coordinateMove, 'B');
                Orion.WR=Moves.makeMove(Orion.WR, coordinateMove, 'R');
                Orion.WQ=Moves.makeMove(Orion.WQ, coordinateMove, 'Q');
                Orion.WK=Moves.makeMove(Orion.WK, coordinateMove, 'K');
                Orion.BP=Moves.makeMove(Orion.BP, coordinateMove, 'p');
                Orion.BN=Moves.makeMove(Orion.BN, coordinateMove, 'n');
                Orion.BB=Moves.makeMove(Orion.BB, coordinateMove, 'b');
                Orion.BR=Moves.makeMove(Orion.BR, coordinateMove, 'r');
                Orion.BQ=Moves.makeMove(Orion.BQ, coordinateMove, 'q');
                Orion.BK=Moves.makeMove(Orion.BK, coordinateMove, 'k');
                Orion.WhiteToMove=!Orion.WhiteToMove;
                
                int numPiecesAfter = Rating.bitCount(Orion.WP|Orion.WN|Orion.WB|Orion.WR|Orion.WQ|Orion.WK|Orion.BP|Orion.BN|Orion.BB|Orion.BR|Orion.BQ|Orion.BK);
                if ((numPiecesBefore==numPiecesAfter)&&(Orion.WP==WPBefore)&&(Orion.BP==BPBefore)){
                	Orion.fiftyMoveCounter++;
                }
                else{
                	Orion.fiftyMoveCounter = 0;
                }
	        }
			
			addToHistory();
			Orion.HISTORY2.add(getBoardInformation());
			//BoardGeneration.drawArray(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK);
			//System.out.println();
		}
	}
	
	@SuppressWarnings({ "unchecked", "rawtypes" })
	public static ArrayList getBoardInformation(){
		ArrayList boardInformation = new ArrayList();
		boardInformation.add(Orion.WK);
		boardInformation.add(Orion.WQ);
		boardInformation.add(Orion.WB);
		boardInformation.add(Orion.WN);
		boardInformation.add(Orion.WR);
		boardInformation.add(Orion.WP);
		boardInformation.add(Orion.BK);
		boardInformation.add(Orion.BQ);
		boardInformation.add(Orion.BB);
		boardInformation.add(Orion.BN);
		boardInformation.add(Orion.BR);
		boardInformation.add(Orion.BP);
		boardInformation.add(Orion.EP);
		boardInformation.add(Orion.CWK);
		boardInformation.add(Orion.CWQ);
		boardInformation.add(Orion.CBK);
		boardInformation.add(Orion.CBQ);
		boardInformation.add(Orion.WhiteHasCastled);
		boardInformation.add(Orion.BlackHasCastled);
		boardInformation.add(Orion.WhiteToMove);
		return boardInformation;
	}
	
	//Visualizing Boards
	public static List<Integer> bitPositions(long number) {
		//Get the integer indeces of the ones in a 64 bit long
	    List<Integer> positions = new ArrayList<>();
	    int position;
	    while (number != 0) {
	    	position = Long.numberOfTrailingZeros(number);
	    	positions.add(position);
	    	number = number^(1L<<position);
	    }
	    return positions;
	}
	public static String gridToString(String[][] board){
		//Convert an 8 by 8 array into a string version of a board
		String val = new String();
		val = "\ta\tb\tc\td\te\tf\tg\th\n";
		   for(int i = 0; i < 8; i++){
			   val = val + Integer.toString(8-i);
		      for(int j = 0; j < 8; j++){
		    	  val = val + "\t" + board[i][j];
		      }
		      val = val + "\n";
		   }
		   return val;
		}
	/*
	public String[][] makeFullBoard(){
		//Create an 8x8 array which contains all the pieces of the board
		
		//Make board object and collect pieces
		String[][] board = new String[8][8];
		long[] boardInformation = Arrays.stream(getBoardInformation()).mapToLong(Long::longValue).toArray();
		long [] whitePieces = Arrays.copyOfRange(boardInformation, 0, 6);
		long [] blackPieces = Arrays.copyOfRange(boardInformation, 6, 12);
		String [] pieceTypes = {"K","Q","B","N","R","P"};
		
		//Populate the board
		for (int i=0;i<6;i++){
			long currentPieceWhite = whitePieces[i];
			long currenntPieceBlack = blackPieces[i];
			List<Integer> whitePieceIndeces = bitPositions(currentPieceWhite);
			List<Integer> blackPieceIndeces = bitPositions(currenntPieceBlack);
			for(int j:whitePieceIndeces){
				board[7-(j/8)][(j%8)] = "W"+pieceTypes[i];
			}
			for(int j:blackPieceIndeces){
				board[7-(j/8)][(j%8)] = "B"+pieceTypes[i];
			}
		}
		return board;
	}
	public String toString(){
		//Prints a representation of the board
		String[][] myBoard = this.makeFullBoard();
		return gridToString(myBoard);
	}
	*/
	
	//Types of Boards
    public static void initiateDebugChess() {
        long WP=0L,WN=0L,WB=0L,WR=0L,WQ=0L,WK=0L,BP=0L,BN=0L,BB=0L,BR=0L,BQ=0L,BK=0L;
        String chessBoard[][]={
                {"r","q","q","q","k","b","n","r"},
                {"p","p","p","p","p","p","p","p"},
                {" "," "," "," "," "," "," "," "},
                {" "," "," "," "," "," "," "," "},
                {" "," "," "," "," "," "," "," "},
                {" "," "," "," ","P"," "," "," "},
                {"P","P","P","P"," ","P","P","P"},
                {"R","Q","Q","Q","K","B","N","R"}};
        arrayToBitboards(chessBoard,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK);
        String fenBoard = makeHistoryFEN(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove,Orion.fiftyMoveCounter,Orion.moveCounter);
        //Orion.HISTORY = new ArrayList<String> ();
        //Orion.HISTORY.add(fenBoard);
        Orion.ThreeMoveRep = new HashMap<String,Integer> ();
        Orion.ThreeMoveRep.put(fenBoard, 1);
        long boardHash = Zobrist.getZobristHash(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove);
        Orion.ThreeMoveRepCheck = new HashMap<Long,Integer> ();
        Orion.ThreeMoveRepCheck.put(boardHash, 1);
    }
    public static void initiateStandardChess() {
        long WP=0L,WN=0L,WB=0L,WR=0L,WQ=0L,WK=0L,BP=0L,BN=0L,BB=0L,BR=0L,BQ=0L,BK=0L;
        String chessBoard[][]={
                {"r","n","b","q","k","b","n","r"},
                {"p","p","p","p","p","p","p","p"},
                {" "," "," "," "," "," "," "," "},
                {" "," "," "," "," "," "," "," "},
                {" "," "," "," "," "," "," "," "},
                {" "," "," "," "," "," "," "," "},
                {"P","P","P","P","P","P","P","P"},
                {"R","N","B","Q","K","B","N","R"}};
        arrayToBitboards(chessBoard,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK);
        String fenBoard = makeHistoryFEN(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove,Orion.fiftyMoveCounter,Orion.moveCounter);
        //Orion.HISTORY = new ArrayList<String> ();
        //Orion.HISTORY.add(fenBoard);
        Orion.ThreeMoveRep = new HashMap<String,Integer> ();
        Orion.ThreeMoveRep.put(fenBoard, 1);
        long boardHash = Zobrist.getZobristHash(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove);
        Orion.ThreeMoveRepCheck = new HashMap<Long,Integer> ();
        Orion.ThreeMoveRepCheck.put(boardHash, 1);
    }
    public static void initiateChess960() {
    	long WP=0L,WN=0L,WB=0L,WR=0L,WQ=0L,WK=0L,BP=0L,BN=0L,BB=0L,BR=0L,BQ=0L,BK=0L;
        String chessBoard[][]={
            {" "," "," "," "," "," "," "," "},
            {"p","p","p","p","p","p","p","p"},
            {" "," "," "," "," "," "," "," "},
            {" "," "," "," "," "," "," "," "},
            {" "," "," "," "," "," "," "," "},
            {" "," "," "," "," "," "," "," "},
            {"P","P","P","P","P","P","P","P"},
            {" "," "," "," "," "," "," "," "}};
        //step 1:
        int random1=(int)(Math.random()*8);
        chessBoard[0][random1]="b";
        chessBoard[7][random1]="B";
        //step 2:
        int random2=(int)(Math.random()*8);
        while (random2%2==random1%2) {
            random2=(int)(Math.random()*8);
        }
        chessBoard[0][random2]="b";
        chessBoard[7][random2]="B";
        //step 3:
        int random3=(int)(Math.random()*8);
        while (random3==random1 || random3==random2) {
            random3=(int)(Math.random()*8);
        }
        chessBoard[0][random3]="q";
        chessBoard[7][random3]="Q";
        //step 4:
        int random4a=(int)(Math.random()*5);
        int counter=0;
        int loop=0;
        while (counter-1<random4a) {
            if (" ".equals(chessBoard[0][loop])) {counter++;}
            loop++;
        }
        chessBoard[0][loop-1]="n";
        chessBoard[7][loop-1]="N";
        int random4b=(int)(Math.random()*4);
        counter=0;
        loop=0;
        while (counter-1<random4b) {
            if (" ".equals(chessBoard[0][loop])) {counter++;}
            loop++;
        }
        chessBoard[0][loop-1]="n";
        chessBoard[7][loop-1]="N";
        //step 5:
        counter=0;
        while (!" ".equals(chessBoard[0][counter])) {
            counter++;
        }
        chessBoard[0][counter]="r";
        chessBoard[7][counter]="R";
        while (!" ".equals(chessBoard[0][counter])) {
            counter++;
        }
        chessBoard[0][counter]="k";
        chessBoard[7][counter]="K";
        while (!" ".equals(chessBoard[0][counter])) {
            counter++;
        }
        chessBoard[0][counter]="r";
        chessBoard[7][counter]="R";
        arrayToBitboards(chessBoard,WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK);
        String fenBoard = makeHistoryFEN(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove,Orion.fiftyMoveCounter,Orion.moveCounter);
        //Orion.HISTORY = new ArrayList<String> ();
        //Orion.HISTORY.add(fenBoard);
        Orion.ThreeMoveRep = new HashMap<String,Integer> ();
        Orion.ThreeMoveRep.put(fenBoard, 1);
        long boardHash = Zobrist.getZobristHash(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove);
        Orion.ThreeMoveRepCheck = new HashMap<Long,Integer> ();
        Orion.ThreeMoveRepCheck.put(boardHash, 1);
    }
    
    public static void importFEN(String fenString){
        //not chess960 compatible
    	//Examples:
    	// rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    	// rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2
		Orion.HISTORY2 = new ArrayList<ArrayList>();
	    Orion.WhiteHasCastled = false;
	    Orion.BlackHasCastled = false;
    	Orion.WP=0; Orion.WN=0; Orion.WB=0;
    	Orion.WR=0; Orion.WQ=0; Orion.WK=0;
    	Orion.BP=0; Orion.BN=0; Orion.BB=0;
    	Orion.BR=0; Orion.BQ=0; Orion.BK=0;
    	Orion.CWK=false; Orion.CWQ=false;
        Orion.CBK=false; Orion.CBQ=false;
		int charIndex = 0;
		int boardIndex = 0;
		//trueBoardIndex = (7-boardIndex/8)*8 + boardIndex%8;
		while (fenString.charAt(charIndex) != ' ')
		{
			switch (fenString.charAt(charIndex++))
			{
			case 'P':
				Orion.WP |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'p':
				Orion.BP |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'N':
				Orion.WN |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'n':
				Orion.BN |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'B':
				Orion.WB |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'b':
				Orion.BB |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'R':
				Orion.WR |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'r':
				Orion.BR |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'Q':
				Orion.WQ |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'q':
				Orion.BQ |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'K':
				Orion.WK |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'k':
				Orion.BK |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case '/':
				break;
			case '1': boardIndex++;
				break;
			case '2': boardIndex += 2;
				break;
			case '3': boardIndex += 3;
				break;
			case '4': boardIndex += 4;
				break;
			case '5': boardIndex += 5;
				break;
			case '6': boardIndex += 6;
				break;
			case '7': boardIndex += 7;
				break;
			case '8': boardIndex += 8;
				break;
			default:
				break;
			}
		}
		Orion.WhiteToMove = (fenString.charAt(++charIndex) == 'w');
		charIndex += 2;
		while (fenString.charAt(charIndex) != ' ')
		{
			switch (fenString.charAt(charIndex++))
			{
			case '-':
				break;
			case 'K': Orion.CWK = true;
				break;
			case 'Q': Orion.CWQ = true;
				break;
			case 'k': Orion.CBK = true;
				break;
			case 'q': Orion.CBQ = true;
				break;
			default:
				break;
			}
		}
		if (fenString.charAt(++charIndex) != '-')
		{
			Orion.EP = Moves.FileMasks8[fenString.charAt(charIndex++) - 'a'];
		}
		charIndex+=2;
		int charIndex2 = fenString.indexOf(' ', charIndex+1);
		Orion.fiftyMoveCounter = Integer.parseInt(fenString.substring(charIndex, charIndex2));
		charIndex = charIndex2+1;
		if (fenString.substring(charIndex).contains(" ")){
			charIndex2 = fenString.indexOf(' ', charIndex);
		}
		else{
			charIndex2 = fenString.length();
		}
		Orion.moveCounter = Integer.parseInt(fenString.substring(charIndex, charIndex2));
		//The move counter starts at one and increments after blacks first move. So just start at 0 if white hasn't gone yet
		if ((Orion.moveCounter==1)&&Orion.WhiteToMove){
			Orion.moveCounter = 0;
		}
        String fenBoard = makeHistoryFEN(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove,Orion.fiftyMoveCounter,Orion.moveCounter);
        //Orion.HISTORY = new ArrayList<String> ();
        //Orion.HISTORY.add(fenBoard);
        Orion.ThreeMoveRep = new HashMap<String,Integer> ();
        Orion.ThreeMoveRep.put(fenBoard, 1);
        long boardHash = Zobrist.getZobristHash(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove);
        Orion.ThreeMoveRepCheck = new HashMap<Long,Integer> ();
        Orion.ThreeMoveRepCheck.put(boardHash, 1);
        Orion.HISTORY2.add(getBoardInformation());
    }
    
    //Helper Functions
    public static void arrayToBitboards(String[][] chessBoard,long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK) {
        String Binary;
        for (int i=0;i<64;i++) {
            Binary="0000000000000000000000000000000000000000000000000000000000000000";
            Binary=Binary.substring(i+1)+"1"+Binary.substring(0, i);
            switch (chessBoard[7-i/8][i%8]) {
                case "P": WP+=convertStringToBitboard(Binary);
                    break;
                case "N": WN+=convertStringToBitboard(Binary);
                    break;
                case "B": WB+=convertStringToBitboard(Binary);
                    break;
                case "R": WR+=convertStringToBitboard(Binary);
                    break;
                case "Q": WQ+=convertStringToBitboard(Binary);
                    break;
                case "K": WK+=convertStringToBitboard(Binary);
                    break;
                case "p": BP+=convertStringToBitboard(Binary);
                    break;
                case "n": BN+=convertStringToBitboard(Binary);
                    break;
                case "b": BB+=convertStringToBitboard(Binary);
                    break;
                case "r": BR+=convertStringToBitboard(Binary);
                    break;
                case "q": BQ+=convertStringToBitboard(Binary);
                    break;
                case "k": BK+=convertStringToBitboard(Binary);
                    break;
            }
        }
        drawArray(WP,WN,WB,WR,WQ,WK,BP,BN,BB,BR,BQ,BK);
        Orion.WP=WP; Orion.WN=WN; Orion.WB=WB;
        Orion.WR=WR; Orion.WQ=WQ; Orion.WK=WK;
        Orion.BP=BP; Orion.BN=BN; Orion.BB=BB;
        Orion.BR=BR; Orion.BQ=BQ; Orion.BK=BK;
    }
    public static long convertStringToBitboard(String Binary) {
        if (Binary.charAt(0)=='0') {//not going to be a negative number
            return Long.parseLong(Binary, 2);
        } else {
            return Long.parseLong("1"+Binary.substring(2), 2)*2;
        }
    }
	public static void drawArray(long WP, long WN, long WB, long WR, long WQ, long WK, long BP, long BN,
			long BB, long BR, long BQ, long BK) {
        String chessBoard[][]=new String[8][8];
        for (int i=0;i<64;i++) {
            chessBoard[i/8][i%8]=" ";
        }
        for (int i=0;i<64;i++) {
            if (((WP>>i)&1)==1) {chessBoard[7-i/8][i%8]="P";}
            if (((WN>>i)&1)==1) {chessBoard[7-i/8][i%8]="N";}
            if (((WB>>i)&1)==1) {chessBoard[7-i/8][i%8]="B";}
            if (((WR>>i)&1)==1) {chessBoard[7-i/8][i%8]="R";}
            if (((WQ>>i)&1)==1) {chessBoard[7-i/8][i%8]="Q";}
            if (((WK>>i)&1)==1) {chessBoard[7-i/8][i%8]="K";}
            if (((BP>>i)&1)==1) {chessBoard[7-i/8][i%8]="p";}
            if (((BN>>i)&1)==1) {chessBoard[7-i/8][i%8]="n";}
            if (((BB>>i)&1)==1) {chessBoard[7-i/8][i%8]="b";}
            if (((BR>>i)&1)==1) {chessBoard[7-i/8][i%8]="r";}
            if (((BQ>>i)&1)==1) {chessBoard[7-i/8][i%8]="q";}
            if (((BK>>i)&1)==1) {chessBoard[7-i/8][i%8]="k";}
        }
        for (int i=0;i<8;i++) {
            System.out.println(Arrays.toString(chessBoard[i]));
        }
	}
	@SuppressWarnings("rawtypes")
	public static void drawArray(ArrayList boardInformation) {
		long WK = (long) boardInformation.get(0),WQ = (long) boardInformation.get(1),
				WB = (long) boardInformation.get(2),WN = (long) boardInformation.get(3),
				WR = (long) boardInformation.get(4),WP = (long) boardInformation.get(5),
				BK = (long) boardInformation.get(6),BQ = (long) boardInformation.get(7),
				BB = (long) boardInformation.get(8),BN = (long) boardInformation.get(9),
				BR = (long) boardInformation.get(10),BP = (long) boardInformation.get(11);
        String chessBoard[][]=new String[8][8];
        for (int i=0;i<64;i++) {
            chessBoard[i/8][i%8]=" ";
        }
        for (int i=0;i<64;i++) {
            if (((WP>>i)&1)==1) {chessBoard[7-i/8][i%8]="P";}
            if (((WN>>i)&1)==1) {chessBoard[7-i/8][i%8]="N";}
            if (((WB>>i)&1)==1) {chessBoard[7-i/8][i%8]="B";}
            if (((WR>>i)&1)==1) {chessBoard[7-i/8][i%8]="R";}
            if (((WQ>>i)&1)==1) {chessBoard[7-i/8][i%8]="Q";}
            if (((WK>>i)&1)==1) {chessBoard[7-i/8][i%8]="K";}
            if (((BP>>i)&1)==1) {chessBoard[7-i/8][i%8]="p";}
            if (((BN>>i)&1)==1) {chessBoard[7-i/8][i%8]="n";}
            if (((BB>>i)&1)==1) {chessBoard[7-i/8][i%8]="b";}
            if (((BR>>i)&1)==1) {chessBoard[7-i/8][i%8]="r";}
            if (((BQ>>i)&1)==1) {chessBoard[7-i/8][i%8]="q";}
            if (((BK>>i)&1)==1) {chessBoard[7-i/8][i%8]="k";}
        }
        for (int i=0;i<8;i++) {
            System.out.println(Arrays.toString(chessBoard[i]));
        }
	}
	public static String makeHistoryFEN(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int fiftyMoveCounter,int totalMoveCounter){
		//Examples:
		// rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
		// rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2
		// r1bqkb2/2pp1p1r/p3p2p/1p2n1pn/NPP1PP2/3P4/P1Q1N1PP/R1B1KB1R w KQq - 1 11
		String fenString = "";

		//trueBoardIndex = (7-boardIndex/8)*8 + boardIndex%8;
		int emptySquareCounter = 0;
		for (int boardIndex=0;boardIndex<64;boardIndex++){
			if ((WP>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'P';
			}
			else if ((BP>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'p';
			}
			else if ((WN>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'N';
			}
			else if ((BN>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'n';
			}
			else if ((WB>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'B';
			}
			else if ((BB>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'b';
			}
			else if ((WR>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'R';
			}
			else if ((BR>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'r';
			}
			else if ((WQ>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'Q';
			}
			else if ((BQ>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'q';
			}
			else if ((WK>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'K';
			}
			else if ((BK>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'k';
			}
			else{
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					if (emptySquareCounter!=0){
						fenString = fenString + emptySquareCounter + '/';
						emptySquareCounter = 0;
					}
					else{
						fenString += '/';
					}
				}
				emptySquareCounter++;
				if (boardIndex==63){
					fenString+=emptySquareCounter;
				}
			}
		}
		
		if (WhiteToMove){
			fenString +=" w ";
		}
		else{
			fenString +=" b ";
		}
		
		if (!(CWK|CWQ|CBK|CBQ)){
			fenString += "-";
		}
		if (CWK){
			fenString += "K";
		}
		if (CWQ){
			fenString += "Q";
		}
		if (CBK){
			fenString += "k";
		}
		if (CBQ){
			fenString += "q";
		}
		
		//Commented out En Passant because the engine doesn't consider en passant.
		/*
		//En Passant
		if (EP==0){
			fenString = fenString + " -";
		}
		else{
			int EPfile = Long.numberOfTrailingZeros(EP);
			fenString = fenString + (char)('a' + EPfile);
		}
		*/
		//Commented out moves because not relevant
		//fenString = fenString + " " + fiftyMoveCounter + " " + totalMoveCounter;
		
		return fenString;
	}
	/*
	public static boolean check3FoldRep(String fenBoard){
		int count = 0;
		for (int i=0;i<Orion.HISTORY.size();i++){
			if (Orion.HISTORY.get(i).startsWith(fenBoard)){
				count++;
			}
			if (count >=3){
				return true;
			}
		}
		return false;
	}*/
	public static String makeFullFEN(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ,boolean WhiteToMove,int fiftyMoveCounter,int totalMoveCounter){
		//Examples:
		// rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
		// rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2
		// r1bqkb2/2pp1p1r/p3p2p/1p2n1pn/NPP1PP2/3P4/P1Q1N1PP/R1B1KB1R w KQq - 1 11
		String fenString = "";

		//trueBoardIndex = (7-boardIndex/8)*8 + boardIndex%8;
		int emptySquareCounter = 0;
		for (int boardIndex=0;boardIndex<64;boardIndex++){
			if ((WP>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'P';
			}
			else if ((BP>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'p';
			}
			else if ((WN>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'N';
			}
			else if ((BN>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'n';
			}
			else if ((WB>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'B';
			}
			else if ((BB>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'b';
			}
			else if ((WR>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'R';
			}
			else if ((BR>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'r';
			}
			else if ((WQ>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'Q';
			}
			else if ((BQ>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'q';
			}
			else if ((WK>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'K';
			}
			else if ((BK>>>((7-boardIndex/8)*8 + boardIndex%8)&1)==1){
				if (emptySquareCounter!=0){
					fenString += emptySquareCounter;
					emptySquareCounter = 0;
				}
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					fenString += '/';
				}
				fenString += 'k';
			}
			else{
				if ((boardIndex%8==0)&&(boardIndex!=0)){
					if (emptySquareCounter!=0){
						fenString = fenString + emptySquareCounter + '/';
						emptySquareCounter = 0;
					}
					else{
						fenString += '/';
					}
				}
				emptySquareCounter++;
				if (boardIndex==63){
					fenString+=emptySquareCounter;
				}
			}
		}
		
		if (WhiteToMove){
			fenString +=" w ";
		}
		else{
			fenString +=" b ";
		}
		
		if (!(CWK|CWQ|CBK|CBQ)){
			fenString += "-";
		}
		if (CWK){
			fenString += "K";
		}
		if (CWQ){
			fenString += "Q";
		}
		if (CBK){
			fenString += "k";
		}
		if (CBQ){
			fenString += "q";
		}
		
		//En Passant
		if (EP==0){
			fenString = fenString + " -";
		}
		else{
			int EPfile = Long.numberOfTrailingZeros(EP);
			fenString = fenString + (char)('a' + EPfile);
		}
		fenString = fenString + " " + fiftyMoveCounter + " " + totalMoveCounter;
		
		return fenString;
		
	}
	public static void addToHistory(){
        /*
		String fenBoard = makeHistoryFEN(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove,Orion.fiftyMoveCounter,Orion.moveCounter);
        Orion.HISTORY.add(fenBoard);
        if (Orion.ThreeMoveRep.containsKey(fenBoard)){
        	Orion.ThreeMoveRep.put(fenBoard, Orion.ThreeMoveRep.get(fenBoard)+1);
        }
        else{
        	Orion.ThreeMoveRep.put(fenBoard, 1);
        }
        */
		Long boardHash = Zobrist.getZobristHash(Orion.WP,Orion.WN,Orion.WB,Orion.WR,Orion.WQ,Orion.WK,Orion.BP,Orion.BN,Orion.BB,Orion.BR,Orion.BQ,Orion.BK,Orion.EP,Orion.CWK,Orion.CWQ,Orion.CBK,Orion.CBQ,Orion.WhiteToMove);
        if (Orion.ThreeMoveRepCheck.containsKey(boardHash)){
        	Orion.ThreeMoveRepCheck.put(boardHash, Orion.ThreeMoveRepCheck.get(boardHash)+1);
        }
        else{
        	Orion.ThreeMoveRepCheck.put(boardHash, 1);
        }
        
	}
}
