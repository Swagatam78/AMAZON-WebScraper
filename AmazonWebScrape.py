import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

HEADES = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# for ProductName
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text.strip()
    except AttributeError:
        title_value = "NA"
    return title_value

# for Prices
def get_Price(soup):
    try:
        price = soup.find("span", attrs={"class": 'a-price-whole'})
        price_value = price.text.strip()
    except:
        price_value = "NA"
    return price_value

# for rating
def get_Rating(soup):
    try:
        rating = soup.find("span", attrs={"class": 'a-icon-alt'})
        rating_value = rating.text.strip()
    except:
        rating_value = "NA"
    return rating_value

# for Count of reviews
def get_Review_count(soup):
    try:
        review = soup.find("span", attrs={"id": 'acrCustomerReviewText'})
        review_value = review.text.strip()
    except:
        review_value = "NA"
    return review_value

# for Count of reviews
def get_Description(soup):
    try:
        review = soup.find("div", attrs={"id": 'feature-bullets"'})
        re1=review.find("ul", attrs={"class": 'a-unordered-list a-vertical a-spacing-mini"'})
        re2=re1.find_all("li",attrs={"class": 'a-spacing-mini'})
        re3=re2.find_all("span",attrs={"class": 'a-list-item'}).text.strip()
        review_value = re3
    except:
        review_value = "NA"
    return review_value

# for ASIN number
def get_ASIN(soup):
    try:
        asin = soup.find("th", text="ASIN").find_next_sibling("td")
        asin_value = asin.text.strip()
    except:
        asin_value = "NA"
    return asin_value

# for Product Discription
def get_Product_Description(soup):
    try:
        PD = soup.find("div", attrs={"class": 'aplus-v2 desktop celwidget'})
        npd=PD.find_all("p")
        value = npd.text.strip()
    except:
        value = "NA"
    return value

# for Manufacturer
def get_Manufacturer(soup):
    try:
        Manu = soup.find("th", text="Manufacturer").find_next_sibling("td")
        value = Manu.text.strip()
    except:
        value = "NA"
    return value


if __name__ == '__main__':
    dict1 = {
        "Name": [],
        "Price": [],
        "Rating": [],
        "No of reviews": [],
        "Product URL": [],
        "ASIN": [],
        "Product Description": [],
        "Description": [],
        "Manufacturer": [],
    }


    for i in range(1, 21):
        SearchPageURL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_" + str(i)
        webpagereq = requests.get(SearchPageURL, headers=HEADES)
        soup1 = BeautifulSoup(webpagereq.text, "html.parser")

        links = soup1.find_all("a", attrs={"class": 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        for link in links:
            product_url = link.get('href')
            if product_url.startswith('/'):
                product_url = 'https://www.amazon.in' + product_url

            web1 = requests.get(product_url, headers=HEADES)
            soup12 = BeautifulSoup(web1.text, "html.parser")

            dict1['Name'].append(get_title(soup12))
            dict1['Price'].append(get_Price(soup12))
            dict1['Rating'].append(get_Rating(soup12))
            dict1['No of reviews'].append(get_Review_count(soup12))
            dict1['Product URL'].append(product_url)
            dict1['ASIN'].append(get_ASIN(soup12))
            dict1['Product Description'].append(get_Product_Description(soup12))
            dict1['Description'].append(get_Description(soup12))
            dict1['Manufacturer'].append(get_Manufacturer(soup12))


    amazon_df = pd.DataFrame.from_dict(dict1)
    amazon_df['Name'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['Name'])
    amazon_df.to_csv("amazon_data13.csv", header=True, index=False)
    print(amazon_df)
