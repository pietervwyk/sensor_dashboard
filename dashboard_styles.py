from dash import html, dcc, Input, Output

def style():
    '''Returns a style dict, for base html.Div.'''
    return {
        'margin-left': '2%',
        'margin-right': '2%',
    }

def center():
    '''Retuns a style dict, for centering a div'''
    return {
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }

def title():
    return {
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center',
        'font-family': "Roboto",
        'font-weight': 400,    
    }