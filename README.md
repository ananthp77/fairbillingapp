# Session Processor

## Overview

The `fairbilling.py` script processes session data from a text file to calculate the minimum total duration and count of sessions for each user. The input file contains lines with a timestamp, a username, and an action (either "Start" or "End"). The script validates the input, calculates session durations, and outputs the total duration and session count for each user.

## Features

- **Input Validation**: Ensures that each line of the input file is correctly formatted.
- **Session Duration Calculation**: Computes the total session duration for each user.
- **Session Count**: Counts the number of sessions each user participated in.
- **Error Handling**: Handles errors in file reading and data processing gracefully.

## Usage

1. **Prepare Input File**: Create a text file where each line contains a timestamp, a username, and an action ("Start" or "End"). The format should be:
```
14:02:03 ALICE99 Start 
14:02:05 CHARLIE End 
14:02:34 ALICE99 End 
14:02:58 ALICE99 Start 
14:03:02 CHARLIE Start 
14:03:33 ALICE99 Start 
14:03:35 ALICE99 End 
14:03:37 CHARLIE End 
14:04:05 ALICE99 End 
14:04:23 ALICE99 End 
14:04:41 CHARLIE Start
```
# Clone the Github repositiry
2. git clone https://github.com/ananthp77/fairbillingapp.git
# Get into the project after cloning
3. cd fairbillingapp
# Build the docker image of the fairbillingapp 
4. docker build -t fairbilling .
# Run the docker image for finding out the result 
5. docker run -v "File Path in your system":/data/filename fairbilling python fairbilling.py /data/filename 
# Example: docker run -v "E:\Ananth\fairbilling\input.csv":/data/input.csv fairbilling python fairbilling.py /data/input.csv
# For executing unit tests, use the command below
6. docker run --rm fairbilling pytest tests/
