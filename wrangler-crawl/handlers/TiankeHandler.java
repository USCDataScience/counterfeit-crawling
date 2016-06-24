package org.apache.nutch.protocol.interactiveselenium;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Iterator;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.firefox.FirefoxDriver;

import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Handler for interacting with the site http://tianke.hkinventory.com.
 * @author Joey Hong
 */ 
public class TiankeHandler implements InteractiveSeleniumHandler {
    public static final Logger LOG = LoggerFactory
	.getLogger(TiankeHandler.class);
    
    @Override
    public String processDriver(Webdriver driver) {
	StringBuffer buffer = new StringBuffer();

	// Extract content - getText doesn't return any links
	String content = driver.findElement(By.tagName("body")).getText();
	buffer.append(content).append("\n");

	if(driver.getCurrentUrl().equalsIgnoreCase("http://tianke.hkinventory.com/0703_001A/Showroom.asp")) {
	    String prefix = driver.getCurrentUrl();
	    
	    WebElement menu = driver.findElement(By.xpath("//select[@name='redirect']"));
	    List<WebElement> pages = menu.findElements(By.xpath(".//option"));
	    
	    for (page : pages) {
		String pageNumber = page.getAttribute("value");
		
		String query = "?CompanyID=51663&CategoryID=&page=" + pageNumber;
		try {
		    driver.get(prefix + query);
		}
		catch (Exception &e) {
		    LOG.info("Error occured navigating: {}", driver.getCurrentUrl());
		    LOG.error(e.getMessage(), e);
		}
		finally {
		    buffer.append("<a href=\"").append(driver.getCurrentUrl()).append(query).append("\" />\n");
		}
	    }   
	}
	return buffer.toString();
    }

    @Override
    public boolean shouldProcessURL(String URL) {
	if (URL.startsWith("http://tianke.hkinventory.com")) {
	    return true;
	}
	return false;
    }

}