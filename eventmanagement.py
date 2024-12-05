import csv
import os
from datetime import datetime

EVENT_FILE = 'events.csv'
ATTENDEE_FILE = 'attendees.csv'
USER_FILE = 'users.csv'

def authenticate():
    print("Welcome to the Event Management System")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Check if user exists in the user file
    try:
        with open(USER_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    print("Authentication successful!")
                    return True
            print("Authentication failed! Please register or check your credentials.")
            return False
    except FileNotFoundError:
        print("No users found. Please register a new user.")
        return False

def register_user():
    username = input("Enter new username: ")
    password = input("Enter new password: ")

    with open(USER_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    print(f"User '{username}' registered successfully!")

def add_event():
    event_id = input("Enter Event ID: ")
    name = input("Enter Event Name: ")
    date = input("Enter Event Date (YYYY-MM-DD): ")
    location = input("Enter Event Location: ")
    description = input("Enter Event Description: ")
    category = input("Enter Event Category: ")

    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    with open(EVENT_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([event_id, name, date, location, description, category])
    print(f"Event '{name}' added successfully.")

def view_events():
    try:
        with open(EVENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            print("\n{:<10} {:<30} {:<15} {:<30} {:<50} {:<20}".format('ID', 'Name', 'Date', 'Location', 'Description', 'Category'))
            print("=" * 150)
            for row in reader:
                print("{:<10} {:<30} {:<15} {:<30} {:<50} {:<20}".format(row[0], row[1], row[2], row[3], row[4], row[5]))
            print("=" * 150)
    except FileNotFoundError:
        print("Events file not found.")

def update_event():
    event_id = input("Enter Event ID to update: ")
    updated = False
    events = []

    try:
        with open(EVENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            events = list(reader)

        for row in events:
            if row[0] == event_id:
                row[1] = input(f"Enter new name (current: {row[1]}): ") or row[1]
                row[2] = input(f"Enter new date (current: {row[2]}): ") or row[2]
                row[3] = input(f"Enter new location (current: {row[3]}): ") or row[3]
                row[4] = input(f"Enter new description (current: {row[4]}): ") or row[4]
                row[5] = input(f"Enter new category (current: {row[5]}): ") or row[5]
                updated = True

        with open(EVENT_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(events)

        if updated:
            print("Event updated successfully.")
        else:
            print("Event ID not found.")
    except FileNotFoundError:
        print("Events file not found.")

def delete_event():
    event_id = input("Enter Event ID to delete: ")
    events = []

    try:
        with open(EVENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            events = list(reader)

        events = [row for row in events if row[0] != event_id]

        with open(EVENT_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(events)

        print("Event deleted successfully.")
    except FileNotFoundError:
        print("Events file not found.")

def add_attendee():
    attendee_id = input("Enter Attendee ID: ")
    event_id = input("Enter Event ID: ")
    name = input("Enter Attendee Name: ")
    email = input("Enter Attendee Email: ")

    with open(ATTENDEE_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([attendee_id, event_id, name, email])
    print(f"Attendee '{name}' added successfully.")

def view_attendees():
    try:
        with open(ATTENDEE_FILE, mode='r') as file:
            reader = csv.reader(file)
            print("\n{:<10} {:<10} {:<30} {:<30}".format('ID', 'Event ID', 'Name', 'Email'))
            print("=" * 80)
            for row in reader:
                print("{:<10} {:<10} {:<30} {:<30}".format(row[0], row[1], row[2], row[3]))
            print("=" * 80)
    except FileNotFoundError:
        print("Attendees file not found.")

def search_event():
    event_id = input("Enter Event ID to search: ")
    found = False

    try:
        with open(EVENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == event_id:
                    print("\nEvent Found:")
                    print(f"ID: {row[0]}, Name: {row[1]}, Date: {row[2]}, Location: {row[3]}, Description: {row[4]}, Category: {row[5]}")
                    found = True
                    break

        if not found:
            print("Event ID not found.")
    except FileNotFoundError:
        print("Events file not found.")

def search_attendees_by_event():
    event_id = input("Enter Event ID to search attendees: ")
    found = False

    try:
        with open(ATTENDEE_FILE, mode='r') as file:
            reader = csv.reader(file)
            print("\nAttendees for Event ID '{}':".format(event_id))
            print("\n{:<10} {:<30} {:<30}".format('ID', 'Name', 'Email'))
            print("=" * 80)
            for row in reader:
                if row[1] == event_id:
                    print("{:<10} {:<30} {:<30}".format(row[0], row[2], row[3]))
                    found = True

        if not found:
            print("No attendees found for Event ID '{}.'".format(event_id))
    except FileNotFoundError:
        print("Attendees file not found.")

def count_attendees_per_event():
    event_count = {}

    try:
        with open(ATTENDEE_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                event_id = row[1]
                if event_id in event_count:
                    event_count[event_id] += 1
                else:
                    event_count[event_id] = 1
        
        print("\nAttendee Count per Event:")
        for event_id, count in event_count.items():
            print(f"Event ID: {event_id}, Attendee Count: {count}")
    except FileNotFoundError:
        print("Attendees file not found.")

def export_events():
    output_file = input("Enter the filename to save events (e.g., events_report.csv): ")
    try:
        with open(EVENT_FILE, mode='r') as file:
            reader = csv.reader(file)
            with open(output_file, mode='w', newline='') as outfile:
                writer = csv.writer(outfile)
                for row in reader:
                    writer.writerow(row)
        print(f"Events exported successfully to '{output_file}'.")
    except FileNotFoundError:
        print("Events file not found.")

def import_attendees():
    input_file = input("Enter the filename to import attendees from (e.g., new_attendees.csv): ")
    try:
        with open(input_file, mode='r') as file:
            reader = csv.reader(file)
            with open(ATTENDEE_FILE, mode='a', newline='') as attendees_file:
                writer = csv.writer(attendees_file)
                for row in reader:
                    writer.writerow(row)
        print("Attendees imported successfully.")
    except FileNotFoundError:
        print("Input file not found.")

def main():
    while True:
        print("\n=====Event Management System=====")
        print("======Created By-Madhav and Raja =======")
        print("======Represented in Kanha Makhan Public School===")
        print("1. Register User")
        print("2. Login User")
        print("3. Add Event")
        print("4. View Events")
        print("5. Update Event")
        print("6. Delete Event")
        print("7. Add Attendee")
        print("8. View Attendees")
        print("9. Search Event")
        print("10. Search Attendees by Event ID")
        print("11. Count Attendees per Event")
        print("12. Export Events to CSV")
        print("13. Import Attendees from CSV")
        print("14. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            if authenticate():
                while True:
                    print("\nUser Menu")
                    print("1. Add Event")
                    print("2. View Events")
                    print("3. Update Event")
                    print("4. Delete Event")
                    print("5. Add Attendee")
                    print("6. View Attendees")
                    print("7. Search Event")
                    print("8. Search Attendees by Event ID")
                    print("9. Count Attendees per Event")
                    print("10. Export Events to CSV")
                    print("11. Import Attendees from CSV")
                    print("12. Logout")

                    user_choice = input("Choose an option: ")

                    if user_choice == '1':
                        add_event()
                    elif user_choice == '2':
                        view_events()
                    elif user_choice == '3':
                        update_event()
                    elif user_choice == '4':
                        delete_event()
                    elif user_choice == '5':
                        add_attendee()
                    elif user_choice == '6':
                        view_attendees()
                    elif user_choice == '7':
                        search_event()
                    elif user_choice == '8':
                        search_attendees_by_event()
                    elif user_choice == '9':
                        count_attendees_per_event()
                    elif user_choice == '10':
                        export_events()
                    elif user_choice == '11':
                        import_attendees()
                    elif user_choice == '12':
                        print("Logging out.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '14':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
