# Origin: https://machinelearningmastery.com/time-series-prediction-with-deep-learning-in-python-with-keras/


# Multilayer Perceptron to Predict International Airline Passengers (t+1, given t)
import numpy as np
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
import os

def convert2float(data):
    out_data = []
    try:
        for d in data:
            out_data.append(list(map(float, d)))
        return out_data
    except:
        return None


WEIGHTS_DIR = os.path.join("..","WEIGHTS")
#PREFIX = "simple_MLP_EURUSD_0"
#PREFIX = "simple_MLP_EURUSD_2_epoch"
PREFIX = "simple_MLP_EURUSD_20_epoch"

# fix random seed for reproducibility
np.random.seed(7)
# load the dataset
# Datum Zeit Eröffnung Hoch Tief Schluss, Ticks
# Row 5 = Schlusskurs
dataframe_train = pandas.read_csv(os.path.join('..','csv_input','EURUSD_train.csv'), usecols=[5], engine='python', skipfooter=3)
dataframe_val = pandas.read_csv(os.path.join('..','csv_input','EURUSD_val.csv'), usecols=[5], engine='python', skipfooter=3)
dataset_train = dataframe_train.values
dataset_val = dataframe_val.values
dataset_train = convert2float(dataset_train)
dataset_val = convert2float(dataset_val)

# split into train and test sets
#train_size = int(len(dataset) * 0.67)
#test_size = len(dataset) - train_size
#train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
train = np.array(dataset_train)
test = np.array(dataset_val)
print(len(train), len(test))
# convert an array of values into a dataset matrix

class MLPPredictor:
    def __init__(self):
        # reshape into X=t and Y=t+1
        self.look_back = 10
        self.trainX, self.trainY = self.create_dataset(train, self.look_back)
        self.testX, self.testY = self.create_dataset(test, self.look_back)
        #self.model = self.create_small_model()
        self.model = self.create_medium_model()
        #self.model = self.create_large_model()


    def create_dataset(self, dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            a = dataset[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return np.array(dataX), np.array(dataY)

    def create_small_model(self):
        # create and fit Multilayer Perceptron model
        model = Sequential()
        model.add(Dense(8, input_dim=self.look_back, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        # 97 parameter
        return model

    def create_medium_model(self):
        # create and fit Multilayer Perceptron model
        model = Sequential()
        model.add(Dense(3000, input_dim=self.look_back, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        # 36K parameter
        return model

    def create_large_model(self):
        # create and fit Multilayer Perceptron model
        model = Sequential()
        model.add(Dense(5417, input_dim=self.look_back, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        # 65K parameter
        return model

    def create_very_large_model(self):
        # create and fit Multilayer Perceptron model
        model = Sequential()
        model.add(Dense(8125, input_dim=self.look_back, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        # 97,5K parameter
        return model

    def train(self):
        self.model.fit(self.trainX, self.trainY,  validation_data=(self.testX, self.testY), nb_epoch=20, batch_size=20, verbose=1)
        self.model.save_weights(os.path.join(WEIGHTS_DIR, PREFIX + "_final.h5"), overwrite=True)

    def load_model(self, path):
        self.model.load_weights(path)

    def eval(self):

        # Estimate self.model performance
        trainScore = self.model.evaluate(self.trainX, self.trainY, verbose=0)
        print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
        testScore = self.model.evaluate(self.testX, self.testY, verbose=0)
        print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))
        # generate predictions for training
        trainPredict = self.model.predict(self.trainX)
        testPredict = self.model.predict(self.testX)
        # shift train predictions for plotting
        trainPredictPlot = np.empty_like(dataset_train)
        trainPredictPlot[:, :] = np.nan
        trainPredictPlot[self.look_back:len(trainPredict)+self.look_back, :] = trainPredict


        # plot baseline and predictions
        plt.plot(dataset_train, "r--", label="Groundtruth")
        plt.plot(trainPredictPlot, "g--", label="Prediction")
        plt.legend()
        plt.show()

        # shift test predictions for plotting
        testPredictPlot = np.empty_like(dataset_val)
        testPredictPlot[:, :] = np.nan
        testPredictPlot[self.look_back:len(dataset_val)-1, :] = testPredict

        plt.plot(dataset_val, "r--", label="Groundtruth")
        plt.plot(testPredictPlot, "g--",  label="Prediction")
        plt.show()

if __name__ == "__main__":
    predictor = MLPPredictor()
    #PREFIX = "simple_MLP_EURUSD_20_epoch_medium"
    #predictor.model = predictor.create_medium_model()
    #predictor.train()
    PREFIX = "simple_MLP_EURUSD_20_epoch_large"
    predictor.model = predictor.create_large_model()
    #predictor.train()
    predictor.load_model(os.path.join(WEIGHTS_DIR, PREFIX + "_final.h5"))
    predictor.eval()



