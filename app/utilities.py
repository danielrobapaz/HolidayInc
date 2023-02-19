from datetime import datetime

# some functions that we can use anywhere in the app
def isEndAfterStart(date1, date2):
    """
    Input: date1: string, date2: string
    Returns true if date2 >= date1
    """
    date1_obj = datetime.strptime(date1, '%Y-%m-%d').strftime('%Y-%m-%d')
    date2_obj = datetime.strptime(date2, '%Y-%m-%d').strftime('%Y-%m-%d')

    return date2_obj >= date1_obj
