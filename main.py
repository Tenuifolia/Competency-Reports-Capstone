
import sqlite3
import datetime
import csv
def current_column_values(column, table, active = 'X', manager = '0', assess_res = [], pwd = '' ):
    # Read list of current column values for future comparing against 
    connection = sqlite3.connect('Competency.db')
    cursor = connection.cursor()
    cells_list = []
    if manager == '1':
        cells = cursor.execute(f"SELECT user_id FROM {table} WHERE is_manager = '{manager}' AND active = '1'")
    elif pwd and active == '1':
        cells = cursor.execute(f"SELECT {column} FROM {table} WHERE email = '{pwd}' and active = {active}")
    elif active == '1' or active == '0':
        cells = cursor.execute(f"SELECT {column} FROM {table} WHERE Active = '{active}'")
    elif assess_res:
        cells = cursor.execute(f"SELECT {column[0]}, {column[1]} FROM {table} WHERE user_id = '{assess_res[0]}' AND assessment_id = {assess_res[1]}")
        for row in cells:
            cells_list.append(row)
        return cells_list
    else:
         cells = cursor.execute(f"SELECT {column} FROM {table}")
    for row in cells:
        cells_list.append(str(row[0]))
    return cells_list

def add_row(table, field_list, current_values_1 = [], current_values_2 = [], current_values_3 = []):
    fields, inputs = verify_add_inputs(field_list, current_values_1, current_values_2, current_values_3)
    
    connection = sqlite3.connect('Competency.db')
    cursor = connection.cursor()

    query = f"INSERT INTO {table} ({fields}) VALUES({'?'+((',?')*(len(fields.split(','))-1))})"
    values = tuple(inputs)
    cursor.execute(query, values)
    connection.commit()
    print("\n Completed! \n")

def edit_row(table, field, new_value, id_name, id, id_name_2 = '', id_2 = ''):

    connection = sqlite3.connect('Competency.db')
    cursor = connection.cursor()
    if id_2:
        query = f"UPDATE {table} SET {field} = ? WHERE {id_name} = {id} AND {id_name_2} = {id_2}"
    else:
        query = f"UPDATE {table} SET {field} = ? WHERE {id_name} = {id}"
    cursor.execute(query, tuple(new_value))
    connection.commit()
    print("\n Completed! \n")

