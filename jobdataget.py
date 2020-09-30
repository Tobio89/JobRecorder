import openpyxl, datetime
from openpyxl.styles import NamedStyle
from os import path
from jobscraper import SaraminRole
import pyperclip


url = pyperclip.paste()
if url and url.startswith('http'):

    SHEET_LOCATION = path.join('C:\\','Users', 'User', 'Google Drive', 'jobs.xlsx')
    print(f'File path is {SHEET_LOCATION}')


    print('Gathering job data...')
    new_role = SaraminRole(url)
    print('Complete.')


    job_file = openpyxl.load_workbook(SHEET_LOCATION)
    job_sheet = job_file.active
    print('File opened, job sheet opened')

    current_job_count = job_sheet['A2'].value
    next_job_count = int(current_job_count) + 1

    print(next_job_count)

    cellAlias = {
        'Count': 'A2',
        'Date Applied': 'B2',
        'Where': 'C2',
        'Company': 'D2',
        'Job': 'E2',
        'Closing Date': 'F2',
    }



    job_sheet.insert_rows(2) # Insert a new row at the top, below titles 
    print('Inserted new top row')

    print('Writing new role to sheet...')

    date_style = NamedStyle(name='datetime', number_format='DD/MM')

    job_sheet[cellAlias['Count']] = next_job_count
    job_sheet[cellAlias['Date Applied']] = new_role.submission_date
    job_sheet[cellAlias['Where']] = 'Saramin'
    job_sheet[cellAlias['Company']] = new_role.company
    job_sheet[cellAlias['Job']] = new_role.description
    job_sheet[cellAlias['Closing Date']] = new_role.closing_date

    job_sheet[cellAlias['Date Applied']].style = date_style
    job_sheet[cellAlias['Closing Date']].style = date_style

    print('Completed.')

    print('Saving...')


    job_file.save(SHEET_LOCATION)

    print('Completed.')
else:
    print('The URL was faulty.')




