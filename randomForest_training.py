import sys
from pyspark import SparkContext
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors

if __name__ == "__main__":

    # importing the file
    file = sys.argv[1]

    def mapper(line):
        parts = line.split(';')
        points = []
        for i in range(len(parts)-1):
            points.append(parts[i])
        return LabeledPoint(float(parts[len(parts)-1]), Vectors.dense(points))

    sc = SparkContext(appName="WineQualityPrediction")

    # loading and parsing the data
    train_data = sc.textFile(file)
    header = train_data.first()
    filtered_data = train_data.filter(lambda row: row != header)
    train_parsed_data = filtered_data.map(mapper)
    train_parsed_data.cache()

    # building model
    model = RandomForest.trainClassifier(train_parsed_data, numClasses=10, categoricalFeaturesInfo={},
                                         numTrees=10, featureSubsetStrategy="auto",
                                         impurity='gini', maxDepth=4, maxBins=32)

    # Save and load model
    model.save(sc, "myRandomModel")

    sc.stop()
