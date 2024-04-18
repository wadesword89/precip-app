import os
import requests
import gzip

from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

def download_grib2_files(year_month, start_day, end_day, output_dir):
    base_url = "https://noaa-mrms-pds.s3.amazonaws.com/CONUS/RadarOnly_QPE_15M_00.00"

    def download_and_extract(url, gz_file_path):
        with requests.Session() as session:
            response = session.get(url, stream=True)
            if response.status_code == 200:
                with open(gz_file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                with gzip.open(gz_file_path, 'rb') as gz_file:
                    grib2_content = gz_file.read()
                    grib2_file_path = gz_file_path[:-3]
                    with open(grib2_file_path, 'wb') as grib2_file:
                        grib2_file.write(grib2_content)
                
                os.remove(gz_file_path)

    def process_date(current_date):
        current_date_str = current_date.strftime('%Y%m%d')
        date_output_dir = os.path.join(output_dir, current_date_str)
        os.makedirs(date_output_dir, exist_ok=True)
        
        start_time = datetime.strptime('000000', '%H%M%S')
        end_time = datetime.strptime('234500', '%H%M%S')
        current_time = start_time
        delta = timedelta(minutes=15)
        
        tasks = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            while current_time <= end_time:
                current_time_str = current_time.strftime('%H%M%S')
                file_name = f'MRMS_RadarOnly_QPE_15M_00.00_{current_date_str}-{current_time_str}.grib2.gz'
                url = f'{base_url}/{current_date_str}/{file_name}'
                gz_file_path = os.path.join(date_output_dir, file_name)
                
                if not os.path.exists(gz_file_path[:-3]):
                    task = executor.submit(download_and_extract, url, gz_file_path)
                    tasks.append(task)

                current_time += delta

            for task in tasks:
                task.result()

    start_date = datetime.strptime(year_month + start_day, '%Y%m%d')
    end_date = datetime.strptime(year_month + end_day, '%Y%m%d')

    current_date = start_date
    while current_date <= end_date:
        process_date(current_date)
        current_date += timedelta(days=1)
