
LESS_THAN = 0
MORE_THAN = 1

def value(operator: str):
    
    if operator == LESS_THAN:
        return "<"
    if operator == MORE_THAN:
        return ">"
    return ""