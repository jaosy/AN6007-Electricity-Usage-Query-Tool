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


# merging DataFrames using Pandas library functions
def merge(area_df: pd.DataFrame, date_dim_df: pd.DataFrame, dwelling_df: pd.DataFrame, electricity_df: pd.DataFrame) -> pd.DataFrame:
    merged_df = pd.merge(electricity_df, area_df, on='AreaID', how='inner')
    merged_df = pd.merge(merged_df, date_dim_df, on='DateID', how='inner')
    merged_df = pd.merge(merged_df, dwelling_df, left_on='dwelling_type_id', right_on='TypeID', how='inner')

    return merged_df


def transform(merged_df: pd.DataFrame):
    denormalized_df = merged_df.groupby(['Region', 'Area', 'year', 'month', 'dwelling_type'])['kwh_per_acc'].mean().reset_index()
    denormalized_df = denormalized_df.rename(columns={'kwh_per_acc': 'avg_kwh_per_acc'})
    denormalized_df['avg_kwh_per_acc'] = denormalized_df['avg_kwh_per_acc'].round(2)
    denormalized_df = denormalized_df.sort_values(['Area', 'year', 'month', 'dwelling_type'])

    return denormalized_df


def make_output(denormalized_df: pd.DataFrame):
    records = [
        ElectricityRecord(
            region=row.Region,
            area=row.Area,
            year=row.year,
            month=row.month,
            dwelling_type=row.dwelling_type,
            avg_kwh_per_acc=row.avg_kwh_per_acc
        )
        
        for row in denormalized_df.itertuples()
    ]

    return records


if __name__ == "__main__":
    input_df = read_input()
    merged_df = merge(input_df[0], input_df[1], input_df[2], input_df[3])
    denormalized_df = transform(merged_df)
    result = make_output(denormalized_df)

    print(f"Number of records: {len(result)}")
    print("\nFirst 3 records:")
    for record in result[:3]:
        print(record)