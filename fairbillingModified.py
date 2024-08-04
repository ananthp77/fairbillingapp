import sys
from datetime import datetime

def populateResult(user, result, duration):
    if user in result:
        result[user] = result[user] + duration
    else:
        result[user] = duration

def populateSessionCount(user, sessionCounts):
    if user in sessionCounts:
        sessionCounts[user] = sessionCounts[user] + 1
    else:
        sessionCounts[user] = 1

def is_valid_time_format(time_str):
    try:
        datetime.strptime(time_str, '%H:%M:%S')
        return True
    except ValueError:
        return False

def is_valid_user(user_str):
    return user_str.isalnum()

def validate_line(line):
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
    try:
        with open(file_path, 'r') as file:
            data = file.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}, {}

    sessions = {}
    result = {}
    sessionCounts = {}

    valid_data = [line.strip() for line in data if validate_line(line)]
    
    if not valid_data:
        print("No valid data found in the file.")
        return result, sessionCounts

    try:
        first_time = datetime.strptime(valid_data[0].split()[0], "%H:%M:%S")
        last_time = datetime.strptime(valid_data[-1].split()[0], "%H:%M:%S")
    except ValueError as e:
        print(f"Error parsing initial or final times: {e}")
        return result, sessionCounts

    for line in valid_data:
        parts = line.strip().split()
        time_str, user, action = parts
        try:
            time = datetime.strptime(time_str, '%H:%M:%S')
        except ValueError as e:
            print(f"Error parsing time: {e}")
            continue

        try:
            if action == 'Start':
                if user not in sessions:
                    sessions[user] = [time]
                else:
                    sessions[user].append(time)
            elif action == 'End':
                if user in sessions:
                    all_sessions_start = sessions[user]
                    if all_sessions_start:
                        session_start = sessions[user].pop(0)
                        duration = time - session_start
                        duration = int(duration.total_seconds())
                        populateResult(user, result, duration)
                        populateSessionCount(user, sessionCounts)
                    else:
                        duration = time - first_time
                        duration = int(duration.total_seconds())
                        populateResult(user, result, duration)
                        populateSessionCount(user, sessionCounts)
                else:
                    duration = time - first_time
                    duration = int(duration.total_seconds())
                    populateResult(user, result, duration)
                    populateSessionCount(user, sessionCounts)
        except Exception as e:
            print(f"Error processing line '{line}': {e}")

    for user, sessions in sessions.items():
        for sessionStart in sessions:
            try:
                duration = last_time - sessionStart
                duration = int(duration.total_seconds())
                populateResult(user, result, duration)
                populateSessionCount(user, sessionCounts)
            except Exception as e:
                print(f"Error calculating duration for user '{user}': {e}")

    return result, sessionCounts

def print_results(result, sessionCounts):
    print("User,TotalSessions,MinimumTotalDuration")
    for user in result:
        total_sessions = sessionCounts.get(user, 0)
        total_duration = result[user]
        print(f"{user},{total_sessions},{total_duration}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python session_processor.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result, sessionCounts = process_data(file_path)
    print_results(result, sessionCounts)
