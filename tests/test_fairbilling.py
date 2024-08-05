import unittest
from fairbilling import process_data, is_valid_time_format, is_valid_user, validate_line
import os
class TestFairBilling(unittest.TestCase):

    def test_is_valid_time_format(self):
        # Valid time format
        self.assertTrue(is_valid_time_format("12:00:00"))
        # Invalid time format
        self.assertFalse(is_valid_time_format("25:00:00"))
        self.assertFalse(is_valid_time_format("12:60:00"))
        self.assertFalse(is_valid_time_format("notatime"))

    def test_is_valid_user(self):
        # Valid user names
        self.assertTrue(is_valid_user("user1"))
        self.assertTrue(is_valid_user("User123"))
        # Invalid user names
        self.assertFalse(is_valid_user("user@name"))
        self.assertFalse(is_valid_user("user name"))

    def test_validate_line(self):
        # Valid lines
        self.assertTrue(validate_line("12:00:00 user1 Start"))
        self.assertTrue(validate_line("12:30:00 user1 End"))
        # Invalid lines
        self.assertFalse(validate_line("12:00 user1 Start"))  # Incorrect time format
        self.assertFalse(validate_line("12:00:00 user@name Start"))  # Invalid user
        self.assertFalse(validate_line("12:00:00 user1 InvalidAction"))  # Invalid action
        self.assertFalse(validate_line("Incomplete line"))  # Incomplete line

    def test_process_data(self):
        # Test processing of data with simple session records
        file_content = [
            "09:00:00 user1 Start\n",
            "09:01:00 user1 End\n",
            "09:30:00 user2 Start\n",
            "09:30:30 user2 End\n"
        ]

        with open('test_file.txt', 'w') as f:
            f.writelines(file_content)

        result, session_counts = process_data('test_file.txt')

        # Expected results
        self.assertEqual(result['user1'], 60)  # 1 minute
        self.assertEqual(session_counts['user1'], 1)
        self.assertEqual(result['user2'], 30)  # 30 seconds
        self.assertEqual(session_counts['user2'], 1)

    def test_unmatched_end_action(self):
        # Test handling of 'End' action without a preceding 'Start'
        file_content = [
            "10:00:00 user1 End\n",
            "10:01:00 user1 Start\n",
            "10:01:45 user1 End\n"
        ]

        with open('test_file.txt', 'w') as f:
            f.writelines(file_content)
       
        result, session_counts = process_data('test_file.txt')
        # Expected results: The unmatched 'End' at 09:00:00 should count from the first time in the file which is the same line itself(0 seconds)
        self.assertEqual(result['user1'], 45)  # 1 hours total (0 second + 45 seconds)
        self.assertEqual(session_counts['user1'], 2)

    def test_no_valid_data(self):
        # Test file with no valid data
        file_content = [
            "Invalid line 1\n",
            "Another invalid line\n"
        ]

        with open('test_file.txt', 'w') as f:
            f.writelines(file_content)

        result, session_counts = process_data('test_file.txt')

        # Expected results: No valid data should result in empty result and session_counts
        self.assertEqual(result, {})
        self.assertEqual(session_counts, {})
    
    def test_concurrent_sessions(self):
        # call the porcess_data method with the file stored in the testfiels directory
        result, session_counts =process_data('tests/testfiles/input1.txt')
        self.assertEqual(result['ALICE99'], 240)
        self.assertEqual(result['CHARLIE'], 37)
        self.assertEqual(session_counts['ALICE99'], 4)
        self.assertEqual(session_counts['CHARLIE'], 3)
        
    
    def tearDown(self):
        # Remove the test file if it exists
        if os.path.exists('test_file.txt'):
            os.remove('test_file.txt')

if __name__ == '__main__':
    unittest.main()
