import sys
import logging
from datetime import datetime

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def populate_result(user, result, duration):
    """Updates the total duration for a user."""
    if user in result:
        result[user] += duration
    else:
        result[user] = duration

def populate_session_count(user, session_counts):
    """Updates the session count for a user."""
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
    if len(parts) != 3:
        return False
    time_str, user, action = parts
    if not is_valid_time_format(time_str) or not is_valid_user(user):
        return False
    if action not in {'Start', 'End'}:
        return False
    return True

def process_data(file_path):
    """Processes the session data from the input file."""
    try:
        with open(file_path, 'r') as file:
            data = file.readlines()
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return {}, {}

    sessions = {}  # Stores ongoing sessions for each user
    result = {}    # Stores total duration for each user
    session_counts = {}  # Stores session counts for each user

    # Filter and validate data
    valid_data = [line.strip() for line in data if validate_line(line)]
    
    if not valid_data:
        logging.warning("No valid data found in the file.")
        return result, session_counts

    try:
        first_time = datetime.strptime(valid_data[0].split()[0], "%H:%M:%S")
        last_time = datetime.strptime(valid_data[-1].split()[0], "%H:%M:%S")
    except ValueError as e:
        logging.error(f"Error parsing initial or final times: {e}")
        return result, session_counts

    for line in valid_data:
        parts = line.strip().split()
        time_str, user, action = parts
        try:
            time = datetime.strptime(time_str, '%H:%M:%S')
        except ValueError as e:
            logging.error(f"Error parsing time: {e}")
            continue

        try:
            if action == 'Start':
                # Start a new session for the user
                if user not in sessions:
                    sessions[user] = [time]
                else:
                    sessions[user].append(time)
            elif action == 'End':
                # End the current session for the user
                if user in sessions:
                    all_sessions_start = sessions[user]
                    if all_sessions_start:
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
                    # Handle case where 'End' is found without 'Start'
                    duration = time - first_time
                    duration = int(duration.total_seconds())
                    populate_result(user, result, duration)
                    populate_session_count(user, session_counts)
        except Exception as e:
            logging.error(f"Error processing line '{line}': {e}")

    # Handle sessions that did not end with 'End' action
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
    if len(sys.argv) != 2:
        print("Usage: python session_processor.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result, session_counts = process_data(file_path)
    print_results(result, session_counts)
