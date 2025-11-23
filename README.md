#  BrowserStack Automation Assignment

This project completes the **BrowserStack Automation Engineer
Assignment**, which includes:

-   Scraping 5 news articles\
-   Downloading images\
-   Translating content\
-   Running cross-browser tests on BrowserStack using Selenium\
-   Storing outputs and providing public build/test URLs

------------------------------------------------------------------------

## 📂 Project Structure

    selenium_assignment/
    │
    ├── articles/
    │   ├── Article_1/
    │   ├── Article_2/
    │   ├── Article_3/
    │   ├── Article_4/
    │   └── Article_5/
    │
    ├── output/
    │   ├── Article_1/
    │   ├── Article_2/
    │   ├── Article_3/
    │   ├── Article_4/
    │   └── Article_5/
    │   ├── summary.json
    │   └── translations.json
    │
    └── src/
        ├── scraper.py
        ├── translate.py
        ├── analyze.py
        ├── test_driver.py
        ├── browserstack_test.py
        └── requirements.txt

------------------------------------------------------------------------

##  Features Implemented

###  1. Article Scraping

Extracted title, body content, and images from 5 Spanish news articles.

###  2. Image Downloading

Saved article images into respective folders.

###  3. Translation

Translated article content into English using automated translation
logic.\
Stored results in `translations.json`.

###  4. Summary Generation

Generated summaries of each article and stored in `summary.json`.

###  5. BrowserStack Automation

Executed 5 automated Selenium tests on BrowserStack:

-   Windows 11 -- Firefox\
-   iPhone 14 -- iOS Safari\
-   Android Pixel -- Chrome\
-   macOS Sonoma -- Safari\
-   Windows 10 -- Edge

All tests passed successfully.

------------------------------------------------------------------------

##  How to Run Locally

### **1️ Create virtual environment**

    python -m venv venv
    source venv/bin/activate  (Mac/Linux)
    venv\Scripts\activate     (Windows)

### **2️ Install dependencies**

    pip install -r src/requirements.txt

### **3️ Run scraper**

    python src/scraper.py

### **4️ Run translation**

    python src/translate.py

### **5️ Run analysis**

    python src/analyze.py

### **6️ Run BrowserStack tests**

Set your credentials:

    export BROWSERSTACK_USERNAME="your_username"
    export BROWSERSTACK_ACCESS_KEY="your_key"

Then run:

    python src/browserstack_test.py

------------------------------------------------------------------------

## BrowserStack Build (Public URL)

🔗 **BrowserStack Build:**\
https://automation.browserstack.com/projects/Default+Project/builds/Untitled+Build+Run/1?tab=tests&testListView=spec&public_token=3a08135d875eef5083f39e09426b20ef5b0f227e80bc76a7cd40fb720a61fed9

------------------------------------------------------------------------

##  GitHub Repository

🔗 **Repository URL:**\
https://github.com/shashankhnr/browserstack-assignment

------------------------------------------------------------------------

##  Notes

-   `venv` folder is intentionally not committed.\
-   Output files are saved inside `/output/` per assignment
    instructions.\
-   All tests pass successfully on BrowserStack.\
-   The project is fully reproducible using the steps above.


