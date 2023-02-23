from datetime import datetime
from flask import (
    redirect, url_for
)

# some functions that we can use anywhere in the app
def isEndAfterStart(date1, date2):
    """
    Input: date1: string, date2: string
    Returns true if date2 >= date1
    """
    date1_obj = datetime.strptime(date1, '%Y-%m-%d').strftime('%Y-%m-%d')
    date2_obj = datetime.strptime(date2, '%Y-%m-%d').strftime('%Y-%m-%d')

    return date2_obj >= date1_obj


def dataForUserTable(users, proyects):
    """
    Input: users: sql row object, proyects: sql row object
    Returns: a dict with the data of users and proyects
    """

    # create a list of the proyects
    proyectList = {}
    for proyect in proyects:
        proyectList[proyect['id']] = proyect['description']
    
    roles = {
        'op_manager' : 'Gerente de operaciones',
        'mechanic_sup' : 'Supervisor del area de mecanica',
        'painting_sup' : 'Supervisor del area de latoneria y pintura',
        'mechanic_spec' : 'Especialista en mecanica',
        'electricity_spec' : 'Especialista en electricidad',
        'waiting': ''
    }

    data = []

    for user in users: 
        proyect = ''
        if user['proyId'] is not None:
            proyect = proyectList[user['proyId']]

        data.append(
            {
                'id': user['id'],
                'username': user['username'],
                'firstname': user['firstname'],
                'secondname': user['secondname'],
                'role': roles[user['role']],
                'proyect': proyect,
                'auth': user['auth']
            }
        )

    return data

def dataForProyectTable(proyects):
    """
    Input: proyects: sql row object
    Returns: a dict with the data of proyects
    """

    data = []
    for proyect in proyects:
        status = 'Closed'
        if proyect['status'] == 1:
            status = 'Enabled'

        data.append(
            {
                'id': proyect['id'],
                'description': proyect['description'],
                'start': proyect['start'],
                'end': proyect['end'],
                'status': status
            }
        )

    return data


def redirectToUser(user):
    if user['role'] == 'admin':
        return redirect(url_for('user.root'))

    elif user['role'] == 'op_manager':
        return redirect(url_for('user.manager'))

def dataForLoggerTable(logs):
    """
    Input: logs: sql row object
    Returns: a dict with the data of logs
    """

    data = []
    for log in logs:
        data.append(
            {
                'id': log['id'],
                'date': log['date'],
                'event': log['event'],
                'user': log['user']
            }
        )
    return data

def findProyectDescById(db, id):
    '''
        Input: db: data base conexion object
               id: integer, id of the proyect
        Returns: The description of the proyect whose id is the given
    '''

    return db.execute(
        'SELECT description FROM proyect WHERE id = ?',
        (id),
    ).fetchone()['description']

def findUsernameById(db, id):
    '''
        Input: db: data base conection object
               id: integer, id of the user
        Returns: Username whose id is the given
    '''

    return db.execute(
        'SELECT username FROM user WHERE id = ?',
        (id)
    ).fetchone()['username']

def getEventMsg(db, content, mode):
    '''
        Input: db data base conection object
               content of the message of the event
               mode: mode of the event
        Returns: A string that represents the event
    '''
    roles = {
        'op_manager' : 'Gerente de operaciones',
        'mechanic_sup' : 'Supervisor del area de mecanica',
        'painting_sup' : 'Supervisor del area de latoneria y pintura',
        'mechanic_spec' : 'Especialista en mecanica',
        'electricity_spec' : 'Especialista en electricidad',
        'waiting': ''
    }

    msg = ''
    if mode == 'register':
        msg = f'Register user \'{content}\' into system'

    elif mode == 'createUser':
        msg = f'Create user \'{content}\''

    elif mode == 'createProyect':
        msg = f'Create proyect \'{content}\''

    elif mode == 'setProyect': 
        msg = f'Set proyect \'{findProyectDescById(db, content[1])}\' to user \'{content[0]}\''

    elif mode == 'setRole':
        msg = f'Set role \'{roles[content[1]]}\' to user \'{content[0]}\''

    elif mode == 'rejectUser':
        msg = f'Reject user \'{findUsernameById(db, content)}\''

    elif mode == 'aproveUser':
        msg = f'Aprove user \'{content}\''

    elif mode == 'deleteUser':
        msg = f'Delete user \'{findUsernameById(db, content)}\''

    elif mode == 'enableProyect':
        msg = f'Enable proyect \'{findProyectDescById(db, content)}\''

    elif mode == 'closeProyect':
        msg = f'Close proyect \'{findProyectDescById(db, content)}\''
    
    elif mode == 'deleteProyect':
        msg = f'Delete proyect \'{findProyectDescById(db, content)}\''

    elif mode == 'unauthorizedUser':
        msg = f'User \'{content}\' unauthorized'

    elif mode == 'removeProyect':
        msg = f'User \'{content}\' has no proyect assigned'
    
    elif mode == 'changeDates':
        msg = f'Dates of proyect \'{findProyectDescById(db, content)}\' changed'
    return msg

def loggerQuery(db, user, mode, content):
    '''
        Input: db: data base conexion object
               user: user of the log
               mode: operation 
        Returns: Insert a log in logger table 
    '''

    # curr time
    now = datetime.now()
    currtime = now.strftime('%D - %H:%M')

    db.execute(
        'INSERT INTO logger (event, date, user) VALUES (?, ?, ?)',
        (getEventMsg(db, content, mode), currtime, user)
    )