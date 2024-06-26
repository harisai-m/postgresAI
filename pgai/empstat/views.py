from django.shortcuts import render
from .models import Employee,Fuelconsumption,WeatherData,Sales
from django.db.models import Count
import matplotlib.pyplot as plt
import pandas as pd
import os
from django.apps import apps
from io import StringIO
from django.urls import reverse
from pandas import read_csv
from pandas.plotting import autocorrelation_plot
from pandas import DataFrame
from statsmodels.tsa.arima.model import ARIMA


def home(request):
    context = {
        'project_title': 'PostgreAI',
        'subtitle': 'Intelligence to Postgres',
        'data_analysis_description': "PostgreAI's Data Analysis feature transforms generic data from PostgreSQL tables into actionable insights. By loading table data into a Pandas DataFrame, users gain access to an array of statistical metrics, including means, medians, and standard deviations. The application provides a quick overview of the data by displaying the first 5 rows and essential DataFrame information like data types and non-null counts. For better data comprehension, PostgreAI creates graphs illustrating the distribution of distinct values in selected columns. Moreover, it offers time series analysis capabilities, automatically detecting timestamp columns and generating graphical representations to uncover trends and patterns over time.",
        'forecasting_description': "In the realm of forecasting, PostgreAI leverages predefined models to predict future outcomes based on diverse data sources, encompassing sales data, weather data, and database/server monitoring data. Through efficient data loading into Pandas DataFrames, the system prepares data for comprehensive analysis and pattern recognition. Using advanced algorithms, PostgreAI identifies meaningful patterns and relationships within the data, subsequently constructing predictive models for target fields such as sales, profit, or disk usage. With these predictive models, users gain the power to make informed decisions and forecasts, whether predicting future sales trends or anticipating resource utilization patterns. PostgreAI simplifies the process of data-driven forecasting, offering valuable insights for strategic planning and decision-making.",
    }
    return render(request, 'pgai/home.html', context)


def model_list(request):
    # Get a list of all your Django models
    app_name = 'empstat'
    models = apps.get_app_config(app_name).get_models() 
    # app = apps.get_app_config(app_name)
    # models = app.get_models()

    # Create a list of dictionaries with model names and their URLs
    model_data = []
    for model in models:
        model_data.append({
            'model_name': model._meta.verbose_name,
            'model_url':  reverse('model_details', args=[model._meta.object_name])
        })
    
    # Pass the list of model names to the template
    context = {
        'models': model_data,
    }

    return render(request, 'pgai/model_list.html', context)

def model_details(request, model_name):
    # Find the model based on the name in the URL
    model = apps.get_model('empstat', model_name)

    # Retrieve data from the selected model and convert it to a DataFrame
    queryset = model.objects.all().values()
    df = pd.DataFrame.from_records(queryset)

    # Calculate summary statistics (describe)
    describe_data = df.describe()

    # Capture the output of df.info() as a string
    info_output = StringIO()
    df.info(buf=info_output)
    info_data = info_output.getvalue()
    info_output.close()

    # Pass the model details to the template
    context = {
        'model_name': model_name,
        'data_frame': df.head().to_html(classes='table table-striped table-bordered table-sm'),
        'describe': describe_data.to_html(classes='table table-striped table-bordered table-sm'),
        'info': info_data,
    }

    return render(request, 'pgai/model_details.html', context)




