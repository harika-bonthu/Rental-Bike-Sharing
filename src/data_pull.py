import numpy as np
import pandas as pd
import os
from src.config import Config
from application_logger.logger import applogger
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
filename = os.path.basename(__file__)

class datasetfetcher:
    """
    This class shall be used to fetch and save the data from a Cassandra database.
    """
    def __init__(self):
        self.classname = self.__class__.__name__
        self.logger_object = applogger()
        self.file_object = open("Logs/db_logs.txt", 'a+')

        self.logger_object.log(self.file_object, f'Current Script: {filename}')
        self.logger_object.log(self.file_object, f'Entered the class: {self.classname}')
        
        Config.ORIGINAL_DATASET_FILE_PATH.mkdir(parents=True, exist_ok=True)
        self.logger_object.log(self.file_object, 'Created original_data folder in assets directory')

        self.fetch_dataset()
        

    def fetch_dataset(self):
        self.funcname = self.fetch_dataset.__name__
        self.logger_object.log(self.file_object, f'Entered the function: {self.funcname} of the class: {self.classname}')
        try:
            cloud_config= {
                'secure_connect_bundle': Config.Bundle
            }
            auth_provider = PlainTextAuthProvider('FLRoqfqpSoLwFEqPADARSlNu', 'PW12rmeePoCbS8TOuw8F6,tkqMB,F-ZnnjaZIH3,BfloA1GBUsLB8,6doLucSPj54b-aHYKFaAK3F0kQZamXIbm0leuboNrz1DFxS05vOxgOt78BD60Zmf0n8AcRpSC9')
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect()
            row = session.execute("select release_version from system.local").one()
            if row:
                # print(row[0])
                self.logger_object.log(self.file_object, 'Successfully connected to the database')
            else:
                print("An error occurred.")
            bike=session.execute('use bike').one() # connecting to bike database

            day=session.execute('select * from day').all() # fetching all the data from the day table
            day=pd.DataFrame(day) # converting list to dataframe
            day.to_csv(Config.ORIGINAL_DATASET_FILE_PATH.joinpath('day.csv'), index=False)
            self.logger_object.log(self.file_object, 'Stored day data to day.csv')

            hour=session.execute('select * from hour').all() # fetching all the data from the hour table
            hour=pd.DataFrame(hour) # converting list to dataframe
            hour.to_csv(Config.ORIGINAL_DATASET_FILE_PATH.joinpath('hour.csv'), index=False)
            self.logger_object.log(self.file_object, 'Stored hour data to hour.csv')

            self.logger_object.log(self.file_object, f'Exited the function: {self.funcname} of the class: {self.classname}')

        except Exception as e:
            self.logger_object.log(
                self.file_object,
                f"Exception occured in {self.funcname} method of {self.classname} class. Exception message: {e}",
            )
            raise Exception()

