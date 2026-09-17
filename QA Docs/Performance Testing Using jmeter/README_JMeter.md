# AgriBot Performance Testing (Apache JMeter)

Load testing for **AgriBot** ([agribot.sbs](https://agribot.sbs)), a live smart
agriculture platform, using **Apache JMeter**.

## What's in this folder

|File|Description|
|-|-|
|`agribot\_load\_test.jmx`|The JMeter test plan used to run these tests. Open it directly in the JMeter GUI to inspect or re-run.|
|`AgriBot\_Performance\_Testing\_Report.docx`|Full write-up: test plan, results, charts, analysis, and recommendations.|

## What Was Tested

Three real pages on the live site were load-tested:

* **Homepage** (`/`)
* **About page** (`/about`)
* **Login page** (`/login`)

Two load levels were run:

|Test|Concurrent Users|Ramp-up|Loop Count|
|-|-|-|-|
|Baseline|5|10s|5|
|Load Test|50|10s|2|

## Key Results

|Page|Load|Avg Response Time|Max Response Time|Error Rate|
|-|-|-|-|-|
|Homepage|5 users|453ms|1,733ms|0.00%|
|Homepage|50 users|421ms|919ms|0.00%|
|About page|50 users|254ms|1,079ms|0.00%|
|Login page|50 users|188ms|869ms|0.00%|

**0% error rate across every test** — AgriBot handled both load levels without a single failed request.

The Homepage was consistently the slowest and most variable page, largely due to its autoplaying background video and reliance on external CDN resources (Tailwind CSS, Font Awesome, Google Fonts, AOS). The Login and About pages were fast and consistent by comparison.

Full analysis, charts, bottleneck discussion, and improvement recommendations are in the accompanying report.

## How to Re-run This Test

1. Install [Apache JMeter](https://jmeter.apache.org/) (requires a JDK).
2. Open JMeter and load `agribot\_load\_test.jmx` via **File → Open**.
3. Click the green **Start** button to run the test plan.
4. View results in the **Summary Report** listener.

To point the test at a different environment, edit the **Server Name or IP** field in each HTTP Request sampler.

## Tooling

* **Load testing tool:** Apache JMeter
* **Target:** AgriBot, hosted on an AWS EC2 instance

## Note

Since AgriBot runs on a personal AWS EC2 instance rather than production-grade infrastructure, results may vary slightly between runs depending on instance load and network conditions at the time of testing.

