#Scrapes the internet for what I need

from selenium import webdriver
import argparse
from time import sleep
import pandas as pd
import numpy as np
import sys

#create a parser for my arguments
parser = argparse.ArgumentParser()

parser.add_argument("-s", "--ipo", dest="ipo", action="store", help="stock symbol/ipo")
parser.add_argument("--sma", dest="movingAverage", action="store_true", help="prints the moving average of a stock")

''' 

websites:

    
    https://www.barchart.com/stocks/quotes/{IPO}/technical-analysis

'''


def getSMAFromBarchart(IPO):

    driver = webdriver.Firefox()

    try:
        driver.get(f"https://www.barchart.com/stocks/quotes/{IPO}/technical-analysis")
        driver.implicitly_wait(15)
        #get current price
        currentPrice = float(driver.find_element_by_css_selector("span.last-change:nth-child(1)").text)
        
        #find moving averages
        SMA5 = float(driver.find_element_by_xpath("/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/ng-transclude/table/tbody/tr[1]/td[2]").text)
        SMA20 = float(driver.find_element_by_xpath("/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/ng-transclude/table/tbody/tr[2]/td[2]").text)
        SMA50 = float(driver.find_element_by_xpath("/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/ng-transclude/table/tbody/tr[3]/td[2]").text)
        SMA100 = float(driver.find_element_by_xpath("/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/ng-transclude/table/tbody/tr[4]/td[2]").text)
        SMA200 = float(driver.find_element_by_xpath("/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/ng-transclude/table/tbody/tr[5]/td[2]").text)
        SMAYear = float(driver.find_element_by_xpath("/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/ng-transclude/table/tbody/tr[6]/td[2]").text)

        #create dataframe taht records everything mentioned and return it
        SMADF = pd.DataFrame(np.array([[IPO, currentPrice, SMA5, SMA20, SMA50, SMA100, SMA200, SMAYear]]), columns=["symbol", "price", "SMA5", "SMA20", "SMA50", "SMA100", "SMA200", "SMAYear"])
        
        return SMADF
    except:
        print(sys.exc_info()[0])
        sys.exit(1)
    finally:
        driver.quit()


if __name__ == "__main__":
    args = parser.parse_args()
    if args.movingAverage:
        print(getSMAFromBarchart(args.ipo))