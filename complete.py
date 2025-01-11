"""
This program denormalizes electricity usage data by merging multiple data sources into a Pandas DataFrame.

It performs the following main operations:
1. Reads input data from text files
2. Merges different datasets using Pandas
3. Calculate the average electricity usage per region and dwelling type in a specific time period
4. Converts the results to a list of ElectricityRecord objects as per requirements

Author: Jacqueline Ong
Date: 12/16/2024
"""


from task_i_pandas import read_input, merge, transform, make_output


def get_electricity_data():
    datasets = read_input()
    merged_data = merge(datasets[0], datasets[1], datasets[2], datasets[3])
    denormalized_data = transform(merged_data)
    result = make_output(denormalized_data)
    
    return result


# for standalone testing complete.py output
if __name__ == "__main__":
    datasets = read_input()
    merged_data = merge(datasets[0], datasets[1], datasets[2], datasets[3])
    denormalized_data = transform(merged_data)
    result = make_output(denormalized_data)

    print(f"Number of records: {len(result)}")
    print("\nFirst 3 records:")
    for record in result[:3]:
        print(record)