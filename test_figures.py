import pandas as pd
from pandas import DataFrame 
import numpy
import matplotlib.pyplot as plt


def make_random_figure():
    """ Makes a random figure (using pandas)

    Returns a matplotlib figure
    """

    # make some fake data or use numpy to get random data
    Data = {'Unemployment_Rate' : [6.1,5.8,5.7,5.7,5.8,5.6,5.5,5.3,5.2,5.2],
            'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
    }
    # or get some real data from here https://pandas-datareader.readthedocs.io/en/latest/

    # pull data into a dataframe
    df = DataFrame(Data,columns=['Unemployment_Rate','Stock_Index_Price'])
    # fig = df.plot()
    # fig = df.plot(x ='Unemployment_Rate', y='Stock_Index_Price', kind = 'scatter')
    # return fig
    return df 

    


if __name__ == "__main__":

    df = make_random_figure()
    df.to_html('test_this.html')
