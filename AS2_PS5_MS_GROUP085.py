'''@author: GROUP085 '''

import traceback

# Name         : maxProfitWithIterativeApproach
# Desc         : This Function calculates the maximum profit in share sell by using Iterative Approach
# param (list) : List stock_prices_list contain the stock price on a given day in dataset
# return       : MaximumProfit, BuyDay,SellDay value if successful else return the error codes
# Example      : maxProfitWithIterativeApproach(stock_prices_list)
def maxProfitWithIterativeApproach(stock_prices_list):
    len_of_list = len(stock_prices_list)
    buy_index=0
    buy_value=stock_prices_list[0]
    sell_index=0
    sell_value=stock_prices_list[0]
    diff=0
    for price_index in range(len_of_list-1):
        currentValue=stock_prices_list[price_index]
        nextValue=stock_prices_list[price_index+1]
        max_profit=sell_value-buy_value
        current_profit=nextValue-currentValue
        # finding the minium buy price and day to buy in the list of values
        if currentValue<buy_value and (max_profit<current_profit or diff<current_profit) :
            buy_index =price_index
            buy_value=currentValue
        # finding the initial sell price and day to sell in the list of values
        if sell_index<buy_index & current_profit>diff:
            sell_index =price_index+1
            sell_value=nextValue
            diff=current_profit
        # finding the sell price and day to sell in the list of values
        if currentValue>=sell_value:
            sell_index =price_index
            sell_value=currentValue
        # increment the buy index if current value is same as next value.
        if currentValue == buy_value :
            buy_index =price_index
    # finding the Maximum sell price and day to sell in the list of values
    if stock_prices_list[len_of_list-1]>sell_value:
        sell_index =len_of_list-1
        sell_value = stock_prices_list[len_of_list-1]

    if(buy_index != sell_index):
        return sell_value - buy_value , buy_index,sell_index
    else:
        return 0,0,0
# Name         : maxProfitcalculationWithDivideandConquer
# Desc         : This Function calculates the maximum profit in share sell by using Divide & Conquer strategy
# param (list) : List stock_prices_list contain the stock price on a given day in dataset
# param (int)  : start contain the index of first day in dataset
# param (int)  : stop contain the index of last day in dataset
# return       : MaximumProfit, BuyDay,SellDay value if successful else return the error codes
# Example      : maxProfitcalculationWithDivideandConquer(stock_prices_list, start, stop)
def maxProfitcalculationWithDivideandConquerRecursion(stock_prices_list, start, stop):
    size = stop - start
    # buy on the first day, sell on the second.
    if size == 0:
        return 0, start, start
    if size == 1:
        return stock_prices_list[stop] - stock_prices_list[start], start, stop \
            # calculate mid value divide by 2 and then we will use this to trail down
    medium = start + size//2
    # the "divide" part in Divide & Conquer: try both halfs of the array
    profitcalculatedfromfirstpart, buy1, sell1 = maxProfitcalculationWithDivideandConquerRecursion(stock_prices_list, start, medium-1)
    profitcalculatedfromSecondpart, buy2, sell2 = maxProfitcalculationWithDivideandConquerRecursion(stock_prices_list, medium, stop)

    # finding the minium buy price in the lower half and the maximum sell price in the upper half
    stock_buy_idx = start
    stock_buy_value = stock_prices_list[start]
    if stock_prices_list[start] == stock_prices_list[start+1]:
        stock_buy_value = stock_prices_list[start+1]
    for i in range(start+1, medium):
        if stock_prices_list[i] < stock_buy_value and stock_prices_list[i] != stock_buy_value:
            stock_buy_value = stock_prices_list[i]
            stock_buy_idx = i

    stock_Sell_idx = medium
    stock_Sell_value = stock_prices_list[medium]
    for i in range(medium+1, stop+1):
        if stock_prices_list[i] > stock_Sell_value:
            stock_Sell_value = stock_prices_list[i]
            stock_Sell_idx = i

    # those two points generate the maximum cross border profit
    profit = stock_Sell_value - stock_buy_value

    # and now compare our three options and find the best one
    if profitcalculatedfromSecondpart > profitcalculatedfromfirstpart:
        if profit > profitcalculatedfromSecondpart:
            return profit, stock_buy_idx, stock_Sell_idx
        else:
            return profitcalculatedfromSecondpart, buy2, sell2
    else:
        if profit > profitcalculatedfromfirstpart:
            return profit, stock_buy_idx, stock_Sell_idx
        else:
            return profitcalculatedfromfirstpart, buy1, sell1

# Main driver Code
if __name__ == "__main__":
    try:
        with open("outputPS5.txt","w+") as record_output:
            # read stock details  available for previous from inputPS5a.txt
            with open("inputPS5.txt",'r') as readStocksOfPreviousDays:
                sizeOfStockData=readStocksOfPreviousDays.readlines()
                if len(sizeOfStockData) != 0:
                    price = []
                    for i in sizeOfStockData:
                        if '/' in i:
                            day,Stockprice= i.split('/')
                            price.append(int(Stockprice))
                    if len(price) < 2:
                        record_output.write("\nWarning : Stock price data must be given atleast for two days !")
                    else :
                        invalidDecreasingDatasetFlag = bool(all(i < price[0] for i in price[1:]))
                        invalidContinuityDatasetFlag = bool(all(i == price[0] for i in price[1:]))
                        if invalidDecreasingDatasetFlag is True:
                            record_output.write("\nWarning : No solution possible since future price is not increased")
                        elif invalidContinuityDatasetFlag is True:
                            record_output.write("\nWarning : No solution possible since future price is same for all the days")
                        else:
                            totalprofit,buy,sell=maxProfitWithIterativeApproach(price)
                            totalprofit2,buy2,sell2=maxProfitcalculationWithDivideandConquerRecursion(price,0,len(price)-1)
                            if totalprofit == buy == sell == totalprofit2 == buy2 == sell2 == 0:
                                record_output.write("\nWarning : Stock price data must be given atleast for two days !")
                            else:
                                record_output.write("\nMaximum Profit(Iterative Solution):"+ str(totalprofit)+"\nDay to buy: "+str(buy)+"\nDay to sell: "+str(sell))
                                record_output.write("\nMaximum Profit(Divide & Conquer):"+ str(totalprofit2)+"\nDay to buy: "+str(buy2)+"\nDay to sell: "+str(sell2))
                else:
                    record_output.write("\nERROR: Stock price data input file can not be blank !")
    except FileNotFoundError:
        record_output.write("\nERROR: Place input files named as InputPS5a.txt and enter stock data in desired format like i.e. day/stockprice")
    except Exception:
        print("\nERROR: InputPS5a.txt file data is corrputed so update gently !")
        traceback.print_exc() 
    finally:
        record_output.close()