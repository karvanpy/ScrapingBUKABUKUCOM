# ScrapingBUKABUKUCOM
Scrape all books information (http://bukabuku.com) based on category.

### Install Scrapy
```python3
pip3 install scrapy
```

### Clone Repo
```
git clone https://github.com/karvanpy/ScrapingBUKABUKUCOM
```

### Enter to bukabukucom directory
```bash
cd bukabukucom
```

### Crawl the spider (spider name is 'bukabukucom')
```python3
scrapy crawl bukabukucom
```

### Export result (to CSV/JSON/XML)
```
scrapy crawl bukabukucom -O bukabukucom_result.csv
```
If you want to export to spreadsheet / XLSX format, install scrapy-xlsx first: `pip3 install scrapy-xlsx`, then:
```python3
scrapy crawl bukabukucom -O bukabukucom_result.xlsx
```