def delete_row(user_id, assessment_id):
    connection = sqlite3.connect('Competency.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM Assessment_Results WHERE user_id = {user_id} AND assessment_id = {assessment_id}")
    connection.commit()
    print("\n Completed! \n")

def verify_add_inputs(field_list, current_values_1 = [], current_values_2 = [], current_values_3 = []):
    values = []
    for field in field_list:
        if field == 'email':
            user_input = input(f'Enter their {field}: ')
            while user_input in current_values_1:
                user_input = input(f'Please enter a unique {field}: ').strip().lower()
            values.append(user_input)
        elif field in ['date_created', 'date_hired', 'date_taken', 'date_created']: 
            date = input(f'Enter their {field}. (mm-dd-yyyy): ').split('-')
            while True:
                date_is_valid = True
                if len(date) != 3:
                    date_is_valid = False
                else:
                    month, day, year = date
                    try :
                        datetime.date(int(year), int(month), int(day))
                    except ValueError :
                        date_is_valid = False
                if date_is_valid:
                    user_input = '/'.join(date) 
                    break
                else: 
                    date = input(f'Please enter a valid {field}. (mm/dd/yyyy): ').split('/')
            values.append(user_input)
        elif field =='is_manager':
            user_input = input(f'Enter their role, Employee or Manager: ').lower()
            while user_input not in ['employee','e','0','manager','m','1']:
                user_input = input(f'Please enter if they are an Employee or a Manager: ').lower()
            values.append('1') if user_input in ['manager','m','1'] else values.append('0')
        elif field == 'user_id':
            user_input = input(f'Enter their {field}: ')
            while user_input not in current_values_1:
                user_input = input(f'Please enter a valid, current {field}: ')
            values.append(user_input)
        elif field == 'assessment_id':
            user_input = input(f'Enter the {field}: ')
            while user_input not in current_values_2:
                user_input = input(f'Please enter a valid {field}: ')
            values.append(user_input)
        elif field == 'manager_id':
            user_input = input(f"Enter the ID number of the manager who requested this assessment. (Enter '0' if none): ").lower()
            while user_input not in current_values_3 and user_input != '0':
                user_input = input('Please enter a valid manager ID number: ')
            values.append(user_input)
        elif field == 'competency_id':
            user_input = input(f"Enter the {field} number: ").lower()
            while user_input not in current_values_1:
                user_input = (f'Please enter a valid {field} number: ')
            values.append(user_input)
        elif field == 'name':
            user_input = input(f"Enter the competency {field}: ")
            while user_input in current_values_1:
                user_input = (f'Please enter a valid competency {field}: ')
            values.append(user_input)
        else:
            values.append(input(f'Enter their {field}: '))

    return (','.join(field_list), values)

def verify_edit_inputs(table, column_names, key_1, key_2 = '', current_values_1 = [], current_values_2 = [], current_values_3 = []):
    if key_2:
        user_input = input(f"Enter the assessment taker's {key_1}: ")
        while user_input not in current_column_values('user_id', 'Assessment_Results') and user_input != 'q':   
            while user_input not in current_column_values('user_id', 'Users', '1') and user_input != 'q':
                user_input = input(f'Please enter a valid {key_1}: ').lower()
            user_input = input(f"No existing Assessment Results for that User, choose a different user, or Enter 'Q' to exit: ").lower()  
        if user_input == 'q':
            exit
        user_input2 =  user_input = input(f"Enter the correlating {key_2}: ")
        while (user_input, user_input2) not in current_column_values(('user_id', 'assessment_id'), 'Assessment_Results', 'X', '0', '1'):
            while user_input2 not in current_column_values('assessment_id', 'Assessments') and user_input2 != 'q':
                user_input2 = input(f'Please enter a valid {key_2}: ').lower()
            user_input2 = input(f"No existing Assessment Results for that User - Assessment_ID combo, choose a different Assessment_ID, or Enter 'Q' to exit: ").lower()
        if user_input2 == 'q':
            exit
        
        user_input3 = input("Enter the field to edit: ")
        while user_input3 not in column_names:
            user_input3 = input(f"Please enter a valid field from {table}: ")
        field, user_input4 = verify_add_inputs([user_input3],current_values_1, current_values_2, current_values_3)
        return (user_input, user_input2, user_input4, field)
    elif key_1 == 'employee':
        user_input3 = input("Enter the field to edit: ")
        while user_input3 not in column_names:
            user_input3 = input(f"Please enter a valid field from {table}: ")
        field, user_input4 = verify_add_inputs([user_input3],current_values_1, current_values_2, current_values_3)
        return (current_user_id, user_input4, field)

    else:        
        user_input = input(f"Enter the {key_1} to edit: ")
        while user_input not in current_column_values(key_1, table):
            user_input = input(f"Please enter a valid {key_1}: ")

        user_input3 = input("Enter the field to edit: ")
        while user_input3 not in column_names:
            user_input3 = input(f"Please enter a valid field from {table}: ")
        field, user_input4 = verify_add_inputs([user_input3],current_values_1, current_values_2, current_values_3)
        return (user_input, user_input4, field)

users_list = ['first_name', 'last_name', 'phone', 'email', 'password', 'date_created', 'date_hired', 'is_manager']
assess_results_list = ['user_id', 'assessment_id', 'assessment_score', 'date_taken', 'manager_id']
assessments_list = ['competency_id', 'date_created']
competencies_list = ['name', 'date_created']

print('\n-------------------------------')
print('      Competency Reports')
print('            Sign In')
print('-------------------------------\n')

user_name = input("Enter your Username: ")
while user_name not in current_column_values('email', 'Users', '1'):
    user_name = input("Please enter a valid Username: ")
pwd = input("Enter you password: ")
while pwd not in current_column_values('password', 'Users', '1', pwd = user_name):
    pwd = input("Wrong password, try again: ")

current_user_id = (current_column_values('user_id', 'Users', '1', pwd = user_name))[0]
print(current_user_id)
access = current_column_values('is_manager', 'Users', '1', pwd = user_name)
if access[0] == '1':
    
    print('\n-------------------------------')
    print('      Choose your Portal')
    print('-------------------------------\n')
    print('  1) Manager Portal')
    print('  2) Personal Portal')
    choice = input("\nEnter Manager Portal, or Personal Portal: ").lower()
    while choice not in ['manager portal', 'manager', 'm', '1', 'personal portal', 'personal', 'p', '2']:
        choice = input("Please enter a valid option: ")


if access[0] == '0' or choice in ['personal portal', 'personal', 'p', '2']:
    while True:
        print('\n\n-------------------------------')
        print('      Competency Reports')
        print('        Personal Portal')
        print('-------------------------------\n')

        print('  1) View your Assessment Reports')
        print('  2) Edit your Contact Information')
        print('  9) Quit\n')

        user_input1 = input('Select a function: ').lower()
        while user_input1 not in ['1','2','9','q','v','e']:
            user_input1 = input("Please enter a valid response: ")
        if user_input1 == '1' or user_input1 =='v':
            if current_user_id in current_column_values('user_id', 'Assessment_Results'):
                connection = sqlite3.connect('Competency.db')
                cursor = connection.cursor()
                rows = cursor.execute(f"SELECT * FROM Assessment_Results WHERE user_id = {current_user_id}")
                print(f"{'user_id':<10}{'assessment_id':<15}{'assessment_score':<18}{'date_taken':<15}{'manager_id':<12}")
                print(f"{'-------':<10}{'-------------':<15}{'----------------':<18}{'----------':<15}{'----------':<15}")
                for row in rows:
                    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<18}{row[3]:<15}{row[4]:<12}")
                input("\n<Enter to Continue>\n")
            else:
                input("No current Assessment Results for this user. ")
        elif user_input1 == '2' or user_input1 =='e':
            connection = sqlite3.connect('Competency.db')
            cursor = connection.cursor()
            rows = cursor.execute(f"SELECT * FROM Users WHERE user_id = {current_user_id}")
            print(f"{'user_id':<10}{'first_name':<15}{'last_name':<15}{'phone':<15}{'email':<25}{'password':<20}\
{'date_created':<15}{'date_hired':<15}{'is_manager':<14}{'active':<7}")
            print(f"{'-------':<10}{'----------':<15}{'---------':<15}{'-----':<15}{'-----':<25}{'--------':<20}\
{'------------':<15}{'----------':<15}{'----------':<14}{'------':<7}")
            for row in rows:
                print(f"{row[0]:<10}{row[1]:<15}{row[2]:<15}{row[3]:<15}{row[4]:<25}{row[5]:<20}\
{row[6]:<15}{row[7]:<15}{row[8]:<14}{row[9]:<7}\n")

            email_list = current_column_values('email', 'Users', '1')
            user_id, new_value, field = verify_edit_inputs('Users', users_list, 'employee', '', email_list)
            edit_row('Users', field, new_value, 'user_id', current_user_id)
        else:
            break 
        


