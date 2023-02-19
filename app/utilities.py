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
        'electricity_spec' : 'Especialista en electricidad'
    }
    
    data = []

    for user in users:
        data.append(
            {
                'id': user['id'],
                'username': user['username'],
                'firstname': user['firstname'],
                'secondname': user['secondname'],
                'role': roles[user['role']],
                'proyect': proyectList[user['proyId']]
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