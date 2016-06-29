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
 * Handler that handles the pagination for http://www.alibaba.com.
 * @author Joey Hong
 */
public class AlibabaHandler implements InteractiveSeleniumHandler {
    public static final Logger LOG = LoggerFactory
	.getLogger(AlibabaHandler.class);
    
    @Override
    public String processDriver(final WebDriver driver) {
	StringBuffer buffer = new StringBuffer();

	// Extract content - getText doesn't return any links
	String content = driver.findElement(By.tagName("body")).getText();
	buffer.append(content).append("\n");
	
	if (driver.getCurrentUrl().startsWith("http://trends.alibaba.com/markets/Integrated-Circuits_400103.html") ||
	    driver.getCurrentUrl().equalsIgnoreCase("http://www.alibaba.com/Integrated-Circuits_pid400103")) {
	    
	    WebElement next= driver.findElement(By.xpath("//div[@class='ui2-pagination-pages']//a[@class='next']"));
	    
	    String link = next.getAttribute("href");
	    
	    WebDriver pagination = new FirefoxDriver();
	    pagination.get(link);
	    while (true) {
		try {
		    pagination.findElement(By.xpath("//div[@class='ui2-pagination-pages']//a[@class='next']"))
			.click();
		    
		    (new WebDriverWait(driver, 8)).until(new ExpectedCondition<Boolean>() {
			    public Boolean apply(WebDriver d) {
				try {
				    Thread.sleep(5000);
				} catch (InterruptedException e) {
				    e.printStackTrace();
				}
				return d.getCurrentUrl().toLowerCase().contains(driver.getCurrentUrl().toLowerCase());
			    }
			});
		    buffer.append("<a href=\"").append(pagination.getCurrentUrl()).append("\" />\n");
		}
		catch(Exception e) {
		    pagination.quit();
		}
	    }
	}
	return buffer.toString();
    }

    @Override
    public boolean shouldProcessURL(String URL) {
	String hostname = "alibaba";
	
	if (URL.indexOf(hostname) >= 0) {
	    return true;
	}
	return false;    
    }
}