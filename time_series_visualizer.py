from calendar import month_name
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df.set_index('date')
# Clean data
cleaned=df.copy()
#print(len(cleaned))
for y in df.index:
        if ((df.iloc[y,1]) < (df['value'].quantile(0.025))) or ((df.iloc[y,1]) > (df['value'].quantile(0.975))):
            cleaned.drop(df.index[y],inplace=True)
#print(len(cleaned))
df=cleaned.copy()

def draw_line_plot():
    # Draw line plot
    df['date'] = pd.to_datetime(df.date)
    #print(df.date)
    fig, ax = plt.subplots(figsize=[18, 10])
    ax.plot(df['date'],df['value'])
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    #print(df.groupby(pd.Grouper(key='date', axis=0,freq='M')).mean())
    """ df_bar = df.groupby(pd.Grouper(key='date', axis=0,freq='M')).mean()
    print(df_bar) """
    """ df_bar_asc = df_bar.sort_values(by='date', ascending=True)
    print(df_bar) """
    months = month_name[1:]
    df['months'] = pd.Categorical(df.date.dt.strftime('%B'), categories=months, ordered=True)

    #print(df['months'])
    # pivot the dataframe into the correct shape
    dfp = pd.pivot_table(data=df, index=df.date.dt.year, columns='months', values='value')

    #print(dfp.head())
    # Draw bar plot
    fig,ax=plt.subplots()
    dfp.plot(ax=ax,kind='bar', figsize=(12, 4), ylabel='Average Page Views', xlabel='Years', rot=0)
    legend = ax.legend(bbox_to_anchor=(1, 1.02), loc='upper left')
    legend.set_title("Months", prop = {'size':12})
    
    



    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    print(df_box)
    # Draw box plots (using Seaborn)
    fig,ax=plt.subplots(1,2,figsize=[18, 10])
    #df_box.boxplot(by ='year', column =['value'], grid = False,ax=ax)
    
    sns.set_style("whitegrid")
  
    sns.boxplot(x = 'year', y = 'value', data = df_box,ax=ax[0]).set(title='Year-wise Box Plot (Trend)', xlabel='Year', ylabel='Page Views')
    
    df_box['month'] = pd.Categorical(df_box['month'], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    df_box.sort_values(by='month',inplace=True)
    sns.boxplot(x = 'month', y = 'value', data = df_box,ax=ax[1]).set(title='Month-wise Box Plot (Seasonality)', xlabel='Month', ylabel='Page Views')



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
