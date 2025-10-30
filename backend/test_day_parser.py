"""
Test file to demonstrate the DayParser functionality

This shows how the backend now handles day-of-operation filtering
"""

import sys
sys.path.append('/Users/binossama/Desktop/soen342-project/backend')

from models.DayParser import DayParser

print("=" * 60)
print("DAY PARSER - TEST EXAMPLES")
print("=" * 60)

# Test 1: Parse comma-separated format
print("\n1. COMMA-SEPARATED FORMAT:")
print("-" * 40)
test1 = "Mon,Wed,Fri"
result1 = DayParser.parse_days(test1)
print(f"Input: '{test1}'")
print(f"Output: {result1}")

# Test 2: Parse dash/range format
print("\n2. DASH/RANGE FORMAT:")
print("-" * 40)
test2 = "Fri-Sun"
result2 = DayParser.parse_days(test2)
print(f"Input: '{test2}'")
print(f"Output: {result2}")

# Test 3: Parse "Daily"
print("\n3. DAILY FORMAT:")
print("-" * 40)
test3 = "Daily"
result3 = DayParser.parse_days(test3)
print(f"Input: '{test3}'")
print(f"Output: {result3}")

# Test 4: User checkbox matching
print("\n4. USER CHECKBOX MATCHING:")
print("-" * 40)
user_selected = ['Monday', 'Friday']
connection_days = "Mon,Wed,Fri"
match = DayParser.days_match(user_selected, connection_days)
print(f"User selected: {user_selected}")
print(f"Connection operates: '{connection_days}' -> {DayParser.parse_days(connection_days)}")
print(f"Match: {match} ✓")

# Test 5: User checkbox NOT matching
print("\n5. USER CHECKBOX NO MATCH:")
print("-" * 40)
user_selected2 = ['Tuesday', 'Thursday']
connection_days2 = "Mon,Wed,Fri"
match2 = DayParser.days_match(user_selected2, connection_days2)
print(f"User selected: {user_selected2}")
print(f"Connection operates: '{connection_days2}' -> {DayParser.parse_days(connection_days2)}")
print(f"Match: {match2} ✗")

# Test 6: User checkbox matching range
print("\n6. USER CHECKBOX WITH RANGE:")
print("-" * 40)
user_selected3 = ['Saturday']
connection_days3 = "Fri-Sun"
match3 = DayParser.days_match(user_selected3, connection_days3)
print(f"User selected: {user_selected3}")
print(f"Connection operates: '{connection_days3}' -> {DayParser.parse_days(connection_days3)}")
print(f"Match: {match3} ✓")

# Test 7: Real CSV examples
print("\n7. REAL CSV EXAMPLES:")
print("-" * 40)
csv_examples = [
    "Fri-Sun",
    "Daily", 
    "Mon,Wed,Fri"
]
for example in csv_examples:
    parsed = DayParser.parse_days(example)
    print(f"'{example}' -> {parsed}")

print("\n" + "=" * 60)
print("INTEGRATION EXAMPLE - FRONTEND TO BACKEND")
print("=" * 60)
print("\nFrontend sends:")
print('{ "operationDays": ["Monday", "Friday"] }')
print("\nBackend receives array and compares to connections:")
print("  Connection 1: 'Mon,Wed,Fri' -> MATCH ✓ (Friday is in list)")
print("  Connection 2: 'Fri-Sun' -> MATCH ✓ (Friday is in range)")
print("  Connection 3: 'Tue,Thu' -> NO MATCH ✗")
print("  Connection 4: 'Daily' -> MATCH ✓ (all days match)")
print("\n" + "=" * 60)
