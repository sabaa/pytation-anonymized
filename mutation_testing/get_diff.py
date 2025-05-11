import subprocess
import re

DIFF_TYPE_ADDED = 'added'
DIFF_TYPE_DELETED = 'deleted'
DIFF_TYPE_MODIFIED = 'modified'
DIFF_TYPE_UNKNOWN = 'unknown'

def get_changed_lines(commit1, commit2):
    cmd = ['git', 'diff', '-U0', '--no-color', commit1, commit2]
    try:
        diff_output = subprocess.check_output(cmd, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in running git diff: {e}")
        return []
    
    filename = ''
    changes = []

    for line in diff_output.splitlines():
        if line.startswith('diff --git'):
            match = re.match(r'diff --git a\/.* b\/(.*)', line)
            if match:
                filename = match.group(1)
        elif line.startswith('@@'):

            match = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
            if match:
                old_start = int(match.group(1))
                old_count = int(match.group(2)) if match.group(2) else 1
                new_start = int(match.group(3))
                new_count = int(match.group(4)) if match.group(4) else 1

                change_dict = {
                    "filename": filename,
                    "lines": [],
                    "type": ""
                }

                if old_count > 0 and new_count == 0:
                    change_dict["type"] = DIFF_TYPE_DELETED
                    # Deletion
                    old_end = old_start + old_count - 1
                    if old_count == 1:
                        change_dict["lines"] = [old_start]
                    else:
                        change_dict["lines"] = list(range(old_start, old_end + 1))
                elif old_count == 0 and new_count > 0:
                    # Insertion
                    change_dict["type"] = DIFF_TYPE_ADDED
                    new_end = new_start + new_count - 1
                    if new_count == 1:
                        change_dict["lines"] = [new_start]
                    else:
                        change_dict["lines"] = list(range(new_start, new_end + 1))
                elif old_count > 0 and new_count > 0:
                    # Modification
                    change_dict["type"] = DIFF_TYPE_MODIFIED
                    new_end = new_start + new_count - 1
                    if old_count == new_count and old_start == new_start:
                        if old_count == 1:
                            change_dict["lines"] = [new_start]
                        else:
                            change_dict["lines"] = list(range(new_start, new_end + 1))
                    else:
                        change_dict["lines"] = list(range(new_start, new_end + 1))
                else:
                    change_dict["type"] = DIFF_TYPE_UNKNOWN
                    change_dict["lines"] = [line]
                changes.append(change_dict)
    return changes
