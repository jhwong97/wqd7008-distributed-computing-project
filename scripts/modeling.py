import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pmdarima as pm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates
from sklearn.metrics import r2_score

def data_split(split_ratio, data):
    train_data_list = []
    test_data_list = []
    for value in split_ratio:
        train_size = int(value * len(data))
        test_size = len(data) - train_size
        train_data = df_model_actual.iloc[:train_size]
        test_data = df_model_actual.iloc[train_size:]
        train_data_list.append(train_data)
        test_data_list.append(test_data)
    return train_data_list, test_data_list

def plot_data_split(split_ratio, data, attribute, nrow, ncol, figsize_x, figsize_y):
    train_data_list, test_data_list = data_split(split_ratio, data)
    fig, axs = plt.subplots(nrow, ncol, figsize = (figsize_x,figsize_y))
    
    for count in range(len(train_data_list)):
        train_data = pd.DataFrame(train_data_list[count][attribute])
        train_data['Legend'] = 'Train'
        test_data = pd.DataFrame(test_data_list[count][attribute])
        test_data['Legend'] = 'Test'
        df =pd.concat([train_data, test_data])
    
        sns.lineplot(ax = axs[count], data = df, x ='date', y='my_total_export', hue ='Legend', palette=['green','red'])
        axs[count].set_title(f"Data Split {int(split_ratio[count]*100)}:{round((int(1)-split_ratio[count])*100)}")
        axs[count].set(xlabel = 'Period', ylabel = "MY_Exports (USD Billions)")
        
    plt.tight_layout()
    plt.savefig('/home/ubuntu/result/figures/data-split.jpg', format='jpeg')

def arima_modeling(original_data, train_data_list, test_data_list, seasonal, attribute):
    data_fc = []
    data_lower = []
    data_upper = []
    data_aic = []
    data_fitted = []
    data_index_of_fc = []
    
    for i in range(len(train_data_list)):
        train_data = train_data_list[i][attribute]
        test_data = test_data_list[i][attribute]
        for i in range(len(seasonal)):
            model = pm.auto_arima(train_data,         # time se
                                  m=12,               # frequency of series                      
                                  seasonal=seasonal[i],     # TRUE if seasonal series
                                  stationary=False,
                                  d=None,             # let model determine 'd'
                                  test='adf',         # use adftest to find optimal 'd'
                                  start_p=0, start_q=0, # minimum p and q
                                  max_p=12, max_q=12, # maximum p and q
                                  D=None,             # let model determine 'D'
                                  max_order=None,
                                  trace=False,
                                  error_action='ignore',  
                                  suppress_warnings=True, 
                                  stepwise=True)
            print(model.summary)
            fc, confint = model.predict(n_periods=len(test_data), return_conf_int=True)
            index_of_fc = pd.date_range(pd.to_datetime(train_data.index[-1])  + relativedelta(months = +1), periods = len(test_data), freq = 'MS')
            
            data_fc.append(fc)
            data_lower.append(confint[:,0])
            data_upper.append(confint[:,1])
            data_aic.append(model.aic())
            data_fitted.append(model.fittedvalues())
            data_index_of_fc.append(index_of_fc)
            actual = test_data['my_total_export']
            forecast = fc
            mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
            rmse = np.mean((forecast - actual)**2)**.5  # RMSE
            r2 = r2_score(actual, forecast) #R2
            print(f'MAPE: {mape}, RMSE: {rmse}, R2: {r2}')

    df_act_fc_list = []
    df_lower_list = []
    df_upper_list = []
    df_fitted_list = []
    
    for i in range(len(data_fc)):
        df_fc = pd.DataFrame(index = data_index_of_fc[i])
        df_lower = pd.DataFrame(index = data_index_of_fc[i])
        df_upper = pd.DataFrame(index = data_index_of_fc[i])
        df_aic = pd.DataFrame()
        df_fitted = pd.DataFrame(index = original_data.index)

        df_fc['my_total_export'] = data_fc[i]
        df_lower['my_total_export'] = data_lower[i]
        df_upper['my_total_export'] = data_upper[i]
        df_aic['my_total_export'] = data_aic[i]
        df_fitted['my_total_export'] = data_fitted[i]
        
        actual_data = original_data['my_total_export'].copy()
        actual_data = pd.DataFrame(actual_data)
        forecast_data = df_fc
        actual_data['desc'] = 'Actual'
        forecast_data['desc'] = 'Forecast'
        df_act_fc = pd.concat([actual_data, forecast_data]).reset_index()
        df_act_fc = df_act_fc.rename(columns={'index': 'date'})
        df_act_fc_list.append(df_act_fc)
        df_lower_list.append(df_lower)
        df_upper_list.append(df_upper)
        df_fitted_list.append(df_fitted)
        
    return df_act_fc_list, df_fitted_list, df_lower_list, df_upper_list

