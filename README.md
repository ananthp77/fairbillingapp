# Session Processor

## Overview

The `fairbilling.py` script processes session data from a log file to calculate the minimum total duration of sessions in seconds and number of sessions for each user. The input log file contains usage data that consists of a timestamp (in HH:MM:SS format), a username (single alphanumeric string of arbitary length), and an action (either "Start" or "End"). If there is a record with "End" status that has no possible matching "Start",the start time should be assumed to be the earliest time of any record in the file and if e there is a “Start” with no possible matching “End”, the end timeshould be assumed to be the latest time of any record in the file. Any log records/lines that do not contain a valid time stamp, username and a Strt/End marker shudl be ignored. The script validates the input in logfile, calculates session durations, and output the minimum total duration and session count for each user.

## Assumptions
The data in the input log file will be correctly ordered chronologically and that all records in the file will be from within a single day (i.e. they will not span midnight).

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
## 2. Clone the Github repositiry
   git clone https://github.com/ananthp77/fairbillingapp.git

## 3. Get into the project after cloning
      cd fairbillingapp

## 4. Build the docker image of the fairbillingapp 
     docker build -t fairbilling .

## 5. Run the docker image for finding out the result 
      docker run -v <File Path in your system>:/data/<filename> fairbilling python fairbilling.py /data/<filename> 
      **Example: docker run -v "E:\Ananth\fairbilling\input.csv":/data/input.csv fairbilling python fairbilling.py /data/input.csv**

## 6. For executing unit tests, use the command below
      docker run --rm fairbilling pytest tests/

## To run locally without docker
     python fairbilling.py <inputFilePath>
    
