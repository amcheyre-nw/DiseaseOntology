import os.path
import gzip
import time
import codecs
import pandas as pd
import csv
import argparse


def read_csv(filename):
    data = []
    columns = [3, 4, 5, 6, 8, 9, 10]

    # import shutil
    # with gzip.open('file.txt.gz', 'rb') as f_in:
    #     with open('file.txt', 'wb') as f_out:
    #         shutil.copyfileobj(f_in, f_out)

    # start = time.time()
    # read data in chunks of 1 million rows at a time
    # chunks = pd.read_csv(filename, chunksize=100000, usecols= columns)
    # end = time.time()
    # print("Read csv with chunks: ", (end - start), "sec")
    # pd_df = pd.concat(chunks)

    with open(filename, 'r') as f:
        records = csv.reader(f)
        n = 1
        for record in records:
            if n % 230000 == 0:
                break
            row = []
            n += 1
            if record[4] == 'C0525045' or record[8] == 'C0525045':
                for column in columns:
                    row.append(record[column])
                data.append(row)
    # print(data)
    df = pd.DataFrame(data)
    df.columns = ['Predicate', 'Subject_CUI', 'Subject_Name', 'Subject_Semtype', 'Object_CUI', 'Object_Name',
                  'Object_Semtype']
    df = df[
        ['Subject_Name', 'Predicate', 'Object_Name', 'Subject_CUI', 'Subject_Semtype', 'Object_CUI', 'Object_Semtype']]
    print(df)
    return df


parser = argparse.ArgumentParser(description='Extract Information from SemMed Database')
parser.add_argument('--path', type=str, help='location of the SemMed DB predications file in the format csv.gz')
args = parser.parse_args()
df = read_csv(args.path)
print('Finished parsing the database')
path = os.path.split(args.path)
df.to_csv(os.path.join(path[0], 'ExtractedPredications.csv'), header=True, index=None)
print('Finished saving the extracted predications')
