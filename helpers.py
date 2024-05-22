import pandas as pd

def access_data(data, index1, index2):
    accessed_data = [data[0][index1], data[index2][0], data[index1][index2]]
    print("\nData accessed: ", accessed_data)
    return accessed_data

def transform_data(inputData):
    matrix = [inputData.columns.tolist()] 
    matrix += inputData.values.tolist()
    print(matrix)
    return matrix

def open_csv(csv_file):                
    inputData = pd.read_csv(csv_file, header=0)
    print(inputData)
    return inputData

def read_input(csv_file):
    print("Opening file: ", csv_file)  
    inputData = open_csv(csv_file)
    print("\nTransforming data into matrix...")
    data = transform_data(inputData)
    return data

if __name__ == "__main__":
    filename = input("Filename (filename.csv): ")
    data = read_input(filename)
    data_accessed = access_data(data, 3, 2)  
