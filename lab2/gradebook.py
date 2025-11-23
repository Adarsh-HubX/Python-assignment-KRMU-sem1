import csv
import statistics
from pathlib import Path


def print_welcome():
    print("\n" + "="*60)
    print("             WELCOME TO GRADEBOOK ANALYZER v1.0")
    print("="*60)
    print("\nThis tool helps you analyze student grades efficiently!")
    print("\nFeatures:")
    print("  • Calculate grade statistics (mean, median, min, max)")
    print("  • Assign letter grades automatically")
    print("  • Filter pass/fail students")
    print("  • Generate formatted grade reports\n")


def get_input_method():
    while True:
        print("\n" + "-"*60)
        print("How would you like to input student data?")
        print("1. Manual entry (type names and marks)")
        print("2. Load from CSV file")
        choice = input("\nEnter your choice (1 or 2): ").strip()

        if choice in ['1', '2']:
            return choice
        print("❌ Invalid choice. Please enter 1 or 2.\n")


def manual_data_entry():
    marks = {}
    print("\n--- MANUAL DATA ENTRY ---\n")

    while True:
        try:
            num_students = input("How many students are in the class? ").strip()
            if not num_students.isdigit():
                print("❌ Please enter a whole number.\n")
                continue
            num_students = int(num_students)
            if num_students <= 0:
                print("❌ Please enter a positive number.\n")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.\n")

    print()

    for i in range(num_students):
        while True:
            name = input(f"Student {i+1} - Enter name: ").strip()
            if not name:
                print("❌ Name cannot be empty.\n")
                continue

            try:
                mark = float(input(f"Enter marks for {name}: ").strip())
                if not (0 <= mark <= 100):
                    print("❌ Marks must be between 0 and 100.\n")
                    continue
                
                if name in marks:
                    print(f"⚠️ Warning: '{name}' already exists. Overwriting mark.")
                
                marks[name] = mark
                print(f"✓ Added {name}: {mark}\n")
                break
            except ValueError:
                print("❌ Please enter a valid number for marks.\n")

    return marks


