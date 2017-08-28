import java.util.ArrayList;
import java.util.HashMap;

public class BoardObject {
	// Pieces
    long WP=0L,WN=0L,WB=0L,WR=0L,WQ=0L,WK=0L,BP=0L,BN=0L,BB=0L,BR=0L,BQ=0L,BK=0L,EP=0L;
    //Castling Rights and whose turn it is
    boolean CWK=true,CWQ=true,CBK=true,CBQ=true,WhiteToMove=true;//true=castle is possible
    int fiftyMoveCounter=0,moveCounter=0;
    public BoardObject() {
    	inputFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    }
    public BoardObject(String fenString) {
    	inputFen(fenString);
    }
    public BoardObject(long WP,long WN,long WB,long WR,long WQ,long WK,long BP,long BN,long BB,long BR,long BQ,long BK,long EP,boolean CWK,boolean CWQ,boolean CBK,boolean CBQ) {
    	this.WP=WP; this.WN=WN; this.WB=WB;
    	this.WR=WR; this.WQ=WQ; this.WK=WK;
    	this.BP=BP; this.BN=BN; this.BB=BB;
    	this.BR=BR; this.BQ=BQ; this.BK=BK;
    	this.EP = EP;
    	this.CWK=CWK; this.CWQ=CWQ;
        this.CBK=CBK; this.CBQ=CBQ;
    }
    public void inputFen(String fenString){
        //not chess960 compatible
    	//Examples:
    	// rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    	// rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2
    	this.WP=0; this.WN=0; this.WB=0;
    	this.WR=0; this.WQ=0; this.WK=0;
    	this.BP=0; this.BN=0; this.BB=0;
    	this.BR=0; this.BQ=0; this.BK=0;
    	this.CWK=false; this.CWQ=false;
        this.CBK=false; this.CBQ=false;
		int charIndex = 0;
		int boardIndex = 0;
		//trueBoardIndex = (7-boardIndex/8)*8 + boardIndex%8;
		while (fenString.charAt(charIndex) != ' ')
		{
			switch (fenString.charAt(charIndex++))
			{
			case 'P':
				this.WP |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'p':
				this.BP |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'N':
				this.WN |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'n':
				this.BN |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'B':
				this.WB |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'b':
				this.BB |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'R':
				this.WR |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'r':
				this.BR |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'Q':
				this.WQ |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'q':
				this.BQ |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'K':
				this.WK |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
				boardIndex++;
				break;
			case 'k':
				this.BK |= (1L << ((7-boardIndex/8)*8 + boardIndex%8));
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
		this.WhiteToMove = (fenString.charAt(++charIndex) == 'w');
		charIndex += 2;
		while (fenString.charAt(charIndex) != ' ')
		{
			switch (fenString.charAt(charIndex++))
			{
			case '-':
				break;
			case 'K': this.CWK = true;
				break;
			case 'Q': this.CWQ = true;
				break;
			case 'k': this.CBK = true;
				break;
			case 'q': this.CBQ = true;
				break;
			default:
				break;
			}
		}
		if (fenString.charAt(++charIndex) != '-')
		{
			this.EP = Moves.FileMasks8[fenString.charAt(charIndex++) - 'a'];
		}
		charIndex+=2;
		int charIndex2 = fenString.indexOf(' ', charIndex+1);
		this.fiftyMoveCounter = Integer.parseInt(fenString.substring(charIndex, charIndex2));
		charIndex = charIndex2+1;
		if (fenString.substring(charIndex).contains(" ")){
			charIndex2 = fenString.indexOf(' ', charIndex);
		}
		else{
			charIndex2 = fenString.length();
		}
		this.moveCounter = Integer.parseInt(fenString.substring(charIndex, charIndex2));
		//The move counter starts at one and increments after blacks first move. So just start at 0 if white hasn't gone yet
		if ((this.moveCounter==1)&&this.WhiteToMove){
			this.moveCounter = 0;
		}
    }
}
