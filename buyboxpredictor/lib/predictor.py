from keras.models import load_model
import os


class Predictor():

    def predict(self,data_inputs):
        cwd = os.getcwd()

        model = load_model(cwd+"/buyboxpredictor/lib/buybox_predictor_model.h5")

        data_inputs = self.normalize_data([data_inputs])
        print(data_inputs)

        result = model.predict([data_inputs]).round()

        if result[0][0] == 1.0:
            return True
        return False        

    def normalize_data(self,datas):
        highest = [99.0, 999, 1, 99.99, 96, 1, 9.94]

        for i in range(len(datas)):        
            for j in range(len(highest)):
                if datas[i][j] == True:
                    print(datas[i][j])
                    datas[i][j] = 1.0
                elif datas[i][j] == False:
                    print(datas[i][j])
                    datas[i][j] = 0.0
                else:
                    datas[i][j] = float(datas[i][j])/float(highest[j])    

        return datas