def data_analysis_model(request, model_name):
    model = apps.get_model('empstat', model_name)
    data = model.objects.all()
    analysis_results = analyze_discreate_data_model(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/data_analysis.html', context)


def analyze_discreate_data_model(data):
    if not data:
        return "No data to analyze."

    columns_info = []
    for field in data[0]._meta.get_fields():
        column_name = field.name
        column_type = field.get_internal_type()

        # Check if the column contains discrete strings or numbers
        is_discrete_string = False
        is_discrete_to_show = False
        is_number = False
        distinct_values = list()
        count_of_col = len(data)
        chart_filename = 'image.png'


        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            if len(distinct_values) <= 0.4 * count_of_col:
                is_discrete_to_show = True
                        # Generate a bar chart for discrete columns
                if distinct_values:
                    plt.figure(figsize=(15, 6))
                    plt.bar(distinct_values, [data.filter(**{column_name: val}).count() for val in distinct_values])
                    plt.title(f'Distinct Values Count for {column_name}')
                    plt.xlabel(column_name)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
                    plt.close()
        elif column_type in ['IntegerField', 'FloatField', 'DecimalField']:
                is_number = True
                

        columns_info.append({
            'column_name': column_name,
            'column_type': column_type,
            'is_discrete_string': is_discrete_string,
            'is_number': is_number,
            'distinct_values': distinct_values,
            'count_of_col': count_of_col,
            'is_discrete_to_show': is_discrete_to_show,
            'chart_filename': chart_filename,

        })

    return columns_info


#  Old code

def ml_features(request):
    app_name = 'empstat'
    models = apps.get_app_config(app_name).get_models()
    model_data = {}
    # records_count = WeatherData.objects.count()

    # Distinct departments and their counts
    # station_city = WeatherData.objects.values('Station_City').annotate(count=Count('Station_City'))

    for model in models:
        # Retrieve data from the current model and convert it to a DataFrame
        queryset = model.objects.all().values()
        df = pd.DataFrame.from_records(queryset)

        # Calculate summary statistics (describe)
        describe_data = df.describe()

        # Capture the output of df.info() as a string
        info_output = StringIO()
        df.info(buf=info_output)
        info_data = info_output.getvalue()
        info_output.close()

        # Store the data for the current model in the dictionary
        model_name = model.__name__
        model_data[model_name] = {
            'data_frame': df.head().to_html(classes='table table-striped table-bordered table-sm'),
            'describe': describe_data.to_html(classes='table table-striped table-bordered table-sm'),
            'info': info_data,
        }

    # Pass the model data to the template
    context = {
        'model_data': model_data,
    }

    return render(request, 'pgai/ml_features.html', context)



def data_analysis(request):
    data = Fuelconsumption.objects.all()
    analysis_results = analyze_discreate_data(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/data_analysis.html', context)


def analyze_discreate_data(data):
    if not data:
        return "No data to analyze."

    columns_info = []
    for field in data[0]._meta.get_fields():
        column_name = field.name
        column_type = field.get_internal_type()

        # Check if the column contains discrete strings or numbers
        is_discrete_string = False
        is_discrete_to_show = False
        is_number = False
        distinct_values = list()
        count_of_col = len(data)
        chart_filename = 'image.png'


        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            if len(distinct_values) <= 0.4 * count_of_col:
                is_discrete_to_show = True
                        # Generate a bar chart for discrete columns
                if distinct_values:
                    plt.figure(figsize=(15, 6))
                    plt.bar(distinct_values, [data.filter(**{column_name: val}).count() for val in distinct_values])
                    plt.title(f'Distinct Values Count for {column_name}')
                    plt.xlabel(column_name)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
                    plt.close()
        elif column_type in ['IntegerField', 'FloatField', 'DecimalField']:
                is_number = True
                

        columns_info.append({
            'column_name': column_name,
            'column_type': column_type,
            'is_discrete_string': is_discrete_string,
            'is_number': is_number,
            'distinct_values': distinct_values,
            'count_of_col': count_of_col,
            'is_discrete_to_show': is_discrete_to_show,
            'chart_filename': chart_filename,

        })

    return columns_info

def timeseries_analysis(request):
    data = WeatherData.objects.all()
    analysis_results = analyze_timeseries_data(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/data_analysis.html', context)

def analyze_timeseries_data(data):
    if not data:
        return "No data to analyze."
    
    columns_info = []
    for field in data[0]._meta.get_fields():
        column_name = field.name
        column_type = field.get_internal_type()

        # Check if the column contains discrete strings or numbers
        is_discrete_string = False
        is_discrete_to_show = False
        is_number = False
        distinct_values = list()
        count_of_col = len(data)
        chart_filename = 'image.png'
        timestamp_column = ''

        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            # if len(distinct_values) <= 0.1 * count_of_col and len(distinct_values) <= 55:
            if  len(distinct_values) <= 55:
                is_discrete_to_show = True
                        # Generate a bar chart for discrete columns
                if distinct_values:
                    plt.figure(figsize=(25, 6))
                    plt.bar(distinct_values, [data.filter(**{column_name: val}).count() for val in distinct_values])
                    plt.title(f'Distinct Values Count for {column_name}')
                    plt.xlabel(column_name)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
                    plt.close()
        elif column_type in ['IntegerField', 'FloatField', 'DecimalField']:
                is_number = True
                timestamp_column = 'Date_Full'  # Replace with your timestamp column name

                new_york_data = data.filter(Station_City="New York")

                # Generate a line chart for numeric columns based on timestamp
                if timestamp_column:
                    df = pd.DataFrame(list(new_york_data.values(timestamp_column, column_name)))
                    df.set_index(timestamp_column, inplace=True)
                    plt.figure(figsize=(20, 6))
                    plt.scatter(df.index, df[column_name])
                    plt.title(f'{column_name} Over Time')
                    plt.xlabel(timestamp_column)
                    plt.ylabel(column_name)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_vs_date_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai', chart_filename))
                    plt.close()

    
        columns_info.append({
            'column_name': column_name,
            'column_type': column_type,
            'is_discrete_string': is_discrete_string,
            'is_number': is_number,
            'distinct_values': distinct_values,
            'count_of_col': count_of_col,
            'is_discrete_to_show': is_discrete_to_show,
            'chart_filename': chart_filename,
            'timestamp_column': timestamp_column,

        })

    return columns_info


def sales_analysis(request):
    data = Sales.objects.all()
    analysis_results = analyze_sales_data(data)
    context = {
        'analysis_result': analysis_results,
    }
    return render(request, 'pgai/sales_analysis.html', context)

def analyze_sales_data(data):
    if not data:
        return "No data to analyze."
    
    columns_info = []
    for field in data[0]._meta.get_fields():
        column_name = field.name
        column_type = field.get_internal_type()

        # Check if the column contains discrete strings or numbers
        is_discrete_string = False
        is_discrete_to_show = False
        is_number = False
        distinct_values = list()
        count_of_col = len(data)
        chart_filename = 'image.png'
        timestamp_column = ''
        year = 0

        if column_type == 'CharField' or column_type == 'TextField':
            is_discrete_string = True
            distinct_values = data.values_list(column_name, flat=True).distinct()
            # if len(distinct_values) <= 0.1 * count_of_col and len(distinct_values) <= 55:
            if  len(distinct_values) <= 0.5 * count_of_col:
                is_discrete_to_show = True
                # Generate a bar chart for discrete columns
                if distinct_values:
                    plt.figure(figsize=(25, 6))
                    plt.bar(distinct_values, [data.filter(**{column_name: val}).count() for val in distinct_values])
                    plt.title(f'Distinct Values Count for {column_name}')
                    plt.xlabel(column_name)
                    plt.ylabel('Count')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    chart_filename = f'{column_name}_sales_chart.png'
                    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
                    plt.close()

                    columns_info.append({
                    'column_name': column_name,
                    'column_type': column_type,
                    'is_discrete_string': is_discrete_string,
                    'is_number': is_number,
                    'distinct_values': distinct_values,
                    'count_of_col': count_of_col,
                    'is_discrete_to_show': is_discrete_to_show,
                    'chart_filename': chart_filename,
                    'timestamp_column': timestamp_column,
                    

                     })

            


        elif column_type in ['IntegerField', 'FloatField', 'DecimalField']:
                is_number = True
                timestamp_column = 'orderdate'  # Replace with your timestamp column name

                # new_york_data = data.filter(Station_City="New York")
                
                unique_years = data.values_list('year_id', flat=True).distinct()
                if timestamp_column:
                # Generate a line chart for numeric columns based on timestamp
                    for year in sorted(unique_years):
                        year_data = data.filter(year_id=year)
                        df = pd.DataFrame(list(year_data.values(timestamp_column, column_name)))
                        df.set_index(timestamp_column, inplace=True)
                        plt.figure(figsize=(50, 6))
                        plt.scatter(df.index, df[column_name])
                        plt.title(f'{column_name} Over Time')
                        plt.xlabel(timestamp_column)
                        plt.ylabel(column_name)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        chart_filename = f'{column_name}_vs_date_for_{year}_chart.png'
                        plt.savefig(os.path.join('empstat/static/pgai', chart_filename))
                        plt.close()

                        columns_info.append({
                        'column_name': column_name,
                        'column_type': column_type,
                        'is_discrete_string': is_discrete_string,
                        'is_number': is_number,
                        'distinct_values': distinct_values,
                        'count_of_col': count_of_col,
                        'is_discrete_to_show': is_discrete_to_show,
                        'chart_filename': chart_filename,
                        'timestamp_column': timestamp_column,
                        'year': year,

                         })



    
        

    return columns_info


def forecasting(request):
    # shows forecasting abilities
    forecasting_abilities = ["Sales_Pridiction","Capacity_Planing","Future_Trends","Stockmarket_Prediction"]
    model_data = []
    for ability in forecasting_abilities:
        model_data.append({
            'model_name': ability,
            'model_url': reverse(ability,args=[ability])
        })
    # Pass the list of model names to the template
    context = {
        'models': model_data,
    }

    return render(request, 'pgai/forecasting.html', context)

def Sales_Pridiction(request,model_name):
    
    shampoo_sales = [ { "Month": "1-01", "Sales": 266.0 }, { "Month": "1-02", "Sales": 145.9 }, { "Month": "1-03", "Sales": 183.1 }, { "Month": "1-04", "Sales": 119.3 }, { "Month": "1-05", "Sales": 180.3 }, { "Month": "1-06", "Sales": 168.5 }, { "Month": "1-07", "Sales": 231.8 }, { "Month": "1-08", "Sales": 224.5 }, { "Month": "1-09", "Sales": 192.8 }, { "Month": "1-10", "Sales": 122.9 }, { "Month": "1-11", "Sales": 336.5 }, { "Month": "1-12", "Sales": 185.9 }, { "Month": "2-01", "Sales": 194.3 }, { "Month": "2-02", "Sales": 149.5 }, { "Month": "2-03", "Sales": 210.1 }, { "Month": "2-04", "Sales": 273.3 }, { "Month": "2-05", "Sales": 191.4 }, { "Month": "2-06", "Sales": 287.0 }, { "Month": "2-07", "Sales": 226.0 }, { "Month": "2-08", "Sales": 303.6 }, { "Month": "2-09", "Sales": 289.9 }, { "Month": "2-10", "Sales": 421.6 }, { "Month": "2-11", "Sales": 264.5 }, { "Month": "2-12", "Sales": 342.3 }, { "Month": "3-01", "Sales": 339.7 }, { "Month": "3-02", "Sales": 440.4 }, { "Month": "3-03", "Sales": 315.9 }, { "Month": "3-04", "Sales": 439.3 }, { "Month": "3-05", "Sales": 401.3 }, { "Month": "3-06", "Sales": 437.4 }, { "Month": "3-07", "Sales": 575.5 }, { "Month": "3-08", "Sales": 407.6 }, { "Month": "3-09", "Sales": 682.0 }, { "Month": "3-10", "Sales": 475.3 }, { "Month": "3-11", "Sales": 581.3 }, { "Month": "3-12", "Sales": 646.9 } ]
    shampoo_sales_df = pd.DataFrame(shampoo_sales)

    # Calculate summary statistics (describe)
    describe_data = shampoo_sales_df.describe()

    # Capture the output of df.info() as a string
    info_output = StringIO()
    shampoo_sales_df.info(buf=info_output)
    info_data = info_output.getvalue()
    info_output.close()



    # Pass the model details to the template
    context = {
        'model_name': model_name,
        'data_frame': shampoo_sales_df.head().to_html(classes='table table-striped table-bordered table-sm'),
        'describe': describe_data.to_html(classes='table table-striped table-bordered table-sm'),
        'info': info_data,
    }

    return render(request,'pgai/Sales_Pridiction.html', context)

def Capacity_Planing(request,model_name):
    
    disk_usage = [{"Month":"1-01","Usage":212},{"Month":"1-02","Usage":230},{"Month":"1-04","Usage":238},{"Month":"1-03","Usage":251},{"Month":"1-05","Usage":269},{"Month":"1-06","Usage":276},{"Month":"1-07","Usage":287},{"Month":"1-08","Usage":295},{"Month":"1-09","Usage":306},{"Month":"1-10","Usage":310},{"Month":"1-11","Usage":320},{"Month":"1-12","Usage":280},{"Month":"2-01","Usage":291},{"Month":"2-02","Usage":312},{"Month":"2-03","Usage":326},{"Month":"2-04","Usage":333},{"Month":"2-05","Usage":346},{"Month":"2-06","Usage":354},{"Month":"2-07","Usage":361},{"Month":"2-08","Usage":372},{"Month":"2-09","Usage":385},{"Month":"2-10","Usage":396},{"Month":"2-11","Usage":409},{"Month":"2-12","Usage":391},{"Month":"3-01","Usage":403},{"Month":"3-02","Usage":412},{"Month":"3-03","Usage":423},{"Month":"3-04","Usage":436},{"Month":"3-05","Usage":447},{"Month":"3-06","Usage":459},{"Month":"3-07","Usage":463},{"Month":"3-08","Usage":471},{"Month":"3-09","Usage":483},{"Month":"3-10","Usage":491},{"Month":"3-11","Usage":509},{"Month":"3-12","Usage":492}]   
    df = pd.DataFrame(disk_usage)

    # Calculate summary statistics (describe)
    describe_data = df.describe()

    # Capture the output of df.info() as a string
    info_output = StringIO()
    df.info(buf=info_output)
    info_data = info_output.getvalue()
    info_output.close()



    # Pass the model details to the template
    context = {
        'model_name': model_name,
        'data_frame': df.head().to_html(classes='table table-striped table-bordered table-sm'),
        'describe': describe_data.to_html(classes='table table-striped table-bordered table-sm'),
        'info': info_data,
    }

    return render(request,'pgai/disk_usage.html', context)

def Future_Trends(request,model_name):
    pass
    
def Stockmarket_Prediction(request,model_name):
    pass

def shampoo_sales_prediction(request):

    shampoo_sales = [ { "Month": "1-01", "Sales": 266.0 }, { "Month": "1-02", "Sales": 145.9 }, { "Month": "1-03", "Sales": 183.1 }, { "Month": "1-04", "Sales": 119.3 }, { "Month": "1-05", "Sales": 180.3 }, { "Month": "1-06", "Sales": 168.5 }, { "Month": "1-07", "Sales": 231.8 }, { "Month": "1-08", "Sales": 224.5 }, { "Month": "1-09", "Sales": 192.8 }, { "Month": "1-10", "Sales": 122.9 }, { "Month": "1-11", "Sales": 336.5 }, { "Month": "1-12", "Sales": 185.9 }, { "Month": "2-01", "Sales": 194.3 }, { "Month": "2-02", "Sales": 149.5 }, { "Month": "2-03", "Sales": 210.1 }, { "Month": "2-04", "Sales": 273.3 }, { "Month": "2-05", "Sales": 191.4 }, { "Month": "2-06", "Sales": 287.0 }, { "Month": "2-07", "Sales": 226.0 }, { "Month": "2-08", "Sales": 303.6 }, { "Month": "2-09", "Sales": 289.9 }, { "Month": "2-10", "Sales": 421.6 }, { "Month": "2-11", "Sales": 264.5 }, { "Month": "2-12", "Sales": 342.3 }, { "Month": "3-01", "Sales": 339.7 }, { "Month": "3-02", "Sales": 440.4 }, { "Month": "3-03", "Sales": 315.9 }, { "Month": "3-04", "Sales": 439.3 }, { "Month": "3-05", "Sales": 401.3 }, { "Month": "3-06", "Sales": 437.4 }, { "Month": "3-07", "Sales": 575.5 }, { "Month": "3-08", "Sales": 407.6 }, { "Month": "3-09", "Sales": 682.0 }, { "Month": "3-10", "Sales": 475.3 }, { "Month": "3-11", "Sales": 581.3 }, { "Month": "3-12", "Sales": 646.9 } ]
    df = pd.DataFrame(shampoo_sales)

    plt.figure(figsize=(15, 6))
    df.plot()
    plt.title(f'Shampoo Sales for 3 years')
    plt.xlabel('Months')
    plt.ylabel('Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart_filename = f'Shampoo_Sales_chart.png'
    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
    plt.close()
    # shampoo_sales_forecast_chart = f""

    fc_chart = f'Shampoo_sales_fc_last_year.png'

    context = {
        'chart_filename': chart_filename,
        'fc_chart': fc_chart
    }

    return render(request, 'pgai/shampoo_sales_fc.html', context)


def disk_usage_prediction(request):

    disk_usage = [{"Month":"1-01","Usage":212},{"Month":"1-02","Usage":230},{"Month":"1-04","Usage":238},{"Month":"1-03","Usage":251},{"Month":"1-05","Usage":269},{"Month":"1-06","Usage":276},{"Month":"1-07","Usage":287},{"Month":"1-08","Usage":295},{"Month":"1-09","Usage":306},{"Month":"1-10","Usage":310},{"Month":"1-11","Usage":320},{"Month":"1-12","Usage":280},{"Month":"2-01","Usage":291},{"Month":"2-02","Usage":312},{"Month":"2-03","Usage":326},{"Month":"2-04","Usage":333},{"Month":"2-05","Usage":346},{"Month":"2-06","Usage":354},{"Month":"2-07","Usage":361},{"Month":"2-08","Usage":372},{"Month":"2-09","Usage":385},{"Month":"2-10","Usage":396},{"Month":"2-11","Usage":409},{"Month":"2-12","Usage":391},{"Month":"3-01","Usage":403},{"Month":"3-02","Usage":412},{"Month":"3-03","Usage":423},{"Month":"3-04","Usage":436},{"Month":"3-05","Usage":447},{"Month":"3-06","Usage":459},{"Month":"3-07","Usage":463},{"Month":"3-08","Usage":471},{"Month":"3-09","Usage":483},{"Month":"3-10","Usage":491},{"Month":"3-11","Usage":509},{"Month":"3-12","Usage":492}]   
    df = pd.DataFrame(disk_usage)

    plt.figure(figsize=(15, 6))
    df.plot()
    plt.title(f'Disk Usage for 3 Years')
    plt.xlabel('months')
    plt.ylabel('Disk Usage in GBs')
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart_filename = f'disk_usage_chart.png'
    plt.savefig(os.path.join('empstat/static/pgai/', chart_filename))
    plt.close()

    fc_chart = f'disk_usage_fc_last_year.png'

    context = {
        'max_capacity' : "516.74MB",
        'chart_filename': chart_filename,
        'fc_chart': fc_chart
    }

    return render(request, 'pgai/disk_usage_fc.html', context)