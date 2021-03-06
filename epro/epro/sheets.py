#!/usr/bin/env python2

from __future__ import print_function
import httplib2
import os
import csv

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

class Sheets():


    def __init__(self, spreadsheetId, client_secret_file, application_name):
        self.flags = None


        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        self.CLIENT_SECRET_FILE = client_secret_file
        self.APPLICATION_NAME = application_name

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        self.spreadsheetId = spreadsheetId

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_last_id(self, row_no = False):
        rangeName = 'A1:A'
        result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheetId, range=rangeName,
                majorDimension='COLUMNS').execute()
        values = result.get('values',[])
        
        last_id = values[0][-1]

        if row_no:
            return len(values[0])
        else:
            return last_id
    
    def append_row(self, row):
        if not type(row) is list:
            raise Exception('row is not a list')

        row_count = self.get_last_id(row_no=True) + 1

        new_row = row[0:10]
        new_row.append('=left(G{},7)'.format(row_count)) #K
        new_row.append('') #L
        new_row.append('=I{}'.format(row_count)) #M
        new_row.append('=J{}'.format(row_count)) #N
        new_row.append('=if(J{}<50000,1000,0)'.format(row_count)) #O
        new_row.append('=N{0}-O{0}'.format(row_count)) #P

        rangeName = 'A{0}:P{0}'.format(row_count)

        body = {
            'range' : rangeName,
            'values' : [new_row],
            'majorDimension' : 'ROWS'
        }
        
        result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheetId, range=rangeName,
                valueInputOption='USER_ENTERED', body=body).execute()
        return result

    def sort_sheet(self):
        body = {
            'requests': [
                {
                    'sortRange': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': 1,
                            'startColumnIndex': 0
                        },
                        'sortSpecs': [
                            {
                                'dimensionIndex': 0,
                                'sortOrder': 'ASCENDING'
                            }
                        ]
                    }
                }
            ]
        }
        
        result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheetId, body=body).execute()
        
        return result
#
if __name__=='__main__':
    sheet = Sheets('1mKAsY92nA3I6PhTkNd9aLIY8_SZMXERr2wg5WTYMk34', 'client_secret.json',
            'FinancialData')

    print(sheet.sort_sheet())
