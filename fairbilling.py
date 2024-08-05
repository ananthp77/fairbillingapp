import sys
import logging
from datetime import datetime

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def populate_result(user, result, duration):
    """Result dictionary contains the total duration for a user. This method updates the total duration"""
    if user in result:
        result[user] += duration
    else:
        result[user] = duration

def populate_session_count(user, session_counts):
    """session_counts dictionary contains the total number of sessions for a user. This method updates the total number of sessions"""
    if user in session_counts:
        session_counts[user] += 1
    else:
        session_counts[user] = 1

def is_valid_time_format(time_str):
    """Checks if a time string is in HH:MM:SS format."""
    try:
        datetime.strptime(time_str, '%H:%M:%S')
        return True
    except ValueError:
        return False

def is_valid_user(user_str):
    """Checks if the user string is alphanumeric."""
    return user_str.isalnum()

def validate_line(line):
    """Validates if a line from the input file has the correct format."""
    parts = line.strip().split()
    # check if number of columns in each row
    if len(parts) != 3:
        return False
    time_str, user, action = parts
    # check if every field follows the specified format
    if not is_valid_time_format(time_str) or not is_valid_user(user):
        return False
    if action not in {'Start', 'End'}:
        return False
    return True

def process_data(file_path):
    """Take individual session data from the input file."""
    try:
        with open(file_path, 'r') as file:
            data = file.readlines()
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return {}, {}

    sessions = {}  # Dictionary that stores start sessions for each user
    result = {}    # Dictionary that stores total duration for each user
    session_counts = {}  # Dictionary that stores session counts for each user

    # Filter and validate the input data line by line
    valid_data = [line.strip() for line in data if validate_line(line)]
    # If none of the records are following valid format, logging a warning
    if not valid_data:
        logging.warning("No valid data found in the file.")
        return result, session_counts
    
    # Idenifying the timestamp of first and last record in the log file. This is used to compare when there are any ends without a start or vice versa
    try:
        first_time = datetime.strptime(valid_data[0].split()[0], "%H:%M:%S")
        last_time = datetime.strptime(valid_data[-1].split()[0], "%H:%M:%S")
    except ValueError as e:
        logging.error(f"Error parsing initial or final times: {e}")
        return result, session_counts
    
    # Iterating the records one by one
    for line in valid_data:
        parts = line.strip().split()
        time_str, user, action = parts
        try:
            time = datetime.strptime(time_str, '%H:%M:%S')
        except ValueError as e:
            logging.error(f"Error parsing time: {e}")
            continue

        try:
            """All the start times are added to the sessionsmap.If the action is start and the user is not already added to the sessions map,
            add the starttime to the map. If the action is start and the user is  already added to the sessions map, append the new starttime 
            to the existing list of startimes."""
            # All the start times are added to the 
            if action == 'Start':
                if user not in sessions:
                    sessions[user] = [time]
                else:
                    sessions[user].append(time)
            elif action == 'End':
                """
                When the user action is end, then checking if there are any start sessions for the user. 
                If yes, then take the earliest start session from the list of start sessions.and update the dicionary 
                that holds the session duration and session counts with the information. If there is no startime for that user
                then considering the timestamp of first record as start time.
                """
                if user in sessions:
                    all_sessions_start = sessions[user]
                    if all_sessions_start:
                        # If there is session start, take the earliest session start
                        session_start = sessions[user].pop(0)
                        duration = time - session_start
                        duration = int(duration.total_seconds())
                        populate_result(user, result, duration)
                        populate_session_count(user, session_counts)
                    else:
                        # If no session start, assume the first time
                        duration = time - first_time
                        duration = int(duration.total_seconds())
                        populate_result(user, result, duration)
                        populate_session_count(user, session_counts)
                else:
                    """
                    This else condition handles the occurance of a user record without a start record, in this case also, the timestamp
                    of the first record is considered as start time.
                    """
                    duration = time - first_time
                    duration = int(duration.total_seconds())
                    populate_result(user, result, duration)
                    populate_session_count(user, session_counts)
        except Exception as e:
            logging.error(f"Error processing line '{line}': {e}")

    # Handle sessions that did not end with 'End' action
    """
    Since all the start records are pushed into the sessions dictionary, there can be some start records without an end record, for those
    users without an end record, the timestamp of the last record is considered as the end time.
    """
    for user, sessions in sessions.items():
        for session_start in sessions:
            try:
                duration = last_time - session_start
                duration = int(duration.total_seconds())
                populate_result(user, result, duration)
                populate_session_count(user, session_counts)
            except Exception as e:
                logging.error(f"Error calculating duration for user '{user}': {e}")

    return result, session_counts

def print_results(result, session_counts):
    """Prints the results in Expected format."""
    for user in result:
        total_sessions = session_counts.get(user, 0)
        total_duration = result[user]
        print(f"{user},{total_sessions},{total_duration}")

if __name__ == "__main__":
    """The execution starts here. checking the number of parameters is equal to 1. if yes it is calling the process_data
    method with the file path, and then prints the result"""
    if len(sys.argv) != 2:
        print("Usage: python session_processor.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    #calling the process method where the logic is executed
    result, session_counts = process_data(file_path)
    print_results(result, session_counts)
