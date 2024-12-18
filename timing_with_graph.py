import timeit
import statistics

def pandas_approach(input_size: int):
    SETUP_CODE = {
        'merge': '''
from task_i_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_df, date_dim_df, dwelling_df, electricity_df = input_df
electricity_df.iloc[:input_size]
''',
        'transform': '''
from task_i_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_df, date_dim_df, dwelling_df, electricity_df = input_df
electricity_df.iloc[:input_size]
merged_df = merge(area_df, date_dim_df, dwelling_df, electricity_df)
''',
        'make_output': '''
from task_i_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_df, date_dim_df, dwelling_df, electricity_df = input_df
electricity_df.iloc[:input_size]
merged_df = merge(area_df, date_dim_df, dwelling_df, electricity_df)
denormalized_df = transform(merged_df)
'''
    }

    TEST_CODES = {
        'merge': 'merged_df = merge(area_df, date_dim_df, dwelling_df, electricity_df)',
        'transform': 'denormalized_df = transform(merged_df)',
        'make_output': 'result = make_output(denormalized_df)'
    }

    timing_results = {}

    # Time each component with appropriate setup
    for operation in ['merge', 'transform', 'make_output']:
        times = timeit.repeat(
            setup=SETUP_CODE[operation],
            stmt=TEST_CODES[operation],
            repeat=2,
            number=5
        )
        timing_results[operation] = {
            'min': min(times),
            'max': max(times),
            'avg': statistics.mean(times),
            'std': statistics.stdev(times)
        }

    # Print results in a readable format
    print("\nTiming Results for Pandas Approach(in seconds):")
    for operation, results in timing_results.items():
        print(f"\n{operation.upper()}:")
        print(f"Minimum: {results['min']:.4f}")
        print(f"Maximum: {results['max']:.4f}")
        print(f"Average: {results['avg']:.4f}")
        print(f"Std Dev: {results['std']:.4f}")

    return timing_results

def pure_python_approach():
    SETUP_CODE = {
        'merge': '''
from task_i_non_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_data, date_dim_data, dwelling_data, electricity_data = input_df
''',
        'transform': '''
from task_i_non_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_data, date_dim_data, dwelling_data, electricity_data = input_df
merged_data = merge(area_data, date_dim_data, dwelling_data, electricity_data)
''',
        'make_output': '''
from task_i_non_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_data, date_dim_data, dwelling_data, electricity_data = input_df
merged_data = merge(area_data, date_dim_data, dwelling_data, electricity_data)
denormalized_data = transform(merged_data)
'''
    }

    TEST_CODES = {
        'merge': 'merged_data = merge(area_data, date_dim_data, dwelling_data, electricity_data)',
        'transform': 'denormalized_data = transform(merged_data)',
        'make_output': 'result = make_output(denormalized_data)'
    }

    timing_results = {}

    # Time each component with appropriate setup
    for operation in ['merge', 'transform', 'make_output']:
        times = timeit.repeat(
            setup=SETUP_CODE[operation],
            stmt=TEST_CODES[operation],
            repeat=2,
            number=5
        )
        timing_results[operation] = {
            'min': min(times),
            'max': max(times),
            'avg': statistics.mean(times),
            'std': statistics.stdev(times)
        }

    # Print results in a readable format
    print("\nTiming Results for non-Pandas, Pure Python Approach(in seconds):")
    for operation, results in timing_results.items():
        print(f"\n{operation.upper()}:")
        print(f"Minimum: {results['min']:.4f}")
        print(f"Maximum: {results['max']:.4f}")
        print(f"Average: {results['avg']:.4f}")
        print(f"Std Dev: {results['std']:.4f}")

    return timing_results

if __name__ == "__main__":
    pandas_approach()
    pure_python_approach()