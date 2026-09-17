# QA Documentation

This folder contains four deliverables from a Junior QA Analyst job simulation,
covering test planning, exploratory testing, regression testing, and bug
analysis. Together they show a progression from planning tests on a
hypothetical application to applying those same skills to a real, live
project (AgriBot).

## Contents

|File|Week|Summary|
|-|-|-|
|`ShopEase\_Test\_Plan\_and\_Test\_Cases.docx`|1|A full test plan (scope, strategy, risks, schedule) plus 20 detailed test cases for ShopEase, a hypothetical e-commerce web application.|
|`ShopEase\_Exploratory\_Testing\_Report.docx`|2|Exploratory ("ad-hoc") testing sessions on ShopEase, resulting in 5 documented bugs with reproduction steps, severity, and mock evidence.|
|`AgriBot\_Regression\_Testing\_Suite.docx`|5|A 15-case regression suite for AgriBot, a real live application, built on genuine engineering issues found while developing its automated tests and performance testing.|
|`Bug\_Tracking\_and\_Analysis\_Report.docx`|6|A cross-project bug tracking and trend analysis combining real bugs from both ShopEase and AgriBot with additional illustrative examples, plus recommendations and a reflective process-improvement section.|

## How These Connect

* **Week 1** establishes a structured test plan and case set for ShopEase before any testing begins.
* **Week 2** executes exploratory testing against that same plan, surfacing 5 real bugs (BUG-01 to BUG-05).
* **Week 5** shifts the same regression-testing discipline onto a real, live project (AgriBot), tracing test cases back to actual engineering issues found while building its automation (Week 3) and performance tests (Week 4).
* **Week 6** closes the loop: it analyzes bugs from *both* projects together, looking for patterns across them (e.g. a recurring "duplicate action on double-click" defect found independently in both ShopEase and a simulated example) and reflects on how earlier process changes could have caught these issues sooner.

## Related Work

* **Week 3** — Automated Selenium test scripts for AgriBot (login, registration, navigation, access control).
* **Week 4** — Apache JMeter performance testing for AgriBot, including the `.jmx` test plan and full results report.

