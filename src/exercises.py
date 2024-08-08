easy_exercises = [
    {"question": "List the contents of the current directory.", "answer": "ls"},
    {"question": "Change to the home directory.", "answer": "cd ~"},
    {"question": "Create a directory named 'test'.", "answer": "mkdir test"},
    {"question": "Remove a file named 'file.txt'.", "answer": "rm file.txt"},
    {"question": "Copy 'file1.txt' to 'file2.txt'.", "answer": "cp file1.txt file2.txt"}
]

medium_exercises = [
    {"question": "Search for the word 'error' in 'logfile.txt'.", "answer": "grep error logfile.txt"},
    {"question": "Find all '.txt' files in the '/home' directory.", "answer": "find /home -name '*.txt'"},
    {"question": "Create a tar archive named 'archive.tar' containing 'file1' and 'file2'.", "answer": "tar -cvf archive.tar file1 file2"},
    {"question": "Change the permissions of 'script.sh' to be executable by everyone.", "answer": "chmod +x script.sh"},
    {"question": "List all running processes.", "answer": "ps aux"}
]

hard_exercises = [
    {"question": "Print the first column of the file 'data.txt'.", "answer": "awk '{print $1}' data.txt"},
    {"question": "Replace 'foo' with 'bar' in 'file.txt'.", "answer": "sed 's/foo/bar/g' file.txt"},
    {"question": "Allow incoming traffic on port 22 (SSH).", "answer": "iptables -A INPUT -p tcp --dport 22 -j ACCEPT"},
    {"question": "Schedule a script 'backup.sh' to run daily at 2 AM.", "answer": "echo '0 2 * * * /path/to/backup.sh' | crontab -"},
    {"question": "Connect to a remote server at 'example.com' as user 'admin'.", "answer": "ssh admin@example.com"}
]