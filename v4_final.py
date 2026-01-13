def get_positive_input(prompt):
    while True:
            raw = input(prompt).strip()
            try:
                value = int(raw)
                if value <= 0:
                    print("Please enter a positive integer.")
                    continue
                return value
            except:
                print("Please enter a valid integer.")


def get_input():
    wakesup = input("Enter when you wake up in the morning:").strip()
    task_duration = get_positive_input("Enter how many hours you want to work:")
    breaks_duration = get_positive_input("Enter how much time you need for each break:")
    lockin_duration = get_positive_input("Enter how much time you can work without getting distracted:")
    number_of_tasks = get_positive_input("Enter number of tasks:")
    tasks_list = []
    for i in range(1,number_of_tasks+1):
        f = input(f"{i}. ").strip()
        tasks_list.append(f)
    return wakesup,task_duration,breaks_duration,lockin_duration,number_of_tasks,tasks_list

def compute_time_minutes(task_duration, lockin_duration, breaks_duration):
    total_time_minutes = task_duration * 60

    total_session_count = total_time_minutes // lockin_duration
    remaining_time = total_time_minutes % lockin_duration
    breaks_count = max(0, total_session_count - 1)
    total_duration = total_time_minutes + (breaks_duration * breaks_count)

    return {
        "total_time":total_time_minutes,
        "session_count":total_session_count,
        "leftover_time":remaining_time,
        "break_count":breaks_count,
        "overall_time":total_duration
        }

def convert_wakeup_minutes(wakeup_time):
    waking = wakeup_time.strip()
    wakingup_time = waking.upper()

    time_period = wakingup_time[-2:]
    time = wakingup_time[:-2]

    hour_str, minute_str = time.split(":")

    hour = int(hour_str)
    minute = int(minute_str)

    if time_period == 'AM':
        if hour == 12:
            converted_time = 0
        else:
            converted_time = hour * 60
    if time_period == 'PM':
        if hour == 12:
            converted_time = 12 * 60
        else:
            converted_time = hour * 60 + 720

    total_time_minutes = converted_time + minute 

    return total_time_minutes
def convert_minutes_time(total_minutes):
    hour = total_minutes // 60
    minute = total_minutes % 60

    return hour,minute
def format_time_ampm(total_minutes):
    total_minutes = total_minutes % (24 * 60)

    hour_24 = total_minutes // 60
    minutes = total_minutes % 60

    if hour_24 == 0:
        hour_12 = 12
        period = "AM"
    elif hour_24 < 12:
        hour_12 = hour_24
        period = "AM"
    elif hour_24 == 12:
        hour_12 = 12
        period = "PM"
    else:
        hour_12 = hour_24 - 12
        period = "PM"
    return f"{hour_12}:{minutes:02d} {period}"

def session(ss_count,brk_count,overall_time,breaks_duration, lockin_duration,tasks_list):
    buffer = 30
    current_time = buffer + overall_time

    sessions_count = ss_count

    for i in range(1,sessions_count+1):
        if(i <= len(tasks_list)):
            session_start = format_time_ampm(current_time)
            session_end = current_time + lockin_duration
            task_name = tasks_list[i-1]
        
            break_start = format_time_ampm(session_end)
            break_end = session_end + breaks_duration
            current_time = break_end

        
            print(f"Session {i} starts at -- {session_start} ({task_name})")
            if sessions_count != i:
                print(f"break{i} -- {break_start}")
        else:
            print(f"Session{i} has no work to do as the tasks are less")

def display_summary(wakeup, hours,breaks, lockin,num_tasks, tasks):
    vals = compute_time_minutes(hours, lockin, breaks)
        
    print("----Daily Planner----")
    print(f"Wakes up at: {wakeup}")
    print(f"Task time: {hours}(hours) ({vals['total_time']}minutes)")
    print(f"break: {breaks}(minutes)")
    print(f"lockin_time: {lockin}(minutes)")
    print(f"Number of sessions: {vals['session_count']}")
    print(f"Number of breaks: {vals['break_count']}")
    print(f"Overall time for studying including breaks: {vals['overall_time']}(minutes)")
    if vals['leftover_time'] > 0:
        print("Can have another small study session")
        print(f"leftover time is : {vals['leftover_time']}")
    print(f"Number of tasks they have to finish: {num_tasks}")
    print("Tasks:")
    for i, task in enumerate(tasks, start = 1): 
            print(f"{i}.{task}")
    return   


wakeup_time,task_time,breaks_duration,lockin_duration,number_of_tasks,tasks_list = get_input()
vals = compute_time_minutes(task_time, lockin_duration, breaks_duration)
ss_count = vals['session_count']
brk_count = vals['break_count']
display_summary(wakeup_time,task_time,breaks_duration,lockin_duration,number_of_tasks,tasks_list)
overall_time = convert_wakeup_minutes(wakeup_time)
session(ss_count,brk_count,overall_time, breaks_duration,lockin_duration,tasks_list)
