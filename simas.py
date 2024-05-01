

import numpy as np
import scipy.stats as stats

def mm1_queue_simulation(lambda_rate, mu_rate, simulation_time, num_replications):
    # Convert simulation time from hours to customers
    num_customers = int(simulation_time * lambda_rate)

    # Initialize lists to store results
    avg_time_in_queue = []
    avg_time_in_system = []
    avg_queue_length = []
    avg_num_in_system = []
    server_utilization = []

    for _ in range(num_replications):
        # Generate interarrival times and service times
        interarrival_times = np.random.exponential(1/lambda_rate, num_customers)
        service_times = np.random.exponential(1/mu_rate, num_customers)

        # Initialize lists to store times
        arrival_times = np.cumsum(interarrival_times)
        service_end_times = np.zeros(num_customers)
        service_start_times = np.zeros(num_customers)

        for i in range(num_customers):
            if i == 0:
                service_start_times[i] = arrival_times[i]
            else:
                service_start_times[i] = max(arrival_times[i], service_end_times[i-1])
            service_end_times[i] = service_start_times[i] + service_times[i]

        wait_times = service_start_times - arrival_times
        time_in_system = wait_times + service_times

        # Calculate metrics
        avg_time_in_queue.append(np.mean(wait_times))
        avg_time_in_system.append(np.mean(time_in_system))
        avg_queue_length.append(np.mean(wait_times * lambda_rate))
        avg_num_in_system.append(np.mean(time_in_system * lambda_rate))
        server_utilization.append(np.sum(service_times) / (num_customers / lambda_rate))

    # Calculate theoretical values
    theoretical_time_in_queue = 1 / (mu_rate - lambda_rate)
    theoretical_time_in_system = 1 / (mu_rate - lambda_rate) + 1 / mu_rate
    theoretical_queue_length = lambda_rate / (mu_rate * (mu_rate - lambda_rate))
    theoretical_num_in_system = lambda_rate / (mu_rate - lambda_rate)
    theoretical_server_utilization = lambda_rate / mu_rate

    theoretical_values = [theoretical_time_in_queue, theoretical_time_in_system, theoretical_queue_length, theoretical_num_in_system, theoretical_server_utilization]

    # Calculate 95% confidence intervals and relative errors for each metric
    metrics = [avg_time_in_queue, avg_time_in_system, avg_queue_length, avg_num_in_system, server_utilization]
    confidence_intervals = [(np.mean(metric), stats.norm.interval(0.95, loc=np.mean(metric), scale=stats.sem(metric)), abs(np.mean(metric) - theoretical_values[i]) / theoretical_values[i]) for i, metric in enumerate(metrics)]

    return confidence_intervals

# Run the simulation for 30, 100, and 1000 replications
for num_replications in [30, 100, 1000]:
    confidence_intervals = mm1_queue_simulation(3, 4, 500, num_replications)
    print(f"\nFor {num_replications} replications:")
    print(f"Average time in queue: {confidence_intervals[0][0]} hours, 95% CI: {confidence_intervals[0][1]}, Relative Error: {confidence_intervals[0][2]}")
    print(f"Average time in system: {confidence_intervals[1][0]} hours, 95% CI: {confidence_intervals[1][1]}, Relative Error: {confidence_intervals[1][2]}")
    print(f"Average queue length: {confidence_intervals[2][0]} customers, 95% CI: {confidence_intervals[2][1]}, Relative Error: {confidence_intervals[2][2]}")
    print(f"Average number in system: {confidence_intervals[3][0]} customers, 95% CI: {confidence_intervals[3][1]}, Relative Error: {confidence_intervals[3][2]}")
    print(f"Server utilization: {confidence_intervals[4][0]}, 95% CI: {confidence_intervals[4][1]}, Relative Error: {confidence_intervals[4][2]}")
