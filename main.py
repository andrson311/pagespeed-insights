import urllib.request
import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()
PAGESPEED_KEY = os.getenv('PAGESPEED_API_KEY')

def get_data(url, strategy):
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={strategy}&locale=en&key={PAGESPEED_KEY}"

    response = urllib.request.urlopen(api_url)
    data = json.loads(response.read())

    return data

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Audit website with PageSpeed Insights API')
    parser.add_argument('-u', '--url', help='Provide the URL address of the page you want to audit.')
    parser.add_argument('-s', '--strategy', help='Choose between mobile or desktop.')
    args = parser.parse_args()

    data = get_data(args.url, args.strategy)

    # core web vitals
    vitals = {
        'FCP': data['lighthouseResult']['audits']['first-contentful-paint'],
        'LCP': data['lighthouseResult']['audits']['largest-contentful-paint'],
        'FID': data['lighthouseResult']['audits']['max-potential-fid'],
        'TBT': data['lighthouseResult']['audits']['total-blocking-time'],
        'CLS': data['lighthouseResult']['audits']['cumulative-layout-shift']
    }

    for v in vitals:
        print(f'{v} - time: {vitals[v]["numericValue"] / 1000} seconds, score: {vitals[v]["score"] * 100}%')

    # overall performance score
    overall_score = data['lighthouseResult']['categories']['performance']['score'] * 100
    print(f'Overall score: {overall_score}%')

    # long tasks report
    diagnostics = data['lighthouseResult']['audits']['diagnostics']['details']['items'][0]
    long_tasks_report = {
        'Total tasks': diagnostics['numTasks'],
        'Total tasks time': diagnostics['totalTaskTime'],
        'Long tasks': diagnostics['numTasksOver50ms']
    }

    for i in long_tasks_report:
        print(f'{i}: {long_tasks_report[i]}')

    # sometimes doesn't match the number of tasks over 50ms long
    long_tasks = data["lighthouseResult"]["audits"]["long-tasks"]["displayValue"]
    print(long_tasks)