if access[0] == '1' and choice in ['manager portal', 'manager', 'm', '1']:
    while True:
        print('\n-------------------------------')
        print('      Competency Reports')
        print('        Manager Portal')
        print('-------------------------------\n')

        print('  1) Add a Row')
        print('  2) Edit a Row')
        print('  3) Delete a Row')
        print('  4) Print/Import Reports')
        print('  9) Quit\n')

        user_input1 = input('Select a function: ').lower()
        while user_input1 not in ['1','2','3','4','9','q','a','e','d','r']:
            user_input1 = input("Please enter a valid response: ")
        if user_input1 == '9' or user_input1 == 'q':
                break
        

        if user_input1 in ['1','2','a','e']:         
            print('\n-------------------------------')
            print('           Tables')
            print('-------------------------------\n')


            print('\n  1) Users')
            print('  2) Assessment Result')
            print('  3) Assessments')
            print('  4) Competencies')
            print('  9) Quit\n')

            user_input2 = input('Select the table to alter: ').lower()
            while user_input2 not in ['1','2','3','4','9','q','a','e','d','u','r','c']:
                user_input1 = input("Please enter a valid response: ")

            if user_input1 == '1' or user_input1 == 'a':
                if user_input2 == '1' or user_input2 =='u':
                    email_list = current_column_values('email', 'Users', '1')
                    add_row('Users',users_list, email_list)
                elif user_input2 == '2' or user_input2 =='r':
                    user_id_list = current_column_values('user_id', 'Users', '1')
                    assess_id_list = current_column_values('assessment_id', 'Assessments')
                    manager_id_list = current_column_values('is_manager', 'Users', '1', '1')
                    add_row('Assessment_Results', assess_results_list, user_id_list, assess_id_list, manager_id_list)
                elif user_input2 == '3' or user_input2 =='a':
                    competency_id_list = current_column_values('competency_id', 'Competencies')
                    add_row('Assessments',assessments_list, competency_id_list)
                elif user_input2 == '4' or user_input2 =='c':
                    competency_name_list = current_column_values('name', 'Competencies')
                    add_row('Competencies',competencies_list, competency_name_list)
                elif user_input2 == '9' or user_input2 == 'q':
                    break

            elif user_input1 == '2'or user_input1 == 'e':
                if user_input2 == '1' or user_input2 =='u':
                    email_list = current_column_values('email', 'Users', '1')
                    user_id, new_value, field = verify_edit_inputs('Users', users_list, 'user_id', '', email_list)
                    edit_row('Users', field, new_value, 'user_id', user_id)
            
                elif user_input2 == '2' or user_input2 =='r':
                    manager_id_list = current_column_values('user_id', 'Users', '1', '1')
                    user_id, assessment_id, new_value, field = verify_edit_inputs('Assessment_Results', assess_results_list, 'user_id', 'assessment_id', current_values_3 = manager_id_list)
                    edit_row('Assessment_Results', field, new_value, 'user_id', user_id, 'assessment_id', assessment_id)
                elif user_input2 == '3'  or user_input2 =='a':
                    competency_id_list = current_column_values('competency_id', 'Competency')
                    assessment_id, new_value, field = verify_edit_inputs('Assessments', assessments_list, 'assessment_id')
                    edit_row('Assessments',field, new_value, 'assessment_id', assessment_id)
                elif user_input2 == '4' or user_input2 =='c':
                    competency_name_list = current_column_values('name', 'Competency')
                    competency_id, new_value, field = verify_edit_inputs('Competencies', competencies_list, 'competency_id')
                    edit_row('Competencies', field, new_value, 'competency_id', competency_id)
                elif user_input2 == '9' or user_input2 == 'q':
                    break

        elif user_input1 in ['3','d']:
            print('\n-------------------------------')
            print('           Remove Rows')
            print('-------------------------------\n')


            print('\n  1) Deactivate a User')
            print('  2) Reactivate a User')
            print('  3) Delete an Assessment')
            print('  9) Quit\n')

            user_input2 = input('Select the table to alter: ').lower()
            while user_input2 not in ['1','2','3','9','q','d','r','a']:
                user_input1 = input("Please enter a valid response: ")

            if user_input2 == '1' or user_input2 == 'd':
                user_input3 = input('Enter the user_id to Deactivate: ')
                while user_input3 not in current_column_values('user_id', 'Users', '1'):
                    user_input3 = input("Please enter a valid Username: ")
                edit_row('Users', 'active', '0', 'user_id', user_input3)
                print("\n Completed! \n")
            elif user_input2 == '2' or user_input2 == 'r':
                user_input3 = input('Enter the user_id to Reactivate: ')
                while user_input3 not in current_column_values('user_id', 'Users', '0'):
                    user_input3 = input("Please enter a valid Username: ")
                    if user_input3 in ['9', 'q', 'Q', 'quit']:
                        break
                if user_input3 not in ['9', 'q', 'Q', 'quit']:
                    edit_row('Users', 'active', '1', 'user_id', user_input3)
                    print("\n Completed! \n")
            elif user_input2 == '3' or user_input2 == 'a':
                user_input = input(f"Enter the assessment taker's user_id: ")
                while user_input not in current_column_values('user_id', 'Assessment_Results') and user_input != 'q':   
                    while user_input not in current_column_values('user_id', 'Users', '1') and user_input != 'q':
                        user_input = input(f'Please enter a valid user_id: ').lower()
                    user_input = input(f"No existing Assessment Results for that User, choose a different user, or Enter 'Q' to exit: ").lower()  
                if user_input == 'q':
                    exit
                user_input2 = input(f"Enter the correlating assessment_id: ")
                while (int(user_input), int(user_input2)) not in current_column_values(('user_id', 'assessment_id'), 'Assessment_Results', 'X', '0', [user_input, user_input2]):
                    print(int(user_input), int(user_input2))
                    print(current_column_values(('user_id', 'assessment_id'), 'Assessment_Results', 'X', '0', [user_input, user_input2]))
                    while user_input2 not in current_column_values('assessment_id', 'Assessments') and user_input2 != 'q':
                        user_input2 = input(f'Please enter a valid assessment_id: ').lower()
                    user_input2 = input(f"No existing Assessment Results for that User-Assessment_ID combo, choose a different Assessment_ID, or Enter 'Q' to exit: ").lower()
                    if user_input2 == 'q':
                        break
                if user_input2 not in ['9', 'q', 'Q', 'quit']:
                    delete_row(user_input, user_input2)

            
        elif user_input1 in ['4','r']:
            print('\n-------------------------------')
            print('     Print/Import Reports')
            print('-------------------------------\n')


            print('\n  1) User Competency Summary')
            print('  2) Competency Results Summary')
            print('  3) Export Users CSV')
            print('  4) Export Competencies CSV')
            print('  5) Import Assessment Results')
            print('  9) Quit\n')
            
            user_input2 = input('Select the report: ').lower()
            while user_input2 not in ['1','2','3','4','5','9','u','c','q']:
                user_input1 = input("Please enter a valid response: ")

            if user_input2 in ['1','u']:
                user_input3 = input('Enter the desired user_id number: ')
                while user_input3 not in (current_column_values('user_id', 'Users', '1')):
                    user_input3 = input('Please enter a valid user_id number: ')

                connection = sqlite3.connect('Competency.db')
                cursor = connection.cursor()
                print("\n  User Competency Summary")
                print("---------------------------")
                rows = cursor.execute(f"SELECT * FROM Users WHERE user_id = {user_input3}")
                print(f"\n{'user_id':<10}{'first_name':<15}{'last_name':<15}{'phone':<15}{'email':<25}{'password':<20}\
{'date_created':<15}{'date_hired':<15}{'is_manager':<14}{'active':<7}")
                print(f"{'-------':<10}{'----------':<15}{'---------':<15}{'-----':<15}{'-----':<25}{'--------':<20}\
{'------------':<15}{'----------':<15}{'----------':<14}{'------':<7}")
                for row in rows:
                    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<15}{row[3]:<15}{row[4]:<25}{row[5]:<20}\
{row[6]:<15}{row[7]:<15}{row[8]:<14}{row[9]:<7}\n") 
                
                score_sum = 0
                score_count = 0
                rows = cursor.execute(f"SELECT * FROM Assessment_Results WHERE user_id = {user_input3}")
                print(f"\n{'user_id':<10}{'assessment_id':<15}{'assessment_score':<18}{'date_taken':<15}{'manager_id':<12}")
                print(f"{'-------':<10}{'-------------':<15}{'----------------':<18}{'----------':<15}{'----------':<15}")
                for row in rows:
                    print(f"{row[0]:<10}{row[1]:<15}{row[2]:<18}{row[3]:<15}{row[4]:<12}")
                    score_sum += int(row[2]) 
                    score_count += 1
                score_average = score_sum / len(current_column_values('name', 'Competencies'))
                print(f"\n{'Average Score':<15}\n{'-------------':<15}")
                print(f"{score_average:.2f}")
                print(f"\n{'Missing Assessments':<22}\n{'------------------':<22}")
                print(f"{len(current_column_values('name', 'Competencies')) - score_count}")
                input("\n<Enter to Continue>\n")
            
            elif user_input2 in ['2','c']:
                connection = sqlite3.connect('Competency.db')
                cursor = connection.cursor()
                users_names = cursor.execute(f"SELECT user_id, first_name, last_name FROM Users")
                users_names_dict = {}
                for row in users_names:
                    users_names_dict[row[0]] = f"{row[1]} {row[2]}"
                user_2_assess_dict = []
                lines = cursor.execute(f"SELECT user_id, assessment_id FROM Assessment_Results")
                for row in lines:
                    user_2_assess_dict.append((row[0],row[1]))
                assess_2_comp_dict = {}
                lines2 = cursor.execute(f"SELECT assessment_id, competency_id FROM Assessments")
                for row in lines2:
                    assess_2_comp_dict[row[0]] = row[1]
                comp_id_2_name_dict = {}
                lines3 = cursor.execute(f"SELECT competency_id, name FROM Competencies")
                for row in lines3:    
                    comp_id_2_name_dict[row[0]] = row[1]
                id_2_score_date = {}
                lines4 = cursor.execute(f"SELECT assessment_id, assessment_score, date_taken FROM Assessment_Results")
                for row in lines4:
                    id_2_score_date[row[0]] = [row[1], row[2]]
                user_input4 = input('Select a Competency: ')
                while user_input4 not in (current_column_values('competency_id', 'Competencies')):
                    user_input_4 = input("Please enter a valid Competency: ")                
                competency_sum = 0
                user_count = 0
                print("\n  Competency Results Summary")
                print("-------------------------------")
                print(f"\n{'user_id':<10}{'full_name':<20}{'competency_name':<25}{'assessment_id':<15}{'assessment_score':<18}{'date_taken':<15}")
                print(f"{'-------':<10}{'--------':<20}{'---------------':<25}{'-------------':<15}{'----------------':<18}{'----------':<15}")
                for row in user_2_assess_dict:
                    if row[1] == int(user_input4):
                        print(f"{row[0]:<10}{users_names_dict[row[0]]:<20}{comp_id_2_name_dict[assess_2_comp_dict[row[1]]]:<25}\
{row[1]:<15}{id_2_score_date[row[1]][0]:<18}{id_2_score_date[row[1]][1]:<15}")
                        competency_sum += id_2_score_date[row[1]][0]
                        user_count +=1
                competency_average = competency_sum / len(current_column_values('user_id', 'Users', '1'))
                print(f"\n{'Average Competency Score':<15}\n{'------------------------':<15}")
                print(f"{competency_average:.2f}")
                print(f"\n{'Missing Users':<22}\n{'-------------':<22}")
                print(f"{len(current_column_values('user_id', 'Users')) - user_count}")
                input("\n<Enter to Continue>\n")
            elif user_input2 in ['3']:
                connection = sqlite3.connect('Competency.db')
                cursor = connection.cursor()
                users_lists = cursor.execute("SELECT * FROM Users")
                with open('users_export.csv', 'wt') as out_file:
                    users_header_list = ['user_id','first_name', 'last_name', 'phone', 'email', 'password', 'date_created', 'date_hired', 'is_manager', 'is_active']
                    writer = csv.writer(out_file)
                    writer.writerow(users_header_list)
                    for line in users_lists:
                        writer.writerow(line)
                print('\n Completed!')
                input("\n<Enter to Continue>\n")
            elif user_input2 in ['4']:
                connection = sqlite3.connect('Competency.db')
                cursor = connection.cursor()
                competencies_lists = cursor.execute("SELECT * FROM Competencies")
                with open('competencies_export.csv', 'wt') as out_file:
                    competencies_header_list = ['competency_id','name', 'date_created']
                    writer = csv.writer(out_file)
                    writer.writerow(competencies_header_list)
                    for line in users_lists:
                        writer.writerow(line)
                print('\n Completed!')
                input("\n<Enter to Continue>\n")
            elif user_input2 in ['5']:
                connection = sqlite3.connect('Competency.db')
                cursor = connection.cursor()
                file_name = input('Enter the name of the CSV file to upload: ')
                with open(file_name, 'rt') as in_file:
                    headers = in_file.readline()
                    rows = []
                    for line in in_file:
                        rows.append(line.strip().split(','))
                query = f"INSERT INTO Assessment_Results({headers}) VALUES(?,?,?,?)"
                for row in rows:
                    values = tuple(row)
                    cursor.execute(query,values)
                connection.commit()
                print('\n Completed!')
                input("\n<Enter to Continue>\n")
            elif user_input2 in ['9','q']:
                break
        elif user_input1 == '9' or user_input1 == 'q':
                break
        else:
            break

       