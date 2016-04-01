package org.apache.nutch.protocol.interactiveselenium;

import java.util.List;

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
	WebDriverWait wait = new WebDriverWait(driver, 30);
	
	/** wati for jQuery to load */
	ExpectedCondition<Boolean> jQueryLoad = new ExpectedCondition<Boolean>() {
	    @Override
	    public Boolean apply(WebDriver driver) {
		try {
		    return (boolean) ((JavascriptExecutor) driver)
		    .executeScript("return JQuery.active == 0");
		    
		}
		catch (Exception e) {
		    return true;
		}
	    }
	};
	/** wait for Javascript to load */
	ExpectedCondition<Boolean> jsLoad = new ExpectedCondition<Boolean>() {
	    @Override
	    public Boolean apply(WebDriver driver) {
		try {
		    return (boolean) ((JavascriptExecutor) driver)
		    .executeScript("return document.readyState").toString().equals("complete");
		}
		catch (Exception e) {
		    return true;
		}
	    }
	};
	
	wait.until(jQueryLoad);
	wait.until(jsLoad);

    }
    
    /**
     * Helps focus crawling to relevant pages..
     */
    @Override
    public String processDriver(WebDriver driver) {
	String content = "";
	LOG.info("Processing URL: {}", driver.getCurrentUrl());		
		
	if (driver.getCurrentUrl().equalsIgnoreCase("http://www.etitan.net/")) {
	    loginEtitan(driver);
	    try {
		driver.findElement(By.xpath("//a[text()='products']")).click();
		content += driver.findElement(By.tagName("body")).getAttribute("innerHTML");
	    }
	    catch (NoSuchElementException e) {
		LOG.error(e.getMessage(), e);
	    }
	}
	else if (driver.getCurrentUrl().equalsIgnoreCase("http://www.icdigitalelectronics.com/")) {
	    /** Navigate to electronic parts */
	    try {
		driver.findElement(By.xpath("//a[@title='Line Card']")).click();
		content += driver.findElement(By.tagName("body")).getAttribute("innerHTML");
	    }
	    catch (NoSuchElementException e) {
		LOG.error(e.getMessage(), e);
	    }
	}
	else if (driver.getCurrentUrl().equalsIgnoreCase("http://1sourcecomponents.com/")) {
	    /** Navigate to browse store */
	    try {
		driver.findElement(By.linkText("Browse Store")).click();
		content += driver.findElement(By.tagName("body")).getAttribute("innerHTML");
	    }
	    catch (NoSuchElementException e) {
		LOG.error(e.getMessage(), e);
	    }
	}
	else if (driver.getCurrentUrl().equalsIgnoreCase("http://www.1sourcemilaero.com/#")) {
	    content += navigate1sourcemilaero(driver);
	}
	else if (driver.getCurrentUrl().equalsIgnoreCase("http://www.4starelectronics.com/")) {
	    /** Navigate to inventory */
	    try {
		driver.findElement(By.xpath("//a[text()='In-Stock Inventory']")).click();
		content += driver.findElement(By.tagName("body")).getAttribute("innerHTML");
	    }
	    catch (NoSuchElementException e) {
		LOG.error(e.getMessage(), e);
	    }
	}
	
	return content;
    }
    
    /**
     * Login to the Etitan site 
     */
    public void loginEtitan(WebDriver driver) {
	try {
	    driver.findElement(By.className("btn_log")).click();
	    LOG.info("Login button detected: {}", driver.getCurrentUrl());
	    
	    WebDriverWait wait = new WebDriverWait(driver, 10);
	    wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("lousername")));
	    
	    WebElement email = driver.findElement(By.id("lousername"));
	    WebElement password = driver.findElement(By.id("lopassword"));
	   
	    email.sendKeys("seleniumjplcrawler@gmail.com");
	    password.sendKeys("apachenutchspider");
	    
	    driver.findElement(By.xpath("//button[contains(@class, 'btn_yellow') and text()='Log in']"))
		.click();
	    waitforJavascript(driver);
	    
	    LOG.info("Successfully logged in: {}", driver.getCurrentUrl());
	}
	catch (Exception e) {
	    LOG.info("Could not log in: {}", driver.getCurrentUrl());
	    LOG.error(e.getMessage(), e);
	}
    }

    /**
     * Focuses crawling on a relevant portion of the site with products. Gets only
     * pages that include information about site's products.
     */
    public String navigate1sourcemilaero(WebDriver driver) {
	String content = "";
        try {
	    WebElement menu = driver.findElement(By.xpath("//li[contains(@class, 'menu-item-410')]"));
            
            /** Find all sub-sections of a menu */
            List<WebElement> categories = menu.findElements(By.xpath(".//a"));
	    
            for (int i = 0; i < categories.size(); i++) {
		WebElement element = categories.get(i);
		
                /** Navigates only to the relevant links */
                String link = element.getAttribute("href");
                
		/** Make sure link is under correct hostname */
		if (link.startsWith("http://www.1sourcemilaero.com")) {
		    driver.get(link);
		    waitforJavascript(driver);
		    
		    LOG.info("Found page: {}", driver.getCurrentUrl());
		    content += driver.findElement(By.tagName("body")).getAttribute("innerHTML");
		}
		    
		/** Refresh the handler */
		driver.navigate().refresh();
		waitforJavascript(driver);
		
		menu = driver.findElement(By.xpath("//li[contains(@class, 'menu-item-410')]"));
		categories = menu.findElements(By.xpath(".//a"));
            }
        }
        catch (Exception e) {
            LOG.info("Error occured navigating: {}", driver.getCurrentUrl());
	    LOG.error(e.getMessage(), e);
        }
        return content;
    }
    
    @Override
    public boolean shouldProcessURL(String URL) {
	String[] prefixes = {
	    "http://www.etitan.net",
	    // "http://www.chiptech.com" , // Site appears down
	    "http://www.icdigitalelectronics.com",
	    "http://1sourcecomponents.com",
	    "http://www.1sourcemilaero.com",
	    "http://www.carlinsystems.com", 
	    "http://www.4starelectronics.com",
	    "http://www.gictg.com",
	    "http://www.stockingdistributors.com", 
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