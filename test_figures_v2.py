import pandas as pd
from pandas import DataFrame 
import numpy
import matplotlib.pyplot as plt
from data import Data

def make_dataframe():
    #Data = {'Unemployment_Rate' : [6.1,5.8,5.7,5.7,5.8,5.6,5.5,5.3,5.2,5.2],
    #        'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
    #}
    
    #df = DataFrame(Data,columns=['Unemployment_Rate','Stock_Index_Price'])
    #return df
    pass

    
def make_scatter():
    """ Makes a random figure (using pandas)

    Returns a matplotlib figure
    """
    

    # make some fake data or use numpy to get random data
    
    # or get some real data from here https://pandas-datareader.readthedocs.io/en/latest/

    # pull data into a dataframe
    
    # fig = df.plot()
    df = DataFrame(Data,columns=['Unemployment_Rate','Stock_Index_Price'])
    fig = df.plot(x ='Unemployment_Rate', y='Stock_Index_Price', kind = 'scatter')
    # return fig
    return fig 

def make_bar():
    
    pass


if __name__ == "__main__":
        fig = make_scatter()
        plt.show()
