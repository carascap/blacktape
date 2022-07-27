![Logo](https://github.com/carascap/carascap.github.io/blob/main/images/carascap-100x100.png)

# blacktape

[![Build Status](https://github.com/carascap/blacktape/actions/workflows/test_suite.yml/badge.svg?branch=main)](https://github.com/carascap/blacktape/actions/workflows/test_suite.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/carascap/blacktape/branch/main/graph/badge.svg)](https://codecov.io/gh/carascap/blacktape)
[![Maintainability](https://api.codeclimate.com/v1/badges/4ccea04bc7bb591b6259/maintainability)](https://codeclimate.com/github/carascap/blacktape/maintainability)

Python library and supporting utilities to support text analysis, reporting, and redaction workflows.

## Interactive Environment

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/carascap/blacktape/main)

This repository includes a selection of interactive Jupyter notebooks and sample data to familiarize you with using blacktape in different workflows. The easiest way to try out these notebooks is by clicking on the MyBinder button above, launching a remotely hosted JupyterLab session in your browser.

Blacktape includes the following notebooks:

*end-to-end.ipynb*: Reads in a sample English language file, chunks it into 10,000 character blocks, sets up a SQLite3 database for output. Sets up a pipelined workflow in which each chunk is analyzed to identify named entities and a selection of regular expressions. Includes a selection of database queries and produces a sample redacted output file in which redaction targets are overwritten with a fixed-length block sequence.

*matching.ipynb*: Simple demonstration of NER and pattern matching for a given input.

*pii_patterns.ipynb*: Matching for common PII patterns against synthesized target data in a smple file.

*chunking_pipeline.ipynb*: Demonstration of large file chunking and job submission within a processing pipeline, illustrated by matching entities identified as PERSON or ORGANIZATION.

Several additional notebooks are provided that demonstrate subsets of the functionality illustrated in the above examples.

## License(s)

Logos, documentation, and other non-software products of the CARASCAP team are distributed under the terms of Creative Commons 4.0 Attribution. Software items in CARASCAP repositories are distributed under the terms of the MIT License. See the LICENSE file for additional details.

&copy; 2022, The University of North Carolina at Chapel Hill.

## Development Team and Support

Developed by the CARASCAP team at the University of North Carolina at Chapel Hill.

