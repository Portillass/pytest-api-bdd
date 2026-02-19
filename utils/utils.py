# utils/utils.py
import datetime
import os
import webbrowser
import json

def append_result(results, test_name, status, message, payload=None, start_time=None, end_time=None):
    """Add a test result dictionary to the list, including duration"""
    if start_time is None:
        start_time = datetime.datetime.now()
    if end_time is None:
        end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()

    if isinstance(payload, (dict, list)):
        payload = json.dumps(payload, indent=2)

    results.append({
        "test_name": test_name,
        "status": status,
        "message": message,
        "payload": payload if payload is not None else "No Data",
        "duration": f"{duration:.2f} s"
    })


def generate_html_report(results, filename=None):
    """Generate HTML report with Test Name, Outcome, Duration, and Payload/Response"""
    os.makedirs("reports", exist_ok=True)

    if not filename:
        # Auto-increment filenames like report.html, report1.html, report2.html
        base = "reports/report"
        i = 0
        while True:
            filename = f"{base}{'' if i==0 else i}.html"
            if not os.path.exists(filename):
                break
            i += 1

    report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(results)
    passed = len([r for r in results if r["status"] == "PASSED"])
    failed = len([r for r in results if r["status"] == "FAILED"])

    html_content = f"""
    <html>
    <head>
        <title>Pytest BDD Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f0f2f5;
                margin: 30px;
            }}
            h1 {{
                color: #34495e;
                text-align: center;
            }}
            .summary {{
                margin: 20px auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                max-width: 500px;
                text-align: center;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                table-layout: fixed;
                background-color: #ffffff;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: center;
                word-wrap: break-word;
                font-size: 14px;
            }}
            th {{
                background-color: #2c3e50;
                color: white;
            }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            tr:hover {{ background-color: #f1f1f1; }}
            .PASSED {{ color: green; font-weight: bold; }}
            .FAILED {{ color: red; font-weight: bold; }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
                max-height: 200px;
                overflow: auto;
                margin: 0;
                font-size: 13px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <h1>Pytest BDD Automation Report</h1>

        <div class="summary">
            <p><strong>Report Generated:</strong> {report_time}</p>
            <p><strong>Total Tests:</strong> {total}</p>
            <p><strong>Passed:</strong> <span style="color:green;">{passed}</span></p>
            <p><strong>Failed:</strong> <span style="color:red;">{failed}</span></p>
        </div>

        <table>
            <tr>
                <th style="width:30%;">Test/Scenario Name</th>
                <th style="width:15%;">Outcome</th>
                <th style="width:15%;">Duration</th>
                <th style="width:40%;">Payload / Response</th>
            </tr>
    """

    for r in results:
        payload_display = f"{r['message']}\n{r['payload']}"
        html_content += f"""
            <tr>
                <td>{r['test_name']}</td>
                <td class="{r['status']}">{r['status']}</td>
                <td>{r['duration']}</td>
                <td><pre>{payload_display}</pre></td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Report generated: {filename}")
    webbrowser.open(f"file://{os.path.abspath(filename)}")
