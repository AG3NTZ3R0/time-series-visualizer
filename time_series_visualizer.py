import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
def parse_date(x):
    return dt.datetime.strptime(x, '%Y-%m-%d')

df = pd.read_csv('fcc-forum-pageviews.csv', index_col=['date'], parse_dates=['date'], date_parser=parse_date)

# Clean data
df = df.loc[
  (df['value'] >= df['value'].quantile(0.025))
  & (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(16, 6))

    ax = sns.lineplot(data=df, x='date', y='value')

    ax.set(xlabel='Date', ylabel='Page Views', title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    # fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = (df.copy().groupby(pd.Grouper(freq='M')).mean().rename(columns={'value': 'avg'}))
    df_bar['year'] = pd.DatetimeIndex(df_bar.index).year
    df_bar['month'] = pd.DatetimeIndex(df_bar.index).strftime('%B')
    df_bar = pd.melt(df_bar, id_vars=['year', 'month'], value_vars=['avg'])

    # Draw bar plot
    sns.set_theme(style="ticks")
    fig = sns.catplot(data=df_bar, x='year', y='value', hue='month', kind='bar', legend=False)
    fig.set_xlabels('Years')
    fig.set_ylabels('Average Page Views')
    month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    plt.legend(title='Months', loc='upper left', labels=month_lst)
    fig = fig.fig

    # Save image and return fig (don't change this part)
    # fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy().rename(columns={'value':'Page Views', 'month':'Month'})
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    sns.boxplot(ax=ax1, data=df_box, x=df_box['year'], y=df_box['Page Views'])

    ax1.set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')
    ax2.set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')

    month_lst_abbv = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(ax=ax2, data=df_box, x=df_box['Month'], y=df_box['Page Views'], order=month_lst_abbv)

    # Unable to solve text_box_plot_labels fail
    # Save image and return fig (don't change this part)
    # fig.savefig('box_plot.png')
    return fig
