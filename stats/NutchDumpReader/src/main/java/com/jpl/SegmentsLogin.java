package com.jpl;

import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang.StringUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.io.FileUtils;
import org.apache.hadoop.io.MD5Hash;

import java.util.Arrays;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;

import java.lang.String;
import java.lang.StringBuilder;

import java.net.URL;
import java.net.MalformedURLException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


public class SegmentsLogin {
    private final static Integer MAX_LENGTH_OF_FILENAME = 32;
    private final static Integer MAX_LENGTH_OF_EXTENSION = 5; 
    
    private static void reverseAppendSplits(String string, StringBuilder buf) {
	String[] splits = StringUtils.split(string, ".");
	if (splits.length > 0) {
	    for (int i = splits.length - 1; i > 0; i--) {
		buf.append(splits[i]);
		buf.append('.');
	    }
	    buf.append(splits[0]);
	} else {
	    buf.append(string);
	}
    }
    
    private static String reverseUrl(String stringUrl) throws MalformedURLException{
	URL url;
	
	try {
	    url = new URL(stringUrl);
	}
	catch (MalformedURLException e) {
	    return "";
	}
	
	String host = url.getHost();
	String file = url.getFile();
	String protocol = url.getProtocol();
	int port = url.getPort();

	StringBuilder buf = new StringBuilder();

	/* reverse host */
	reverseAppendSplits(host, buf);

	/* add protocol */
	buf.append(':');
	buf.append(protocol);

	/* add port if necessary */
	if (port != -1) {
	    buf.append(':');
	    buf.append(port);
	}

	/* add path */
	if (file.length() > 0 && '/' != file.charAt(0)) {
	    buf.append('/');
	}
	buf.append(file);

	return buf.toString();
    }


    public static String getReversedOutputPath(String url) throws MalformedURLException {
	String fullDir = "/data3/memex/counterfeit-electronics/dump/full/";

        String[] reversedURL = reverseUrl(url).split(":");
	
	reversedURL[0] = reversedURL[0].replace('.', '/');
	
	String reversedURLPath = reversedURL[0] + "/" + DigestUtils.sha256Hex(url).toUpperCase();
	
	String outputFullPath = String.format("%s/%s", fullDir, reversedURLPath);
	return outputFullPath;
    }
    

    private static String getUrlMD5(String url) {
        byte[] digest = MD5Hash.digest(url).getDigest();

        StringBuffer sb = new StringBuffer();
        for (byte b : digest) {
            sb.append(String.format("%02x", b & 0xff));
        }

        return sb.toString();
    }

    private static String createFileName(String md5, String fileBaseName, String fileExtension) {
        if (fileBaseName.length() > MAX_LENGTH_OF_FILENAME) {
            System.out.println("File name is too long. Truncated to {} characters.", MAX_LENGTH_OF_FILENAME);
            fileBaseName = StringUtils.substring(fileBaseName, 0, MAX_LENGTH_OF_FILENAME);
        } 
        
        if (fileExtension.length() > MAX_LENGTH_OF_EXTENSION) {
            System.out.println("File extension is too long. Truncated to {} characters.", MAX_LENGTH_OF_EXTENSION);
            fileExtension = StringUtils.substring(fileExtension, 0, MAX_LENGTH_OF_EXTENSION);
        }
	
	// Added to prevent FileNotFoundException (Invalid Argument) - in *nix environment
        fileBaseName = fileBaseName.replaceAll("\\?", "");
        fileExtension = fileExtension.replaceAll("\\?", "");

        return String.format(FILENAME_PATTERN, md5, fileBaseName, fileExtension);
    }


    public static String getOutputPath(String url) {
	String fullDir = "/data3/memex/counterfeit-electronics/dump/full/";
	
	String baseName = FilenameUtils.getBaseName(url);
	String extension = FilenameUtils.getExtension(url);
	
	String md5Ofurl = getUrlMD5(url);
	
	if (extension == null || (extension != null && extension.equals(""))) {
	    extension = "html";
	}
	
	String outputFullPath = String.format("%s/%s", fullDir, createFileName(md5Ofurl, baseName, extension));
	return outputFullPath;
    }


    public static boolean hasLogin(String html) {
	Document doc = Jsoup.parse(html);
	
	Elements passwordForm = doc.select("[type='password'], [name='password']");
	if (passwordForm != null && !passwordForm.isEmpty()) {
	    return true;
	}
	
	Elements loginLinks = doc.select("a:contains(log in), a:contains(sign in)");
	if (loginLinks != null && !loginLinks.isEmpty()) {
	    return true;
	}
	
	return false;
    }

 
    public static void main(String[] args) {
	Writer writer = null;
	BufferedReader br = null;
	
	try {
	    FileInputStream fstream = new FileInputStream(args[0]);
	    br = new BufferedReader(new InputStreamReader(fstream));
	    
	    String strLine;
	    
	    FileOutputStream outstream = new FileOutputStream("output/logins.txt");
	    writer = new BufferedWriter(new OutputStreamWriter(outstream, "UTF-8"));
	    
	
	    //Read File Line By Line
	    while ((strLine = br.readLine()) != null)   {
		// Print the content on the console
		System.out.println ("Checking ..." + strLine);
		
		String reversedDumpPath;
		String dumpPath
		try {
		    reversedDumpPath = getReversedOutputPath(strLine);
		}
		catch (MalformedURLException ex) {
		    ex.printStackTrace();
		    continue;
		}
		System.out.println("Reversed Dump: " + reversedDumpPath);
	    
		File dump = new File(reversedDumpPath);
		
		// If doesn't exist, try the other Dump Path
		
		/*
		if (!dump.exists()) {
		    dumpPath = getOutputPath(strLine);
		    System.out.println("Dump: " + dumpPath);

		    dump = File(dumpPath)
		}
		*/
		
		if (dump.exists()) {
		    FileInputStream dumpstream = new FileInputStream(dump);
		    
		    String rawHtml = IOUtils.toString(dumpstream, "UTF-8");
		    if (hasLogin(rawHtml)) {
			// Found a url with Login
			writer.write(strLine);
		    }
		}	
	    }
	   
	} catch (IOException ex) {
	    // Handle exception
	    ex.printStackTrace();
	} finally {
	    // Close both streams
	    try {
		writer.close(); br.close();
	    } catch (Exception ex) {/* Ignore */}
	    	
	}
    }
      
}