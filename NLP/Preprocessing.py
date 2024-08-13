import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the  dataset
file_path = "Data/Intern NLP Dataset.xlsx"
df = pd.read_excel(file_path)


def main():
    """
    Main function to preprocess the dataframe.

    This function extracts date, hour, and minute from the 'Time' column,
    drops the 'Time' column, and adds a 'Total_Visitors' column.
    """

    # Preprocess the datetime column to extract date, hour, and minute
    df["Time"] = pd.to_datetime(df["Time"])
    df["Date"] = df["Time"].dt.date
    df["Hour"] = df["Time"].dt.hour
    df["Minute"] = df["Time"].dt.minute

    # Drop columns that we do not need
    df.drop(columns=["Time"], inplace=True)

    # Make a new column for total visitors
    df["Total_Visitors"] = df[
        ["Is Male", "Is Female", "Is Hijab", "Is Child", "Is Niqab", "Has Bag"]
    ].sum(axis=1)

    return df


def plot_corr(df):
    """
    Function to plot a correlation matrix of the numerical features in the dataframe.

    Parameters
    ----------
        df : DataFrame
            The dataframe to plot the correlation matrix for.
    """

    # Extract numerical features for correlation analysis
    numerical_df = df.select_dtypes(include=["number"])
    # Calculate the correlation matrix
    correlation_matrix = numerical_df.corr()
    # Create a heatmap with correlation values displayed
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()


if __name__ == "__main__":
    df = main()
    plot_corr(df)
