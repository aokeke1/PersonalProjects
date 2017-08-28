import java.util.HashMap;
import java.util.HashSet;

public class TranspositionTable {
	public static HashSet<Long> allKeys = new HashSet<Long>();

	public static HashMap<Long,HashMap> transpositionTable = new HashMap<Long,HashMap>();
	
	
	@SuppressWarnings({ "unchecked", "rawtypes" })
	public static void addValue(long key,int depth,String flag,int value){
		allKeys.add(key);
		HashMap info = new HashMap();
		info.put("FLAG", flag);
		info.put("VALUE", value);
		info.put("DEPTH", depth);
		transpositionTable.put(key, info);
	}
	
	public static boolean contains(long key){
		return allKeys.contains(key);
	}
	public static int getValue(long key){
		return (int) transpositionTable.get(key).get("VALUE");
	}
	public static String getFlag(long key){
		return (String) transpositionTable.get(key).get("FLAG");
	}
	public static int getDepth(long key){
		return (int) transpositionTable.get(key).get("DEPTH");
	}

}
