import sys
from pyspark import SparkContext
from pyspark.mllib.tree import RandomForestModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.evaluation import MulticlassMetrics


if __name__ == "__main__":

    # importing the file
    file = sys.argv[1]

    def mapper(line):
        parts = line.strip().split(";")
        points = []
        for i in range(len(parts) - 1):
            points.append(parts[i])
        return LabeledPoint(float(parts[len(parts)-1]), Vectors.dense(points))

    sc = SparkContext(appName="WineQualityPrediction")

    # loading and parsing the data
    validation_data = sc.textFile("ValidationDataset.csv")
    # comment the above line and uncomment the below line for docker image
    #  validation_data = sc.textFile("/TestData/TestDataset.csv")
    header = validation_data.first()
    filtered_data = validation_data.filter(lambda row: row != header)
    val_parsed_data = filtered_data.map(mapper)
    val_parsed_data.cache()

    # loading the model and predicting the values
    model = RandomForestModel.load(sc, "myRandomModel")
    predictions = model.predict(val_parsed_data.map(lambda x: x.features))
    labelsAndPredictions = val_parsed_data.map(lambda lp: lp.label).zip(predictions)

    # computing F1 score
    metrics = MulticlassMetrics(labelsAndPredictions)
    f_score = metrics.weightedFMeasure()
    print()
    print()
    print("F1 score : " +str(f_score))

    sc.stop()
