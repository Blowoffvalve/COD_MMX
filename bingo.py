from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse, urljoin
from webdriver_manager.chrome import ChromeDriverManager

def scrape_content_and_sublinks(url):
    # Setup WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    sublinks = []
    
    try:
        # Navigate to the webpage
        driver.get(url)
        
        # Extract the website name from the URL
        domain_name = urlparse(url).netloc
        
        # Prepare a filename using the website name
        base_filename = f"{domain_name}_content.txt".replace("www.", "").replace(".com", "")
        
        # Scrape all text content from the base URL
        content = driver.find_elements(By.XPATH, '//*')  # This XPath gets all elements, adjust as needed
        with open(base_filename, 'w', encoding='utf-8') as file:
            for element in content:
                file.write(element.text + '\n')
                
        print(f"Content saved to {base_filename}")
        
        # Find all links on the page
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            href = link.get_attribute('href')
            if href and urlparse(href).netloc == domain_name:
                sublinks.append(href)
                
        # Deduplicate the list of sublinks
        sublinks = list(set(sublinks))
        
        # Visit each link and scrape content
        for i, sublink in enumerate(sublinks[:10]):  # Limit to first 10 links for practicality
            driver.get(sublink)
            sub_content = driver.find_elements(By.XPATH, '//*')
            sub_filename = f"{domain_name}_content_{i}.txt".replace("www.", "").replace(".com", "")
            with open(sub_filename, 'w', encoding='utf-8') as file:
                for element in sub_content:
                    file.write(element.text + '\n')
            print(f"Content from {sublink} saved to {sub_filename}")
            
    finally:
        driver.quit()

# Example usage
url = 'https://guardian.ng/category/news/nigeria/'
scrape_content_and_sublinks(url)
