import org.junit.Test;

public class ChessTest {

	@Test
	public void testTrue() {
		assert(true);
		//fail("Not yet implemented");
		//assertEquals(1,1);
		
	}
	// Tests
	
	@Test
	public void testMoves1() {
		String fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==119060324);
	}
	
	@Test
	public void testMoves2() {
		String fenString = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 5;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==193690690);
	}
	@Test
	public void testMoves3() {
		String fenString = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 7;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==178633661);
	}
	
	@Test
	public void testMoves4() {
		String fenString = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==706045033);
	}
	
	
	@Test
	public void testMoves5() {
		String fenString = "1k6/1b6/8/8/7R/8/8/4K2R b K - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 5;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==1063513);
	}
	
	//TalkChess PERFT Tests (by Martin Sedlak)
	@Test
	public void testMoves6() {
		String fenString = "3k4/3p4/8/K1P4r/8/8/8/8 b - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==1134888);
	}
	@Test
	public void testMoves7() {
		String fenString = "8/8/4k3/8/2p5/8/B2P2K1/8 w - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==1015133);
	}
	@Test
	public void testMoves8() {
		String fenString = "8/8/1k6/2b5/2pP4/8/5K2/8 b - d3 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==1440467);
	}
	@Test
	public void testMoves9() {
		String fenString = "5k2/8/8/8/8/8/8/4K2R w K - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==661072);
	}
	
	@Test
	public void testMoves10() {
		String fenString = "3k4/8/8/8/8/8/8/R3K3 w Q - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==803711);
	}
	@Test
	public void testMoves11() {
		String fenString = "r3k2r/1b4bq/8/8/8/8/7B/R3K2R w KQkq - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 4;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==1274206);
	}
	@Test
	public void testMoves12() {
		String fenString = "r3k2r/8/3Q4/8/8/5q2/8/R3K2R b KQkq - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 4;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==1720476);
	}
	@Test
	public void testMoves13() {
		String fenString = "2K2r2/4P3/8/8/8/8/8/3k4 w - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==3821001);
	}
	@Test
	public void testMoves14() {
		String fenString = "8/8/1P2K3/8/2n5/1q6/8/5k2 b - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 5;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==1004658);
	}
	@Test
	public void testMoves15() {
		String fenString = "4k3/1P6/8/8/8/8/K7/8 w - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==217342);
	}
	@Test
	public void testMoves16() {
		String fenString = "8/P1k5/K7/8/8/8/8/8 w - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==92683);
	}
	@Test
	public void testMoves17() {
		String fenString = "K1k5/8/P7/8/8/8/8/8 w - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 6;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==2217);
	}
	@Test
	public void testMoves18() {
		String fenString = "8/k1P5/8/1K6/8/8/8/8 w - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 7;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==567584);
	}
	@Test
	public void testMoves19() {
		String fenString = "8/8/2k5/5q2/5n2/8/5K2/8 b - - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 4;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==23527);
	}
	
	//Remove castling rights after pawn promotion
	@Test
	public void testMoves20() {
		String fenString = "r3k3/1P6/8/r7/8/8/4PPPP/4KBNR w Kq - 0 1";
		BoardGeneration.importFEN(fenString);
		Perft.perftMaxDepth = 5;
		Perft.perftRoot(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, 0,false);
		assert(Perft.perftTotalMoveCounter==2874505);
	}
	
	
	//Testing fen generation
	@Test
	public void testMoves21() {
		String fenString = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
		BoardGeneration.importFEN(fenString);
		String output = BoardGeneration.makeHistoryFEN(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, Orion.fiftyMoveCounter, Orion.moveCounter);
		assert(fenString.startsWith(output));
	}
	@Test
	public void testMoves22() {
		String fenString = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2";
		BoardGeneration.importFEN(fenString);
		String output = BoardGeneration.makeHistoryFEN(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, Orion.fiftyMoveCounter, Orion.moveCounter);
		assert(fenString.startsWith(output));
	}
	@Test
	public void testMoves23() {
		String fenString = "r1bqkb2/2pp1p1r/p3p2p/1p2n1pn/NPP1PP2/3P4/P1Q1N1PP/R1B1KB1R w KQq - 1 11";
		BoardGeneration.importFEN(fenString);
		String output = BoardGeneration.makeHistoryFEN(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, Orion.fiftyMoveCounter, Orion.moveCounter);
		assert(fenString.startsWith(output));
	}
	@Test
	public void testMoves24() {
		String fenString = "8/6k1/8/8/8/8/3q1bp1/K7 b - - 2 1";
		BoardGeneration.importFEN(fenString);
		String output = BoardGeneration.makeHistoryFEN(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, Orion.fiftyMoveCounter, Orion.moveCounter);
		assert(fenString.startsWith(output));
	}
	@Test
	public void testMoves25() {
		String fenString = "k7/3Q1BP1/8/8/8/8/6K1/8 w - - 2 1";
		BoardGeneration.importFEN(fenString);
		String output = BoardGeneration.makeHistoryFEN(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, Orion.fiftyMoveCounter, Orion.moveCounter);
		assert(fenString.startsWith(output));
	}
	@Test
	public void testMoves26() {
		String fenString = "rnbk1Q2/8/4p3/pBB1Np2/P7/2P5/5PPP/R4K1R b - - 0 28";
		BoardGeneration.importFEN(fenString);
		String output = BoardGeneration.makeHistoryFEN(Orion.WP, Orion.WN, Orion.WB, Orion.WR, Orion.WQ, Orion.WK, Orion.BP, Orion.BN, Orion.BB, Orion.BR, Orion.BQ, Orion.BK, Orion.EP, Orion.CWK, Orion.CWQ, Orion.CBK, Orion.CBQ, Orion.WhiteToMove, Orion.fiftyMoveCounter, Orion.moveCounter);
		assert(fenString.startsWith(output));
	}
	
}
