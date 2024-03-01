import numpy as np
import joblib
import warnings

warnings.filterwarnings('ignore')

model = joblib.load('/home/kazimovzaman2/Backend-Hackathon/apps/aidetect/isolation_forest_model.joblib')
scaler = joblib.load('/home/kazimovzaman2/Backend-Hackathon/apps/aidetect/scaler.joblib')


def check_for_anomaly(data: list):
    """
    This function checks for anomaly in the data using the trained model and scaler and returns the result.
    :param data: [calorie, step_count, active_time]
    :return: {'message': ''}
    """

    data = np.array(data).reshape((1, -1))
    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)

    if prediction == 1:
        return {'message': 'Anomaly detected!'}
    else:
        return {'message': 'No anomaly detected!'}


if __name__ == '__main__':
    data = [2000, 1000, 100]
    print(check_for_anomaly(data))
