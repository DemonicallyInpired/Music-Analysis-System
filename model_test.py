import numpy as np
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import argparse
import ftplib
from ftplib import socket
import preprocessing as pp
import verify
from tensorflow.keras.models import load_model
from Attention import Attention
import warnings
warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument("--ftp", action='store_true')
parser.add_argument("--host", help="Hostname of your FTP")
parser.add_argument("--user", help="Username of your FTP account.")
parser.add_argument("--password", help="Password of your FTP account.")

parser.add_argument("--local", help="Directory of your files")

args = parser.parse_args()

def ftp_connection(host, user, password):

    try:
        ftp = ftplib.FTP(host)
        ftp.login(user, password)
        
        print("FTP Connection Established.")

        filenames = ftp.nlst()

        if os.path.isdir('data'):
            pass
        else:
            os.mkdir("data")

        for filename in filenames:
            if filename == '.' or filename == '.ftpquota' or filename == '..':
                continue

            if filename.split('.')[1] == 'py' or filename.split('.')[1] == 'json':

                file_exists = os.path.isfile(filename)

                if file_exists:
                    print("{} already exists.".format(filename))
                    continue
                else:
                    print("Downloading: {}".format(filename))
                    local_files = os.path.join(os.getcwd(), filename)
                    file = open(local_files, 'wb')
                    ftp.retrbinary("RETR "+ filename, file.write)
                    file.close()
            else:

                file_exists = os.path.isfile("data\\{}".format(filename))

                if file_exists:
                    print("{} already exists.".format(filename))
                    continue
                else:
                    print("Downloading: {}".format(filename))
                    local_files = os.path.join(os.getcwd(), "data\\{}".format(filename))
                    file = open(local_files, 'wb')
                    ftp.retrbinary("RETR "+ filename, file.write)
                    file.close()

        print("\nAll files have been downloaded.")

        ftp.quit()

        if os.path.isfile("manifest.json"):
            verified_files = verify.verify()
        else:
            print("Manifest file is missing, skipping prediction.")
            exit()

        if len(verified_files) > 0:
            x_test = convert_to_dataframe(verified_files)
            x_df = np.array(pp.convert_wav_to_image(x_test, 'data'))

            prediction = model_prediction(x_df)
            for i in range(len(x_test)):
                print("Instruments Used in {}:".format(x_test.iloc[i]['audio']))
                print("Instrument 1: {}%".format(round(prediction[i][0]*100, 2)))
                print("Instrument 41: {}%".format(round(prediction[i][1]*100, 2)))
                print("Instrument 42: {}%".format(round(prediction[i][2]*100, 2)))
                print("Instrument 43: {}%".format(round(prediction[i][3]*100, 2)))
                print("Instrument 44: {}%".format(round(prediction[i][4]*100, 2)))
                print("Instrument 61: {}%".format(round(prediction[i][5]*100, 2)))
                print("Instrument 69: {}%".format(round(prediction[i][6]*100, 2)))
                print("Instrument 7: {}%".format(round(prediction[i][7]*100, 2)))
                print("Instrument 71: {}%".format(round(prediction[i][8]*100, 2)))
                print("Instrument 72: {}%".format(round(prediction[i][9]*100, 2)))
                print("Instrument 74: {}%".format(round(prediction[i][10]*100, 2)))
                print()
        else:
            print("No files available to predict.")

    except socket.gaierror:
        print("AUTH FAILED: Hostname could not be resolved.")
    except ftplib.error_perm as e:
        print(e)
    except PermissionError:
        print("Permission Denied.")

def local_directory(dir):
    # Left for Sagar
    pass

def convert_to_dataframe(li):
    return pd.DataFrame(li, columns=[['audio']])

def model_prediction(df):
    model = load_model("model.h5", custom_objects={'Attention': Attention})
    return model.predict(df)

if args.ftp == False and args.local == None:
    print("Please provide either --ftp or --local argument.")
    exit()

elif args.local and args.ftp:
    parser.print_help()
    exit()

elif args.ftp:
    if not args.host:
        print("Please provide a hostname.")
        exit()
    if not args.user:
        print("Please provide a username.")
        exit()
    if not args.password:
        print("Please provide a password.")
        exit()

    if args.host and args.user and args.password:
        ftp = ftp_connection(args.host, args.user, args.password)

elif args.local:
    if os.path.isdir(args.local):
        local_directory(args.local)
    else:
        print("Please provide a valid directory.")