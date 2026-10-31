import json
import os
import requests

report_path = 'report.json'
receiver_url = os.getenv('RECEIVER_URL')

if not receiver_url:
    print("RECEIVER_URL secret not set. Skipping report transmission.")
    exit(0)

if os.path.exists(report_path):
    with open(report_path) as f:
        data = json.load(f)
    
    payload = {
        'repository': os.getenv('GITHUB_REPOSITORY'),
        'branch': os.getenv('GITHUB_REF_NAME'),
        'commit_sha': os.getenv('GITHUB_SHA'),
        'run_id': os.getenv('GITHUB_RUN_ID'),
        'timestamp': data.get('created'),
        'summary': {
            'total': data.get('summary', {}).get('total', 0),
            'passed': data.get('summary', {}).get('passed', 0),
            'failed': data.get('summary', {}).get('failed', 0),
            'status': 'SUCCESS' if data.get('exitcode') == 0 else 'FAILURE'
        },
        'tests': [{'name': t.get('nodeid'), 'result': t.get('outcome'), 'message': t.get('longrepr', '')} for t in data.get('tests', [])]
    }
    
    try:
        res = requests.post(receiver_url, json=payload, timeout=10)
        print('Report sent successfully:', res.status_code)
    except Exception as e:
        print('Failed to send report:', e)
else:
    print('report.json not found!')
