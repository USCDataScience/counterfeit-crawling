package solr.update.serials;

import org.apache.solr.client.solrj.SolrServer;
import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrServer;
import org.apache.solr.common.SolrDocument;
import org.apache.solr.common.SolrInputDocument;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import javax.script.ScriptException;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.FileReader;
import java.io.FileNotFoundException;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.Iterator;
import java.util.stream.Collectors;

public class SolrUpdateSerials {
    
    public interface Transformer{
        SolrInputDocument transform(JSONObject doc);
    }

    public static final Logger LOG = LoggerFactory.getLogger(SolrUpdateSerials.class);
    
    @Option(name = "-conf", usage = "Config Properties File", required = true)
	private File configFile;
    
    @Option(name = "-path", usage = "Path to JSON File", required = true)
	private String filePath;

    private SolrServer solrServer;
    // private SolrDocIterator iterator;
    private Transformer transformer;

    private int batch = 100;
    
    private void init(String[] args) throws IOException {
	CmdLineParser parser = new CmdLineParser(this);
        try {
            parser.parseArgument(args);
        } catch (CmdLineException e) {
            System.out.println(e.getMessage());
            parser.printUsage(System.out);
            System.exit(1);
        }

	Properties props = new Properties();
        try (InputStream stream = new FileInputStream(configFile)){
		props.load(stream);
	    }
        String solrUrl = props.getProperty("solr.url");
        LOG.info("Solr Server {}", solrUrl);
        this.solrServer = new HttpSolrServer(solrUrl);
        String qry = props.getProperty("solr.qry");
        LOG.info("Query {}", qry);
        String fields = props.getProperty("solr.fl", "").trim();
        String [] fls = null;
        if (!fields.isEmpty()) {
            LOG.info("Fields {}", fields);
            fls = fields.split(",");
        }
        int start = Integer.parseInt(props.getProperty("solr.start", "0"));
        batch = Integer.parseInt(props.getProperty("solr.rows", "100"));
        LOG.info("start {}, rows {}", start, batch);
        String sort = props.getProperty("solr.sort", "").trim();
        LOG.info("Sort {}", sort);
	
    }
    
    public void update() throws IOException, SolrServerException{
	List<SolrInputDocument> buffer = new ArrayList<>(batch);
	long count = 0;
        long batches = 0;
        long skipped = 0;
        long logDelay = 2000;
        long st = System.currentTimeMillis();
	
	JSONParser parser = new JSONParser();
	try {
	    FileReader reader = new FileReader(filePath);
	    
	    JSONObject jsonObject = (JSONObject) parser.parse(reader);
	    
	    Set keys = jsonObject.keySet();
	    Iterator fields = keys.iterator();
	    while (fields.hasNext()) {
		String domain = (String) fields.next();
		
		JSONArray serials = (JSONArray) jsonObject.get(domain);
		Iterator i = serials.iterator();
		while (i.hasNext()) {
		    JSONObject next = (JSONObject) i.next();
		    
		    LOG.info("Image ID {}", next.get("image_id"));
		    SolrInputDocument result = transformer.transform(next);
		    if (result == null) {
		    	skipped++;
		    	continue;
		    }
		    count++;
		    buffer.add(result);
		    
		    if (buffer.size() > batch) {
			try {
			    batches++;
			    solrServer.add(buffer);
			    buffer.clear();
			    System.out.println(count);
			} catch (SolrServerException | IOException e) {
			    System.err.println(e.getMessage());
			    LOG.error(e.getMessage(), e);
			    LOG.error("Last Document = {}, == {}", next.get("id"), result);
			}
		    }
		    
		    if (System.currentTimeMillis() - st > logDelay) {
			LOG.info("Count = {}, skipped = {}, batches = {}. Last added = {}",
				 count, skipped, batches, next.get("id"));
			st = System.currentTimeMillis();
		    }
		}
		if (!buffer.isEmpty()){
		    solrServer.add(buffer);
		}
		LOG.info("Committing before exit");
		solrServer.commit();
		LOG.info("!Done!");
				      
	    }
	    
	} catch (FileNotFoundException e) {
	    e.printStackTrace();
	    LOG.error(e.getMessage(), e);
	} catch (ParseException e) {
	    e.printStackTrace();
	    LOG.error(e.getMessage(), e);
	}
    }
    
    { 
	transformer = new Transformer() {	
		@Override
		public SolrInputDocument transform(JSONObject doc) {
		    SolrInputDocument ret = new SolrInputDocument();
		    
		    String id = doc.get("image_id").toString();
		    ret.setField("id", id);
		    
		    List<String> serials = (ArrayList) doc.get("extracted_serials");
		    ret.setField("extracted_serials_ss", new HashMap<String, Object>(){{put("set", serials);}});
		    
		    return ret;
		}	
	    };
    }
	
    
    public static void main(String[] args) {
    	try {
    		SolrUpdateSerials update = new SolrUpdateSerials();
    		update.init(args);
    		update.update();
    		System.out.println("Done");
    	}
    	catch (Exception e) {
    		e.printStackTrace();
    	}
    }

}