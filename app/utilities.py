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

def redirectFromProyect(user):
    if user['roleId'] == 1:
        return redirect(url_for('proyectView.proyectView'))

    elif user['roleId'] == 3:
        return redirect(url_for('user.manager'))

def redirectFromLogger(user):
    if user['roleId'] == 1:
        return redirect(url_for('user.root'))
    
    elif user['roleId'] == 3:
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


def findRoleNameById(db, id):
    '''
        Input: db: data base conection object
               id: integer, id of the role
        Returns: The name of the role whose id is the given
    '''
    return db.execute(
        'SELECT name FROM roles WHERE id = ?',
        (id,)
    ).fetchone()['name']

def findUsernameById(db, id):
    '''
        Input: db: data base conection object
               id: integer, id of the user
        Returns: Username whose id is the given
    '''

    return db.execute(
        'SELECT username FROM user WHERE id = ?',
        (id,)
    ).fetchone()['username']

def findClientNameById(db, id):
    return db.execute(
        'SELECT firstname FROM clients WHERE id = ?',
        (id)
    ).fetchone()['firstname']

def findCarInfoById(db, id):
    info = db.execute('SELECT brand, model FROM cars WHERE id = ?', (id)).fetchone()

    return info['brand'] + ' ' + info['model']

def getEventMsg(db, content, mode):
    '''
        Input: db data base conection object
               content of the message of the event
               mode: mode of the event
        Returns: A string that represents the event
    '''

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
        msg = f'Set role \'{findRoleNameById(db, content[1])}\' to user \'{content[0]}\''

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

    elif mode == 'changePassword':
        msg = f'User \'{content}\' changed it\'s password'

    elif mode == 'addClient':
        msg = f'Client \'{content}\' was added'

    elif mode == 'deleteClient':
        msg = f'Client \'{findClientNameById(db, content)}\' was deleted'

    elif mode == 'modifyClient':
        msg = f'Client \'{findClientNameById(db, content)}\' was modified'

    elif mode == 'addCar':
        msg = f'Car \'{content[1]} {content[2]}\' was addeed to user \'{findClientNameById(db, content[0])}\''

    elif mode == 'deleteCar':
        msg = f'Car \'{findCarInfoById(db, content)}\' was deleted'

    elif mode == 'modifyCar':
        msg = f'Car \'{content[0]} {content[1]}\' was modified'
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

def dataForUserProfileInfoTable(userInfo):
    """
    Input: userInfo: sql row object
    Returns: a dict with the data of userInfo
    """

    dataInfo = []
    for info in userInfo:
        dataInfo.append(
            {
                'firstname': info['firstname'],
                'secondname': info['secondname'],
                'role': info['role'],
            }
        )

    return dataInfo