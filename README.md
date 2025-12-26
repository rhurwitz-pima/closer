## Overview
`closer` is a Python command-line application that streamlines the process of grading eLumen Class Learning Outcomes (CLOs). From a D2L export file, `closer` creates a per-student CLO assessment file importable into eLumen. Importing the assessment file from `closer` into eLumen eliminates the need for instructors to perform the time-consuming and error-prone task of manually entering that data.

## Prerequisites
Before using `closer`, your D2L course shell **must be configured with calculated grade items that represent each Course Learning Outcome (CLO)**.

Specifically:

- Each CLO must have a corresponding *calculated grade item* in D2L
- These CLO grade items must aggregate scores from relevant assignments, quizzes, or discussions
- The CLO grade items, and only the CLO grade items, must be included when exporting grades from D2L

If your D2L gradebook is not configured this way, `closer` will not be able to recognize or process the exported grading file.

➡️ See: [Configuring D2L for CLO-based grading](docs/howto/d2l-clo-setup.md)

