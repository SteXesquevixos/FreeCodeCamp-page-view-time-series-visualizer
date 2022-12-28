import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

'''Open the file and set the column names'''
df = pd.read_csv('fcc-forum-pageviews.csv', index_col=0)
df.index = pd.to_datetime(df.index)

'''Clean the data by filtering out days when the page views were in the top 2.5% of the dataset 
    or bottom 2.5% of the dataset.'''
df = df[(df['value'] > df['value'].quantile(0.025)) &
        (df['value'] < df['value'].quantile(0.975))]

'''Create a draw_line_plot function that uses Matplotlib to draw a line chart similar to "examples/Figure_1.png". 
    The title should be Daily freeCodeCamp Forum Page Views 5/2016-12/2019. The label on the x axis should be Date 
    and the label on the y axis should be Page Views'''


def draw_line_plot():
    # Plotting the graphic using Matplotlip
    plt.figure(figsize=(15, 5))

    ax = sns.lineplot(x='date', y='value', data=df)
    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    fig = ax.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')

    return fig

'''Create a draw_bar_plot function that draws a bar chart similar to "examples/Figure_2.png". It should show average 
    daily page views for each month grouped by year. The legend should show month labelsand have a title of Months. 
    On the chart, the label on the x axis should be Years and the label on the y axis should be Average Page Views'''


def draw_bar_plot():
    # Average of page views per month
    df_bar = df.resample('MS').mean()

    # Renaming the column 'Page Views' for 'Average Page Views'
    df_bar = df_bar.rename(columns={'value': 'Average Page Views'})

    # Adding a column called 'Month' and 'Year' to show average daily page views for each month grouped by year
    df_bar['month'] = df_bar.index.month_name()
    df_bar['year'] = df_bar.index.year

    # Grouping the columns
    df_grouped = df_bar.groupby(['year', df_bar.index, 'month', 'Average Page Views'])

    # Plotting the graphic using Seaborn
    plt.figure(figsize=(10, 9))

    ax = sns.barplot(x='year',
                     y='Average Page Views',
                     hue_order=['January', 'February', 'March', 'April', 'May', 'June', 'July',
                                'August', 'September', 'October', 'November', 'December'],
                     hue="month",
                     data=df_bar)

    ax.set(xlabel='Years', ylabel='Average Page Views', title='')
    ax.legend(loc='upper left', title='Months')

    fig = ax.get_figure()
    fig.savefig('bar_plot.png')

    return fig


'''Create a draw_box_plot function that uses Seaborn to draw two adjacent box plots similar to "examples/Figure_3.png". 
    These box plots should show how the values are distributed within a given year or month and how it compares over 
    time. The title of the firstchart should be Year-wise Box Plot (Trend) and the title of the econd chart should be 
    Month-wise Box Plot (Seasonality). Make sure he month labels on bottom start at Jan and the x and y axis are labeled
     correctly. The boilerplate includes commands to prepare the data'''


def draw_box_plot():
    # Treating the data
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Plotting the graphs using Seaborn
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # First graph
    sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
    ax[0].set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')

    # Second graph
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1],
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax[1].set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')

    fig.savefig('box_plot.png')

    return fig