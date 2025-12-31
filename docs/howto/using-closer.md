# Using `closer` to Convert D2L CLO Exports

This guide explains how to use the `closer` command-line tool to convert a D2L CLO grading export into a CSV file that can be imported into eLumen.

Before proceeding, ensure that:
- You have exported a CSV file containing only CLO calculated grade items as described in the [Configuring D2L for CLO Based Grading](./d2l-clo-setup.md) how-to document.

## Basic Usage

The `closer` command takes two positional arguments:
- The input CSV file exported from D2L
- The output CSV file to be created for import into eLumen

```bash
closer input.csv output.csv
```

D2L treats grades as percentages while eLumen assesses CLOs as pass/fail. By default, ```closer``` converts D2L grades of 70% and above as passing and below that as failing for eLumen conversion purposes. [See Command-Line Options](#command-line-options) for information on how to customize the threshold setting

If the command completes successfully, `output.csv` will be created and ready for import into eLumen.

## Command-Line Options

You can view all available options by running:

```bash
closer -h
```

```
usage: closer [-h] [-t THRESHOLD] [-v] [--version] input_fname output_fname

Converts D2L grade data to eLumen CLO format.

positional arguments:
  input_fname           Path to source D2L CSV.
  output_fname          Path to destination CSV.

options:
  -h, --help            show this help message and exit
  -t, --threshold THRESHOLD
                        Passing percent (70 by default).
  -v, --verbose         Increase output verbosity.
  --version             show program's version number and exit
```

## Threshold Option

By default, `closer` evaluates CLO performance using its built-in passing threshold of 70%.

To specify a custom passing percentage, use the `--threshold` (or `-t`) option:

```bash
closer --threshold 70 d2l_clo_export.csv elumen_import.csv
```

This example treats scores of 70% or higher as passing for CLO assessment.

## Threshold and eLumen Scoring Model

`closer` is designed to support a **bi-modal CLO assessment model** in eLumen.

In this model:
- Students either **meet expectations** or **do not meet expectations**
- CLO scores imported into eLumen are binary:
  - `1` = Meets expectations
  - `0` = Does not meet expectations

The `--threshold` value determines how numeric CLO grades from D2L are converted into this binary outcome.

- If a student’s CLO percentage is **greater than or equal to the threshold**, `closer` records a value of `1`
- If the percentage is **below the threshold**, `closer` records a value of `0`

For example:

```text
Threshold: 70%

CLO score ≥ 70% → Meets expectations (1)
CLO score < 70% → Does not meet expectations (0)
```

## Verbose Output

To see additional diagnostic information during processing, use the `--verbose` flag:

```bash
closer --verbose d2l_clo_export.csv elumen_import.csv
```

Verbose mode is useful when validating a new workflow or diagnosing input file problems.

## Processing Logic

During execution, `closer` applies the following rules:

- Only rows matching the expected student record pattern are processed
- Header and metadata rows are ignored automatically
- Malformed student rows cause execution to stop with an error
- Scores with a denominator of 0 are treated as 0% and fail the threshold

## Expected Result

After running `closer` successfully:

- A new CSV file is created at the specified output path
- Each row represents a student
- Each CLO is represented in the format expected by eLumen
- The file can be imported directly into eLumen without manual editing

## Common Errors

- Unexpected columns or extra fields: Ensure that only CLO grade items were selected during the D2L export.
- Malformed rows: Verify that the D2L export completed successfully and was not manually edited.
- All students failing a CLO unexpectedly: Check denominator values and confirm the threshold used.
