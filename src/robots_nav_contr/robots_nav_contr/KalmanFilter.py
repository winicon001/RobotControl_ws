# Kalman Filter for Encoder Noise Reduction
# This script simulates the use of a Kalman Filter to reduce noise in encoder readings.
# The Kalman Filter is a recursive algorithm that estimates the state of a dynamic system from a series of noisy measurements.
# It is particularly useful in robotics for sensor fusion and state estimation.
# The script generates simulated noisy encoder readings, applies the Kalman Filter, and plots the results.
# The Kalman Filter is initialized with the first measurement, and the transition and observation matrices are set to 1.
# The transition covariance and observation covariance are set to 0.1 and 2, respectively.
# The script uses the pykalman library to implement the Kalman Filter.
# The results are plotted using matplotlib, showing the true position, noisy measurements, and filtered output.
# The script also prints the true values, noisy measurements, and filtered output to the console.
# The Kalman Filter is a powerful tool for reducing noise in sensor readings and improving the accuracy of state estimation in robotics.
# The script can be modified to work with real encoder data by replacing the simulated noisy measurements with actual readings.
# The Kalman Filter can be tuned by adjusting the transition and observation covariances to better fit the characteristics of the specific system being used.
# The Kalman Filter is widely used in robotics for tasks such as localization, mapping, and sensor fusion.
# It is a fundamental algorithm in the field of robotics and is essential for building reliable and accurate robotic systems.

import numpy as np
from pykalman import KalmanFilter
import matplotlib.pyplot as plt

# Simulated noisy encoder readings
true_values = np.linspace(0, 100, 50)  # True position values
noise = np.random.normal(0, 2, 50)  # Gaussian noise
measurements = true_values + noise  # Noisy measurements

def kalman_filter(measurements):
    # Initialize Kalman Filter
    kf = KalmanFilter(initial_state_mean=measurements[0],
                      initial_state_covariance=1,
                      transition_matrices=[1],
                      observation_matrices=[1],
                      transition_covariance=0.1,
                      observation_covariance=2)

    # Apply Kalman Filter
    filtered_state_means, _ = kf.filter(measurements)
    
    return filtered_state_means

def main(measurements):
    # Apply Kalman Filter to noisy measurements
    filtered_state_means = kalman_filter(measurements)
    # Plot results
    plt.plot(true_values, label="True Position", linestyle="dashed")
    plt.plot(measurements, label="Noisy Measurements", alpha=0.6)
    plt.plot(filtered_state_means, label="Filtered Output", linewidth=2)
    plt.legend()
    plt.xlabel("Time Step")
    plt.ylabel("Position")
    plt.title("Kalman Filter for Encoder Noise Reduction")
    plt.show()
    # Print results
    print("True Values: ", true_values)
    print("Noisy Measurements: ", measurements)
    print("Filtered Output: ", filtered_state_means)

if __name__ == "__main__":
    # Run Kalman Filter
    main()

    

    
   
