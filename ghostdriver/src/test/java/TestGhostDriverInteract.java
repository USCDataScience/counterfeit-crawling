package ghostdriver.test;

import java.util.List;;
import java.util.concurrent.TimeUnit;

import org.junit.*;
import static org.junit.Assert.*;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.phantomjs.PhantomJSDriver;
import org.openqa.selenium.phantomjs.PhantomJSDriverService;
import org.openqa.selenium.remote.DesiredCapabilities;

import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.WebDriverWait;

public class TestGhostDriverInteract {
    private WebDriver driver;
    protected static DesiredCapabilities caps;
   
    public void waitforJS(WebDriver driver) {
	while (true) {
	    Boolean jsIsComplete = (Boolean) ((JavascriptExecutor) driver)
		.executeScript("return document.readyState").toString().equals("complete");
	    
	    if (jsIsComplete) {
		break;
	    }
	    try {
		Thread.sleep(500);
	    } catch (InterruptedException e) {
		e.printStackTrace();
	    }
	}
    }
    
    @Before
    public void initialize() throws Exception {
	caps = new DesiredCapabilities();
	caps.setJavascriptEnabled(true);
	caps.setCapability("takesScreenshot", false);
        // caps.setCapability(
	//    PhantomJSDriverService.PHANTOMJS_EXECUTABLE_PATH_PROPERTY,
        //    "/usr/local/bin/phantomjs");
	
	driver = new PhantomJSDriver(caps);
	driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }
    
    @Test
    public void scroll() throws Exception {
	driver.get("https://www.facebook.com/warriors/"); // site with infinite scroll to load content
	    
	Long currentPos = (Long) ((JavascriptExecutor) driver).executeScript("return window.scrollY;");
	
	//Scroll to bottom of page	
	while (true) {
	    ((JavascriptExecutor) driver).executeScript("window.scrollTo(0,document.body.scrollHeight)");
	    waitforJS(driver);
	    
	    int count = 0;
	    if (currentPos == (Long) ((JavascriptExecutor) driver).executeScript("return window.scrollY;")) {
		count++;
		if (count > 10) {
		    break;
		}
	    } else {
		currentPos = (Long) ((JavascriptExecutor) driver).executeScript("return window.scrollY;");
		if (currentPos > 10000) {
		    break;
		}
		count = 0;
	    }
	}
	
	String content = driver.findElement(By.tagName("body")).getText();
	System.out.println(content);
	System.out.printf("%n");
    }
    
    @After
    public void quit() {
	if (driver != null) {
	    driver.quit();
	    driver = null;
	}
    }
    
}