def load_csv_data():
    print("\n--- CSV FILE IMPORT ---\n")
    NAME_KEYS = ['name', 'student', 'id']
    MARK_KEYS = ['mark', 'score', 'grade', 'points']

    while True:
        filepath = input("Enter CSV file path (e.g., students.csv): ").strip()

        file = Path(filepath)
        if not file.exists():
            print(f"❌ File '{filepath}' not found. Try again or check the path.\n")
            continue

        try:
            marks = {}
            with open(file, 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.reader(f)
                
                try:
                    header_row = next(reader)
                except StopIteration:
                    print("❌ CSV file is empty. Please check your file.\n")
                    continue

                fieldnames = [h.strip().lower() for h in header_row]

                name_col_index = -1
                mark_col_index = -1
                
                for i, h in enumerate(fieldnames):
                    if any(k in h for k in NAME_KEYS) and name_col_index == -1:
                        name_col_index = i
                    if any(k in h for k in MARK_KEYS) and mark_col_index == -1:
                        mark_col_index = i

                if name_col_index == -1 or mark_col_index == -1:
                    print("❌ Could not automatically detect 'Name' and 'Marks' columns.")
                    print(f"Detected headers: {', '.join(header_row)}")
                    print("Please ensure your file has columns containing 'name'/'student' and 'mark'/'score'/'grade'.\n")
                    continue

                for row in reader:
                    if not any(row):
                        continue
                        
                    try:
                        name = row[name_col_index].strip()
                        mark = float(row[mark_col_index].strip())
                        
                        if name and 0 <= mark <= 100:
                            marks[name] = mark
                    except (IndexError, ValueError):
                        continue

            if not marks:
                print("❌ No valid student records found in this CSV.\nMake sure the file has 'Name' and 'Marks' columns and valid data (0-100).\n")
                continue

            print(f"✓ Successfully loaded {len(marks)} valid students from '{filepath}'.\n")
            return marks

        except Exception as e:
            print(f"❌ Error reading file: {type(e).__name__}: {e}\n")


def calculate_average(marks_dict):
    if not marks_dict:
        return 0
    return sum(marks_dict.values()) / len(marks_dict)


def calculate_median(marks_dict):
    if not marks_dict:
        return 0
    return statistics.median(marks_dict.values())


def find_max_score(marks_dict):
    if not marks_dict:
        return 0.0, None
    max_student = max(marks_dict, key=marks_dict.get)
    return marks_dict[max_student], max_student


def find_min_score(marks_dict):
    if not marks_dict:
        return 0.0, None
    min_student = min(marks_dict, key=marks_dict.get)
    return marks_dict[min_student], min_student


def assign_grade(mark):
    if mark >= 90:
        return 'A'
    elif mark >= 80:
        return 'B'
    elif mark >= 70:
        return 'C'
    elif mark >= 60:
        return 'D'
    else:
        return 'F'


def create_grades_dict(marks_dict):
    return {name: assign_grade(mark) for name, mark in marks_dict.items()}


def get_grade_distribution(grades_dict):
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for grade in grades_dict.values():
        if grade in distribution:
            distribution[grade] += 1
    return distribution


def get_pass_fail_students(marks_dict, passing_threshold=40):
    passed = [name for name, mark in marks_dict.items() if mark >= passing_threshold]
    failed = [name for name, mark in marks_dict.items() if mark < passing_threshold]
    return passed, failed, passing_threshold


def display_statistics(marks_dict):
    if not marks_dict:
        return 
        
    avg = calculate_average(marks_dict)
    median = calculate_median(marks_dict)
    max_score, max_student = find_max_score(marks_dict)
    min_score, min_student = find_min_score(marks_dict)

    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS")
    print("="*60)
    print(f"Total Students: {len(marks_dict)}")
    print(f"Average Score: {avg:^28.2f}")
    print(f"Median Score: {median:^29.2f}")
    print(f"Highest Score: {max_score:^28.2f} (Student: {max_student})")
    print(f"Lowest Score: {min_score:^29.2f} (Student: {min_student})")


def display_grade_distribution(grades_dict):
    if not grades_dict:
        return

    distribution = get_grade_distribution(grades_dict)
    total_students = len(grades_dict)

    print("\n" + "="*60)
    print("GRADE DISTRIBUTION")
    print("="*60)
    print(f"{'Grade':<10} {'Count':<10} {'Percentage':>10}")
    print("-" * 30)

    for grade in ['A', 'B', 'C', 'D', 'F']:
        count = distribution.get(grade, 0)
        percentage = (count / total_students * 100) if total_students > 0 else 0
        print(f"{grade:<10} {count:<10} {percentage:>10.1f}%")


def display_pass_fail_summary(marks_dict):
    if not marks_dict:
        return

    passed, failed, threshold = get_pass_fail_students(marks_dict)

    print("\n" + "="*60)
    print("PASS/FAIL SUMMARY")
    print("="*60)
    
    print(f"Passed (≥{threshold}): {len(passed)} students")
    if passed:
        preview_names = passed[:5]
        suffix = '...' if len(passed) > 5 else ''
        print(f"  → {', '.join(preview_names)}{suffix}")

    print(f"Failed (<{threshold}): {len(failed)} students")
    if failed:
        preview_names = failed[:5]
        suffix = '...' if len(failed) > 5 else ''
        print(f"  → {', '.join(preview_names)}{suffix}")


def display_results_table(marks_dict, grades_dict):
    if not marks_dict:
        return

    print("\n" + "="*60)
    print("RESULTS TABLE")
    print("="*60)
    print(f"{'Name':<20} {'Marks':>10} {'Grade':>8}")
    print("-" * 38) 

    for name in sorted(marks_dict.keys()):
        mark = marks_dict[name]
        grade = grades_dict.get(name, 'N/A')
        print(f"{name:<20} {mark:>10.2f} {grade:>8}")

    print("=" * 60)


def export_to_csv(marks_dict, grades_dict):
    if not marks_dict:
        print("❌ Cannot export: No student data available.\n")
        return

    while True:
        filename = input("\nEnter the filename for SIMPLE CSV export (e.g., data_export.csv): ").strip()
        if not filename:
            print("❌ Filename cannot be empty.\n")
            continue
        if not filename.lower().endswith('.csv'):
            filename += '.csv'

        file_path = Path(filename)
        if file_path.exists():
            overwrite = input(f"File '{filename}' already exists. Overwrite? (yes/no): ").strip().lower()
            if overwrite not in ['yes', 'y']:
                print("❌ Export cancelled.\n")
                return
        break

    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow(['Student Name', 'Marks', 'Grade'])

            for name in sorted(marks_dict.keys()):
                writer.writerow([name, marks_dict[name], grades_dict[name]])

        print(f"✓ Simple data file successfully exported to '{filename}'\n")
    except Exception as e:
        print(f"❌ Error exporting to CSV: {type(e).__name__}: {e}\n")


def get_next_action(exported):
    print("\n" + "="*60)
    print("WHAT WOULD YOU LIKE TO DO NEXT?")
    print("="*60)
    
    if exported:
        print("1. Analyze another set of grades (Manual/CSV)")
        print("2. Exit program")
    else: 
        print("1. Analyze another set of grades (Manual/CSV)")
        print("2. Exit program")

    while True:
        choice = input("\nEnter your choice (1 or 2): ").strip()
        if choice == '1':
            return 'analyze_new'
        elif choice == '2':
            return 'exit'
        else:
            print("❌ Invalid choice. Please enter 1 or 2.\n")


def analyze_gradebook(marks_dict):
    if not marks_dict:
        print("❌ No student data available for analysis.")
        return 'analyze_new' 

    grades_dict = create_grades_dict(marks_dict)
    
    display_statistics(marks_dict)
    display_grade_distribution(grades_dict)
    display_pass_fail_summary(marks_dict)
    display_results_table(marks_dict, grades_dict)
    
    exported = False
    export_choice = input("\nWould you like to export **just the student data** to a simple CSV (for later loading)? (yes/no): ").strip().lower()
    if export_choice in ['yes', 'y']:
        export_to_csv(marks_dict, grades_dict)
        exported = True
        
    return get_next_action(exported) 


def main_menu_loop():
    print_welcome()
    
    marks = {} 

    while True:
        method = get_input_method()
        
        if method == '1':
            marks = manual_data_entry()
        elif method == '2':
            marks = load_csv_data()
        
        if not marks:
            continue

        action = analyze_gradebook(marks)

        if action == 'exit':
            print("\n" + "="*60)
            print("Thank you for using GradeBook Analyzer!")
            print("="*60 + "\n")
            break
        elif action == 'analyze_new':
            continue

if __name__ == "__main__":
    main_menu_loop()
