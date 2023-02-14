def get_BB_cords(data_frame):

    # cords of one frame
    cof = {}

    print(len(data_frame))
    for x in range(0, len(data_frame)):
        cof[data_frame.at[x, 'name'] + f'{x}'] = [data_frame.at[x, 'xmin'], data_frame.at[x, 'xmax']]

    return cof

    #print(cof)
    #for key, value in cof.items():
    #    print(f'Name: {key}; xmin: {value[0]}, xmax: {value[1]}')