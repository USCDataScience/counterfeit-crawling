package org.apache.nutch.protocol.interactiveselenium;

import java.util.List;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.NoSuchElementException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Custom handler that performs various tasks to aid in crawling
 * for the various seeded sites.
 * @author Joey Hong
 */
public class CustomHandler implements InteractiveSeleniumHandler {
    public static final Logger LOG = LoggerFactory
	.getLogger(CustomHandler.class);
    
    /** 
     * Waits for Javascript to execute.
     */
    public void waitforJavascript(WebDriver driver) {
	long timeout = 10 * 1000; /* At most 10 seconds */
	
	long start = System.currentTimeMillis();
	while (true) {
	    if (System.currentTimeMillis() - start > timeout) {
		LOG.info("Timeout reached at URL: {}", driver.getCurrentUrl());
		break;
	    }
	    boolean done = (boolean) ((JavascriptExecutor) driver)
		.executeScript("return JQuery.active == 0");
	    if (done) {
		break;
	    }
	    try {
		Thread.sleep(100);
	    } catch (InterruptedException e) {
		e.printStackTrace();
	    }
	}
									 
    }
    
    /**
     * Helps focus crawling to relevant pages..
     */
    @Override
    public String processDriver(WebDriver driver) {
	String ret = "";
	if (driver.getCurrentUrl().equalsIgnoreCase("http://www.etitan.net/")) {
	    ret += loginEtitan(driver);
	    try {
		driver.findElement(By.xpath("//a[text()='Line Card']")).click();
		ret += driver.getPageSource();
	    }
	    catch (NoSuchElementException e) {
	    }
	}
	else if (driver.getCurrentUrl().equalsIgnoreCase("http://www.icdigitalelectronics.com/")) {
	    /** Navigate to electronic parts */
	    try {
		driver.findElement(By.linkText("Line Card")).click();
		ret += driver.getPageSource();
	    }
	    catch (NoSuchElementException e) {
	    }
	}
	else if (driver.getCurrentUrl().equalsIgnoreCase("http://1sourcecomponents.com/")) {
	    /** Navigate to browse store */
	    try {
		driver.findElement(By.linkText("Browse Store")).click();
		ret += driver.getPageSource();
	    }
	    catch (NoSuchElementException e) {
	    }
	}
	else if (driver.getCurrentUrl().equalsIgnoreCase("http://www.1sourcemilaero.com/")) {
	    ret += navigate1sourcemilaero(driver);
	}
	else if (driver.getCurrentUrl().equalsIgnoreCase("http://www.4starelectronics.com/")) {
	    /** Navigate to electronic parts */
	    try {
		driver.findElement(By.xpath("//a[text()='Line Card']")).click();
		ret += driver.getPageSource();
	    }
	    catch (NoSuchElementException e) {
	    }
	}
	return ret;
    }
    
    /**
     * Login to the Etitan site 
     */
    public String loginEtitan(WebDriver driver) {
	String ret = "";
	try {
	    driver.findElement(By.className("btn_log")).click();
	    waitforJavascript(driver);
	    
	    WebElement email = driver.findElement(By.id("lousername"));
	    WebElement password = driver.findElement(By.id("lopassword"));
	    email.sendKeys("seleniumjplcrawler@gmail.com");
	    password.sendKeys("apachenutchspider");
	    
	    driver.findElement(By.xpath("//button[contains(@class, 'log_box') and text()='Log in']"))
		.click();
	    waitforJavascript(driver);
	    
	    ret += driver.getPageSource();
	    LOG.info("Successfully logged in: {}", driver.getCurrentUrl());
	}
	catch (Exception e) {
	    LOG.info("Could not log in: {}", driver.getCurrentUrl());
	}
	return ret;
    }

    /**
     * Focuses crawling on a relevant portion of the site with products. Gets only
     * pages that include information about site's products.
     */
    public String navigate1sourcemilaero(WebDriver driver) {
	String ret = "";
	try {
	    WebElement menu = driver.findElement(By.xpath("//li[contains(@class, 'menu-item-410')]"));
	    
	    /* Find all sub-sections of a menu */
	    List<WebElement> categories = menu.findElements(By.xpath(".//a"));
	    for (WebElement element : categories) {
		/* Navigates only to the relevant links */
		String link = element.getAttribute("href");
		driver.get(link);
		waitforJavascript(driver);
		
		LOG.info("Found page: {}", driver.getCurrentUrl());
		ret += driver.getPageSource();
		driver.navigate().back();
	    }
	}
	catch (Exception e) {
	    LOG.info("Error occured navigating: {}", driver.getCurrentUrl());
	}
	return ret;
    }
    
    @Override
    public boolean shouldProcessURL(String URL) {
	String[] prefixes = {
	    "http://www.etitan.net",
	    // "http://www.chiptech.com" , // Site appears down
	    "http://www.icdigitalelectronics.com",
	    "http://www.1sourcecomponents.com",
	    "http://www.1sourcemilaero.com",
	    // "http://www.carlinsystems.com", 
	    "http://www.4starelectronics.com",
	    // "http://www.gictg.com",
	    // "http://www.stockingdistributors.com", 
	    "http://www.icsource.com"
	};
	for (int i = 0; i < prefixes.length; ++i) {
	    if (URL.startsWith(prefixes[i])) {
		return true;
	    }
	}
	return false;
    }
}