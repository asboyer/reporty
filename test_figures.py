import pandas as pd
from pandas import DataFrame 
import numpy
import matplotlib.pyplot as plt


def make_random_figure():
    """ Makes a random figure (using pandas)

    Returns a matplotlib figure
    """
    pass

    # make some fake data or use numpy to get random data
    # Corona cases and deaths in MASS
    
    # how would I include dates?
    Data = {'Cases' : [0,1017,2033,4946,2106,1045,3840,101,23,428],
            'Death': [0,15,100,152,177,90,179,35,210,17]
    }
    # or get some real data from here https://pandas-datareader.readthedocs.io/en/latest/

    # pull data into a dataframe
    df = DataFrame(Data,columns=['Death','Cases'])
    # fig = df.plot()
    # fig = df.plot(x ='Death', y='Cases', kind = 'scatter')
    # return fig
    # return fig 
    return df
    

    


if __name__ == "__main__":

    fig = make_random_figure()
    df.to_html('test_this.html')
