import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    labels = list()

    with open(filename) as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == "Administrative":
                continue

            ints = [
                row[0], row[2], row[4],
                row[10], row[11], row[12], row[13],
                row[14], row[15], row[16]
            ]
            floats = [
                row[1], row[3], row[5], row[6], row[7],
                row[8], row[9]
            ]

            data = list()
            for i, data_type in enumerate(row):
                if i != 17:
                    if data_type in ints and type(data_type) != int:
                        if i == 10:
                            months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                            data.append(months.index(data_type))
                        elif i == 15:
                            if data_type == "Returning_Visitor":
                                data.append(1)
                            else:
                                data.append(0)
                        elif i == 16:
                            if data_type == "FALSE":
                                data.append(0)
                            else:
                                data.append(1)
                        else:
                            data.append(int(data_type))
                    elif data_type in floats and type(data_type) != float:
                        data.append(float(data_type))

                else:
                    if data_type == "FALSE":
                        labels.append(0)
                    else:
                        labels.append(1)

            evidence.append(data)
        return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive_predictions = 0
    positive_labels = 0
    negative_predictions = 0
    negative_labels = 0

    for label, prediction in zip(labels, predictions):
        if label == prediction:
            if prediction == 1:
                positive_predictions += 1
            if prediction == 0:
                negative_predictions += 1
            
        if label == 1:
            positive_labels += 1
        if label == 0:
            negative_labels += 1
        

    sensitivity = positive_predictions / positive_labels if positive_predictions < positive_labels else 1
    specificity = negative_predictions / negative_labels if negative_predictions < negative_labels else 1

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