def arima_result_plot(df_act_fc_list, df_fitted_list, df_lower_list, df_upper_list,nrow, ncol):
    
    years = mdates.YearLocator()    # every year
    months = mdates.MonthLocator()  # every month
    years_fmt = mdates.DateFormatter('%Y')
    
    fig, axs = plt.subplots(nrow, ncol, figsize = (20,20))
    
    for i in range(len(df_act_fc_list)):
        df_melt = df_act_fc_list[i].melt(id_vars = ['date', 'desc'])
        df_melt_fitted = df_fitted_list[i].reset_index().melt(id_vars = ['date'])

        # Filter data for the current category
        df_plot = df_melt[df_melt['variable'] == 'my_total_export']
        df_lower_plot = df_lower_list[i]['my_total_export']
        df_upper_plot = df_upper_list[i]['my_total_export']
        df_plot_fitted = df_melt_fitted[df_melt_fitted['variable'] == 'my_total_export']

        # Plot the actual and forecasted data
        sns.lineplot(ax = axs[i], data = df_plot, x = 'date', y = 'value', hue = 'desc', marker = 'o')
        # Plot the fitted data with dashed lines
        sns.lineplot(ax = axs[i], data = df_plot_fitted, x = 'date', y = 'value', dashes=True, alpha = 0.5)
        # Set the x-label, y-label, and fill between the lower and upper bounds of the forecast
        axs[i].set_xlabel('my_total_export', size = 12)
        axs[i].set_ylabel('USD Billions', size = 12)
        axs[i].fill_between(df_lower_plot.index, 
                         df_lower_plot, 
                         df_upper_plot, 
                         color='k', alpha=.15)
        # Set the legend and y-limits
        axs[i].legend(loc = 'upper left')
        axs[i].set_ylim([df_plot['value'].min(), df_plot['value'].max()])

        # Set the x-axis tickers and format
        axs[i].xaxis.set_major_locator(years)
        axs[i].xaxis.set_major_formatter(years_fmt)
        axs[i].xaxis.set_minor_locator(months)
        
    plt.tight_layout()
    plt.savefig('/home/ubuntu/result/figures/arima_result.jpg', format='jpeg')
    

df_model_actual = pd.read_csv("/home/ubuntu/result/prepared_dataset.csv")
df_model_actual = df_model_actual.drop(['trade_balance'], axis=1)
df_model_actual['date'] = pd.to_datetime(df_model_actual['date'], infer_datetime_format=True)
df_model_actual = df_model_actual.set_index(['date'])

split_ratio = [0.7,0.8]
data = df_model_actual
train_data_list, test_data_list = data_split(split_ratio, data)
plot_data_split(split_ratio, data, attribute=['my_total_export'], nrow=2, ncol=1, figsize_x=15, figsize_y=15)

df_act_fc_list, df_fitted_list, df_lower_list, df_upper_list = arima_modeling(original_data=df_model_actual,
                                                                                train_data_list=train_data_list,
                                                                                test_data_list=test_data_list,
                                                                                seasonal=[False, True],
                                                                                attribute=['my_total_export'])

arima_result_plot(df_act_fc_list, 
                  df_fitted_list, 
                  df_lower_list, 
                  df_upper_list, 
                  nrow=4, ncol=1)