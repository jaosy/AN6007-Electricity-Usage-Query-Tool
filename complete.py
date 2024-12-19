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


import pandas as pd
from models import ElectricityRecord


def read_input():
    area_df = pd.read_csv('Area.txt', sep=';')
    date_dim_df = pd.read_csv('DateDim.txt', sep=';')
    dwelling_df = pd.read_csv('Dwelling.txt', sep=',')
    electricity_df = pd.read_csv('Electricity.txt'
    , sep=';')

    return [area_df, date_dim_df, dwelling_df, electricity_df]


def merge(area_df: pd.DataFrame, date_dim_df: pd.DataFrame, dwelling_df: pd.DataFrame, electricity_df: pd.DataFrame) -> pd.DataFrame:
    merged_df = pd.merge(electricity_df, area_df, on='AreaID', how='inner')
    merged_df = pd.merge(merged_df, date_dim_df, on='DateID', how='inner')
    merged_df = pd.merge(merged_df, dwelling_df, left_on='dwelling_type_id', right_on='TypeID', how='inner')

    return merged_df


# select relevant columns
def transform(merged_df: pd.DataFrame):
    df = merged_df[['Region', 'Area', 'year', 'month', 'dwelling_type', 'kwh_per_acc']]
    df = df.sort_values(['Area', 'year', 'month', 'dwelling_type'])

    return df


def make_output(denormalized_df: pd.DataFrame):
    records = [
        ElectricityRecord(
            region=row.Region,
            area=row.Area,
            year=row.year,
            month=row.month,
            dwelling_type=row.dwelling_type,
            avg_kwh_per_acc=row.kwh_per_acc
        )
        
        for row in denormalized_df.itertuples()
    ]

    return records


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