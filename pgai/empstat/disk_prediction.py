# evaluate an ARIMA model using a walk-forward validation
import pandas
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima.model import ARIMA
# from sklearn.metrics import mean_squared_error
# from math import sqrt
# load dataset
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')
# series = read_csv('disk_usage.csv', header=0, index_col=0, parse_dates=True, squeeze=True, date_parser=parser)
# series.index = series.index.to_period('M')

# disk_usage = [{"Month":"1-01","Usage":212},{"Month":"1-02","Usage":230},{"Month":"1-04","Usage":238},{"Month":"1-03","Usage":251},{"Month":"1-05","Usage":269},{"Month":"1-06","Usage":276},{"Month":"1-07","Usage":287},{"Month":"1-08","Usage":295},{"Month":"1-09","Usage":306},{"Month":"1-10","Usage":310},{"Month":"1-11","Usage":320},{"Month":"1-12","Usage":280},{"Month":"2-01","Usage":291},{"Month":"2-02","Usage":312},{"Month":"2-03","Usage":326},{"Month":"2-04","Usage":333},{"Month":"2-05","Usage":346},{"Month":"2-06","Usage":354},{"Month":"2-07","Usage":361},{"Month":"2-08","Usage":372},{"Month":"2-09","Usage":385},{"Month":"2-10","Usage":396},{"Month":"2-11","Usage":409},{"Month":"2-12","Usage":391},{"Month":"3-01","Usage":403},{"Month":"3-02","Usage":412},{"Month":"3-03","Usage":423},{"Month":"3-04","Usage":436},{"Month":"3-05","Usage":447},{"Month":"3-06","Usage":459},{"Month":"3-07","Usage":463},{"Month":"3-08","Usage":471},{"Month":"3-09","Usage":483},{"Month":"3-10","Usage":491},{"Month":"3-11","Usage":509},{"Month":"3-12","Usage":492}]   
# df = pandas.DataFrame(disk_usage)
# df.index = df.index.to_period('M')

series = read_csv('disk_usage.csv', header=0, index_col=0, parse_dates=True, squeeze=True, date_parser=parser)
series.index = series.index.to_period('M')

# split into train and test sets
X = series.values
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
# walk-forward validation
for t in range(len(test)):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit()
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
# evaluate forecasts
# rmse = sqrt(mean_squared_error(test, predictions))
# print('Test RMSE: %.3f' % rmse)
# plot forecasts against actual outcomes
pyplot.plot(test,label='Actual')
pyplot.plot(predictions, color='red',label='Predicted')
pyplot.xlabel('Months')
pyplot.ylabel('Disk usage')
pyplot.legend()
pyplot.show()

## Results ######
 series = read_csv('disk_usage.csv', header=0, index_col=0, parse_dates=True, squeeze=True, date_parser=parser)
predicted=417.421136, expected=391.000000
predicted=392.919186, expected=403.000000
predicted=406.456008, expected=412.000000
predicted=415.857843, expected=423.000000
predicted=423.710325, expected=436.000000
predicted=439.906958, expected=447.000000
predicted=454.632960, expected=459.000000
predicted=467.046237, expected=463.000000
predicted=470.042021, expected=471.000000
predicted=477.568719, expected=483.000000
predicted=490.073140, expected=491.000000
predicted=497.106384, expected=509.000000
predicted=516.743503, expected=492.000000
