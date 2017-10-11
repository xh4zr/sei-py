def generate_query_string(params):
    query = []
    first = True
    for key, value in params.items():
        symbol = '&'
        if first:
            symbol = '?'
            first = False

        query.append('{symbol}{key}={value}'.format(symbol=symbol, key=key, value=value))
    return ''.join(query)
