package org.apache.nutch.protocol.interactiveselenium;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.NoSuchElementException;

import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
 * Handler that handles the hover menu for http://www.altitek.com.
 * @author Joey Hong
 */
public class AltitekHandler implements InteractiveSeleniumHandler {
    public static final Logger LOG = LoggerFactory
	.getLogger(AltitekHandler.class);
    
    private Set<String> getMfgsFromMenu(WebDriver driver) {
	Set<String> links = new HashSet<String>();
	
	WebElement menu = driver.findElement(By.xpath("//a[@class='dropdown-toggle']"));
	
	List<WebElement> mfgs = menu.findElements(By.xpath(".//a"));
	for (WebElement mfg : mfgs) {
	    String linkValue = mfg.getAttribute("href");
	    links.add("<a href=\"" +linkValue + "\" />");
	}
	
	return links;
    }

    @Override
    public String processDriver(WebDriver driver) {
	StringBuffer buffer = new StringBuffer();
	
	// Extract content - getText doesn't return any links
	String content = driver.findElement(By.tagName("body")).getText();
	buffer.append(content).append("\n");
	
	Set<String> links = getMfgsFromMenu(driver);
	if (driver.getCurrentUrl().equalsIgnoreCase("http://www.altitek.com/")) {
	    try {
		for (link : links) {
		    driver.get(link);
		}
	    }
	    catch (Exception &e) {
		LOG.info("Error occured navigating: {}", driver.getCurrentUrl());
		LOG.error(e.getMessage(), e);
	    }
	    finally {
		buffer.append(links).append("\n");
	    }
	}
	
	return buffer.toString();
    }

    @Override
    public boolean shouldProcessURL(String URL) {
	String hostname = "altitek";
	
	if (URL.indexOf(hostname) >= 0) {
	    return true;
	}
	return false;
    }

}