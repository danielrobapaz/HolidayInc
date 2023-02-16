# some functions that we can use anywhere in the app
def roleStyle(role):
    """
        Input: role. string that represents a role in the data base
        Returns: string that is the role translate into spansh
    """
    roles = {
        'op_manager' : 'Gerente de operaciones',
        'mechanic_sup' : 'Supervisor del area de mecanica',
        'paintin_sup' : 'Supervisor del area de latoneria y pintura',
        'mechacnic_spec' : 'Especialista en mecanica',
        'electricity_spec' : 'Especialista en electricidad'
    }

    return roles
