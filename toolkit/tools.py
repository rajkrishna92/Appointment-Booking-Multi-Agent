import pandas as pd
from typing import  Literal
from langchain_core.tools import tool
from utils.data_model import *


@tool
def check_availability(desired_date:DateModel, name:Literal["Alice Johnson", "Bob Singh", "Charlie Wang", "Diana Patel", "Ethan Roy","Fiona Zhang", "George Kim", "Helen Thomas", "Ian Verma", "Jessica Lee"]):
    """
    Checking the database if we have availability.
    The parameters should be mentioned by the user in the query
    """
    df = pd.read_csv(r"data/availability.csv")
    
    #print(df)
    
    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    
    rows = list(df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date)&(df['name'] == name)&(df['is_available'] == True)]['date_slot_time'])

    if len(rows) == 0:
        output = "No availability in the entire day"
    else:
        output = f'This availability for {desired_date.date}\n'
        output += "Available slots: " + ', '.join(rows)

    return output

@tool
def check_availability_by_specialization(desired_date:DateModel, specialization:Literal["Network Security", "SoftwareDevelopment", "Data Analysis", "System Administration","Cybersecurity", "Cloud Computing", "Database Management", "AI/ML","Technical Support", "Web Development"]):
    """
    Checking the database if we have availability for the specific specialization.
    The parameters should be mentioned by the user in the query
    """
    #Dummy data
    df = pd.read_csv(r"data/availability.csv")
    df['date_slot_time'] = df['date_slot'].apply(lambda input: input.split(' ')[-1])
    rows = df[(df['date_slot'].apply(lambda input: input.split(' ')[0]) == desired_date.date) & (df['specialization'] == specialization) & (df['is_available'] == True)].groupby(['specialization', 'name'])['date_slot_time'].apply(list).reset_index(name='available_slots')

    if len(rows) == 0:
        output = "No availability in the entire day"
    else:
        def convert_to_am_pm(time_str):
            # Split the time string into hours and minutes
            time_str = str(time_str)
            hours, minutes = map(int, time_str.split(":"))
            
            # Determine AM or PM
            period = "AM" if hours < 12 else "PM"
            
            # Convert hours to 12-hour format
            hours = hours % 12 or 12
            
            # Format the output
            return f"{hours}:{minutes:02d} {period}"
        output = f'This availability for {desired_date.date}\n'
        for row in rows.values:
            output += row[1] + ". Available slots: \n" + ', \n'.join([convert_to_am_pm(value)for value in row[2]])+'\n'

    return output

@tool
def set_appointment(desired_date:DateTimeModel, name:Literal["Alice Johnson", "Bob Singh", "Charlie Wang", "Diana Patel", "Ethan Roy","Fiona Zhang", "George Kim", "Helen Thomas", "Ian Verma", "Jessica Lee"], candidate_name:str):
    """
    Set appointment or slot.
    The parameters MUST be mentioned by the user in the query.
    """
    df = pd.read_csv(r"data/availability.csv")
   
    from datetime import datetime
    def convert_datetime_format(dt_str):
        # Parse the input datetime string
        #dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        dt = datetime.strptime(dt_str, "%d-%m-%Y %H:%M")
        
        # Format the output as 'DD-MM-YYYY H.M' (removing leading zero from hour only)
        return dt.strftime("%d-%m-%Y %#H:%M")
    
    case = df[(df['date_slot'] == convert_datetime_format(desired_date.date))&(df['name'] == name)&(df['is_available'] == True)]
    if len(case) == 0:
        return "No available appointments for that particular case"
    else:
        df.loc[(df['date_slot'] == convert_datetime_format(desired_date.date))&(df['name'] == name) & (df['is_available'] == True), ['is_available','candidate_name']] = [False, candidate_name]
        df.to_csv(f'data/availability.csv', index = False)
        return "Successfully done"
    
@tool
def cancel_appointment(date:DateTimeModel, name:Literal["Alice Johnson", "Bob Singh", "Charlie Wang", "Diana Patel", "Ethan Roy","Fiona Zhang", "George Kim", "Helen Thomas", "Ian Verma", "Jessica Lee"], candidate_name: str):
    """
    Canceling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    df = pd.read_csv(r"data/availability.csv")
    case_to_remove = df[(df['date_slot'] == date.date)&(df['candidate_name'] == candidate_name)&(df['name'] == name)]
    if len(case_to_remove) == 0:
        return "You don´t have any appointment with that specifications"
    else:
        df.loc[(df['date_slot'] == date.date) & (df['candidate_name'] == candidate_name) & (df['name'] == name), ['is_available', 'candidate_name']] = [True, None]
        df.to_csv(f'data/availability.csv', index = False)

        return "Successfully cancelled"
    

@tool
def reschedule_appointment(old_date:DateTimeModel, new_date:DateTimeModel, name:Literal["Alice Johnson", "Bob Singh", "Charlie Wang", "Diana Patel", "Ethan Roy","Fiona Zhang", "George Kim", "Helen Thomas", "Ian Verma", "Jessica Lee"], candidate_name:str,):
    """
    Rescheduling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    df = pd.read_csv(r"data/availability.csv")
    available_for_desired_date = df[(df['date_slot'] == new_date.date)&(df['is_available'] == True)&(df['name'] == name)]
    if len(available_for_desired_date) == 0:
        return "Not available slots in the desired period"
    else:
        cancel_appointment.invoke({'date':old_date, 'candidate_name':candidate_name, 'name':name})
        set_appointment.invoke({'desired_date':new_date, 'candidate_name':candidate_name, 'name':name})
        return "Successfully rescheduled for the desired time"
    
if __name__ == "__main__":
    print(check_availability.invoke({'desired_date': {'date': '01-01-2025'}, 'name': 'Alice Johnson'}))
    print(check_availability_by_specialization.invoke({'desired_date': {'date': '07-07-2025'}, 'specialization': 'Technical Support'}))
    print(set_appointment.invoke({'desired_date': {'date': '08-06-2025 10:00'}, 'name': 'Helen Thomas', 'candidate_name': 'Rajkrishna'}))
    print(cancel_appointment.invoke({'date': {'date': '01-01-2025 10:00'}, 'candidate_name': 'John Doe', 'name': 'Diana Patel'}))
    print(reschedule_appointment.invoke({'old_date': {'date': '01-01-2025 10:00'}, 'new_date': {'date': '02-01-2025 11:00'}, 'candidate_name': 'John Doe', 'name': 'Diana Patel'}))
