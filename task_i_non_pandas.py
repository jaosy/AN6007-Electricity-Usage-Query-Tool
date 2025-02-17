"""
This program denormalizes electricity usage data by merging multiple data sources without Pandas (pure Python).

It performs the following main operations:
1. Reads input data from text files line-by-line
2. Constructs a dictionary for each row (line) of data in each file
3. Merges the list of dictionaries (merge datasets)
3. Calculate the average electricity usage per region and dwelling type in a specific time period
4. Converts the results to a list of ElectricityRecord objects as per requirements

Author: Jacqueline Ong
Date: 12/16/2024
"""


from models import ElectricityRecord

def read_input():
    area_data = []
    with open('Area.txt', 'r') as file:
        # skip the header row
        next(file) 
        for line in file:
            area_id, area, region = line.strip().split(';')
            datapoint = {}
            datapoint['area_id'] = int(area_id)
            datapoint['area'] = area
            datapoint['region'] = region
            area_data.append(datapoint)
            
    date_dim_data = []
    with open('DateDim.txt', 'r') as file: 
        # skip the header row
        next(file)
        for line in file:
            date_id, year, month, quarter = line.strip().split(';')
            datapoint = {}
            datapoint['date_id'] = int(date_id)
            datapoint['year'] = year
            datapoint['month'] = month
            datapoint['quarter'] = quarter
            date_dim_data.append(datapoint)

    dwelling_data = []
    with open('Dwelling.txt', 'r') as file:
        # skip the header row
        next(file)
        for line in file:
            type_id, dwelling_type = line.strip().split(',')
            datapoint = {}
            datapoint['type_id'] = int(type_id)
            datapoint['dwelling_type'] = dwelling_type
            dwelling_data.append(datapoint)

    electricity_data = []
    with open('Electricity.txt', 'r') as file:
        # skip the header row
        next(file)
        for line in file:
            date_id, area_id, dwelling_type_id, kwh_per_acc = line.strip().split(';')
            datapoint = {}
            datapoint['date_id'] = int(date_id)
            datapoint['area_id'] = int(area_id)
            datapoint['type_id'] = int(dwelling_type_id)
            datapoint['kwh_per_acc'] = float(kwh_per_acc)
            electricity_data.append(datapoint)

    return [area_data, date_dim_data, dwelling_data, electricity_data]


def merge(area_data, date_dim_data, dwelling_data, electricity_data):
    merged_data = []

    for electricity_record in electricity_data:
        for area in area_data:
            if electricity_record['area_id'] == area['area_id']:
                merged_record = {**electricity_record, **area}
                merged_data.append(merged_record)

    date_dict = {record['date_id']: record for record in date_dim_data} # O(n)
    for i in range(len(merged_data)): # O(m)
        date_id = merged_data[i]['date_id'] # O(1)
        if date_id in date_dict:
            merged_data[i] = {**date_dict[date_id], **merged_data[i]} 


    dwelling_dict = {record['type_id']: record for record in dwelling_data}
    for i in range(len(merged_data)):
        type_id = merged_data[i]['type_id']
        if type_id in dwelling_dict:
            merged_data[i] = {**dwelling_dict[type_id], **merged_data[i]}

    return merged_data


# select relevant columns
def transform(merged_data):
    denormalized_data = [{
        'region': record['region'],
        'area': record['area'],
        'year': record['year'],
        'month': record['month'],
        'dwelling_type': record['dwelling_type'],
        'avg_kwh_per_acc': record['kwh_per_acc']
    } for record in merged_data]

    # sort the result
    denormalized_data.sort(key=lambda x: (
        x['area'],
        x['year'],
        x['month'],
        x['dwelling_type']
    ))

    return denormalized_data


def make_output(denormalized_data):
    final_records = [ElectricityRecord(record['region'], record['area'], record['year'], record['month'], record['dwelling_type'], record['avg_kwh_per_acc']) for record in denormalized_data]

    return final_records


if __name__ == "__main__":
    datasets = read_input()
    merged_data = merge(datasets[0], datasets[1], datasets[2], datasets[3])
    denormalized_data = transform(merged_data)
    result = make_output(denormalized_data)

    print(f"Number of records: {len(result)}")
    print("\nFirst 3 records:")
    for record in result[:3]:
        print(record)