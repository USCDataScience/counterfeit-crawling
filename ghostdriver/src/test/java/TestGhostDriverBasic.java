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

public class TestGhostDriverBasic {
    private WebDriver driver;
    private String baseUrl;
    protected static DesiredCapabilities caps;
    
    @Before
    public void initialize() throws Exception {
	caps = new DesiredCapabilities();
	caps.setJavascriptEnabled(true);
	caps.setCapability("takesScreenshot", false);
        // caps.setCapability(
	//    PhantomJSDriverService.PHANTOMJS_EXECUTABLE_PATH_PROPERTY,
        //    "/usr/local/bin/phantomjs");
	
	driver = new PhantomJSDriver(caps);
	baseUrl = "http://www.jncmanufacturing.com/"; // Test on site with lots of jQuery
	driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }
    
    @Test
    public void getLinks() throws Exception {
	driver.get(baseUrl);
	
	//Getting all the links present in the page by a HTML tag.
	List<WebElement> links = driver.findElements(By.tagName("a"));
    
	System.out.println("Total Links present is "+links.size());
	for(int i = 0; i < links.size(); i++){
	    System.out.println(links.get(i).getAttribute("href"));
	}
	System.out.printf("%n");
    }
    
    @Test
    public void getContent() throws Exception {
	driver.get("http://www.ibm.com/design/");
	
	//Extract content
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