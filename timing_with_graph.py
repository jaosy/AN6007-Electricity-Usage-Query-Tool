import timeit
import statistics
from complete import get_electricity_data
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate  # For nice table formatting

def pandas_approach(input_size: int):
    SETUP_CODE = {
        'merge': f'''
from task_i_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_df, date_dim_df, dwelling_df, electricity_df = input_df
electricity_df.iloc[:{input_size}]
''',
        'transform': f'''
from task_i_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_df, date_dim_df, dwelling_df, electricity_df = input_df
electricity_df.iloc[:{input_size}]
merged_df = merge(area_df, date_dim_df, dwelling_df, electricity_df)
''',
        'make_output': f'''
from task_i_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_df, date_dim_df, dwelling_df, electricity_df = input_df
electricity_df.iloc[:{input_size}]
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

    # time multiple functions
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

    print("\nTiming Results for Pandas Approach(in seconds):")
    for operation, results in timing_results.items():
        print(f"\n{operation.upper()}:")
        print(f"Minimum: {results['min']:.4f}")
        print(f"Maximum: {results['max']:.4f}")
        print(f"Average: {results['avg']:.4f}")
        print(f"Std Dev: {results['std']:.4f}")

    return timing_results

def pure_python_approach(input_size: int):
    SETUP_CODE = {
        'merge': f'''
from task_i_non_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_data, date_dim_data, dwelling_data, electricity_data = input_df
electricity_data = electricity_data[:{input_size}]
''',
        'transform': f'''
from task_i_non_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_data, date_dim_data, dwelling_data, electricity_data = input_df
electricity_data = electricity_data[:{input_size}]
merged_data = merge(area_data, date_dim_data, dwelling_data, electricity_data)
''',
        'make_output': f'''
from task_i_non_pandas import read_input, merge, transform, make_output

input_df = read_input()
area_data, date_dim_data, dwelling_data, electricity_data = input_df
electricity_data = electricity_data[:{input_size}]
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

    # time multiple functions
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

    return timing_results

if __name__ == "__main__":
    data = get_electricity_data()
    max_input_size = len(data)

    # it is known that the size of the input is at least 20000 from the data exploration portion
    input_sizes = [1000, 5000, 10000, 15000, 20000, max_input_size]
    pandas_timing_sizes = []
    pure_python_timing_sizes = []

    # collect timing results for both approaches
    for size in input_sizes:
        print(f"\nTesting with input size: {size}")
        pandas_result = pandas_approach(size)
        pandas_timing_sizes.append(pandas_result)

        pure_python_result = pure_python_approach(size)
        pure_python_timing_sizes.append(pure_python_result)

    # create two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    operations = ['merge', 'transform', 'make_output']
    colors = ['b', 'g', 'r']

    # Pandas approach
    for op, color in zip(operations, colors):
        avg_times = [result[op]['avg'] for result in pandas_timing_sizes]
        ax1.plot(input_sizes, avg_times, f'{color}o-', label=op.capitalize())

        for i, (size, time) in enumerate(zip(input_sizes, avg_times)):
            ax1.annotate(f'{time:.2f}s', 
                        (size, time),
                        textcoords="offset points",
                        xytext=(0,10),
                        ha='center')

    ax1.set_xlabel('Input Size')
    ax1.set_ylabel('Average Time (seconds)')
    ax1.set_title('Pandas Approach: Time vs Input Size')
    ax1.legend()
    ax1.grid(True)

    # pure Python approach
    for op, color in zip(operations, colors):
        avg_times = [result[op]['avg'] for result in pure_python_timing_sizes]
        ax2.plot(input_sizes, avg_times, f'{color}o-', label=op.capitalize())

        for i, (size, time) in enumerate(zip(input_sizes, avg_times)):
            ax2.annotate(f'{time:.2f}s', 
                        (size, time),
                        textcoords="offset points",
                        xytext=(0,10),
                        ha='center')

    ax2.set_xlabel('Input Size')
    ax2.set_ylabel('Average Time (seconds)')
    ax2.set_title('Pure Python Approach: Time vs Input Size')
    ax2.legend()
    ax2.grid(True)

    def create_comparison_table(pandas_results, python_results, input_sizes):
        comparison_data = []

        for i, size in enumerate(input_sizes):
            for op in operations:
                # Round all numerical values to 2 decimal places
                pandas_time = round(pandas_results[i][op]['avg'], 2)
                python_time = round(python_results[i][op]['avg'], 2)
                diff = round(python_time - pandas_time, 2)
                speedup = round(python_time / pandas_time, 2)

                comparison_data.append({
                    'Input Size': f"{size:,}",  # Format with comma separators
                    'Operation': op.capitalize(),
                    'Pandas Avg (s)': pandas_time,
                    'Python Avg (s)': python_time,
                    'Difference (s)': diff,
                    'Speedup Factor': f"{speedup}x"
                })

        df = pd.DataFrame(comparison_data)

        formatted_table = tabulate(
            df,
            headers={
                'Input Size': 'Size',
                'Operation': 'Operation',
                'Pandas Avg (s)': 'Pandas (s)',
                'Python Avg (s)': 'Python (s)',
                'Difference (s)': 'Diff (s)',
                'Speedup Factor': 'Speedup'
            },
            tablefmt='pretty',
            floatfmt=('', '', '.2f', '.2f', '.2f', '.2f')  # Consistent 2 decimal places
        )

        return formatted_table
    
    print("\nPerformance Comparison Summary:")
    print(create_comparison_table(pandas_timing_sizes, pure_python_timing_sizes, input_sizes))

    print("\nOverall Performance Summary:")
    print("-" * 50)
    for size in input_sizes:
        idx = input_sizes.index(size)
        pandas_total = sum(pandas_timing_sizes[idx][op]['avg'] for op in operations)
        python_total = sum(pure_python_timing_sizes[idx][op]['avg'] for op in operations)
        print(f"\nInput Size: {size}")
        print(f"Total Pandas Time: {pandas_total:.4f}s")
        print(f"Total Python Time: {python_total:.4f}s")
        print(f"Overall Speedup: {python_total/pandas_total:.2f}x")

    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    plt.show()