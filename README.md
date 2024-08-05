# Session Processor

## Overview

The `fairbilling.py` script processes session data from a text file to calculate the minimum total duration and count of sessions for each user. The input file contains lines with a timestamp, a username, and an action (either "Start" or "End"). The script validates the input, calculates session durations, and outputs the total duration and session count for each user.

## Features

- **Input Validation**: Ensures that each line of the input file is correctly formatted.
- **Session Duration Calculation**: Computes the total session duration for each user.
- **Session Count**: Counts the number of sessions each user participated in.
- **Error Handling**: Handles errors in file reading and data processing gracefully.

## Requirements

- Python 3.6 or higher

## Usage

1. **Prepare Input File**: Create a text file where each line contains a timestamp, a username, and an action ("Start" or "End"). The format should be:
1. git clone
2. cd directory
3. docker build -t fairbilling .
4. docker run -v <"File Path in your system">:/data/<filename> fairbilling python fairbilling.py /data/<filename> 
5. Example: docker run -v "E:\Ananth\fairbilling\input.csv":/data/input.csv fairbilling python fairbilling.py /data/input.csv
5. docker run fairbilling pytest tests/
