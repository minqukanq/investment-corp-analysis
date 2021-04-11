# play store webcrawler

A simple way to crawl Google Play Store reviews from python using Selenium and Beautifulsoup

## Installation

Install with pip

```
pip install pandas
pip install selenium
pip install beautifulsoup4
pip install lxml
```



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

The code may not work on Linux or Mac os.

```
python play-store-webcrawler.py --url "URL" --chrome "Chrome driver dir path" \
--save_dir "save dir path"
```

```
optional arguments:
  -h, --help           	  show this help message and exit
  --url URL            	  URL of the page to crawl
  --chrome CHROME         chromedriver path
  --save_dir SAVE_DIR  	  Crawled data filename, ex) 'output.csv'
```

## Running a Python script:
```
python play-store-webcrawler.py --url "https://play.google.com/store/apps/details?id=com.kakaobank.channel&showAllReviews=true" --chrome chromedriver.exe --save_dir kakao_bank.csv
```
We now have a data.

| DATE      | STAR                              | LIKE | REVIEW                                                       |
| --------- | --------------------------------- | ---- | ------------------------------------------------------------ |
| 2021-2-19 | 별표 5개 만점에 1개를 받았습니다. | 1    | 좀.. 개선이 많이 필요해보입니다.. 타 증권사 어플에비해 가독성이 너무 떨어져요 버튼도 잘 안먹구요. |
| 2021-2-2  | 별표 5개 만점에 1개를 받았습니다  | 3    | 폴드2. one UI 3.0 업뎃 후 아이콘 아예 안보임. 매도도 매수도 이제 못하게 됨....당장 고쳐라... |
| ...       | ...                               | ...  | ...                                                          |


