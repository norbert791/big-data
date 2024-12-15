import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
def read_csv_file(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Create box plots
def create_box_plots(data):
    try:
        # Set up the plotting style
        sns.set(style="whitegrid")

        # Create the box plot for errHll grouped by card
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='card', y='errHll', data=data, palette='Set2')
        plt.title('Box Plot of errHll by card')
        plt.xlabel('Card')
        plt.ylabel('errHll')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Create the box plot for errLL grouped by card
        plt.figure(figsize=(12, 6))
        sns.boxplot(x='card', y='errLL', data=data, palette='Set3')
        plt.title('Box Plot of errLL by card')
        plt.xlabel('Card')
        plt.ylabel('errLL')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error creating plots: {e}")

# Main function
def main():
    file_path = 'results.csv'
    data = read_csv_file(file_path)

    if data is not None:
        if {'card', 'errHll', 'errLL'}.issubset(data.columns):
            create_box_plots(data)
        else:
            print("The CSV file does not have the required columns: 'card', 'errHll', 'errLL'.")

if __name__ == "__main__":
    main()
