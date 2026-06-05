import pandas as pd

print("Script started...")

TRAIN_PATH = "data/KDDTrain+.txt"
TEST_PATH = "data/KDDTest+.txt"

def load_data():
    print("Loading dataset...")

    train_df = pd.read_csv(TRAIN_PATH, header=None)
    test_df = pd.read_csv(TEST_PATH, header=None)

    print("Train Shape:", train_df.shape)
    print("Test Shape:", test_df.shape)

    return train_df, test_df


if __name__ == "__main__":
    print("Main block running...")

    train, test = load_data()

    print("First rows:")
    print(train.head())