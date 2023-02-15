# return dic of cord of one frame
def get_BB_cords(data_frame):
    
    # cords of one frame
    cof = {}
    
    print(len(data_frame))
    for x in range(0, len(data_frame)):
        cof[data_frame.at[x, 'name'] + f'_{x}'] = [data_frame.at[x, 'xmin'], data_frame.at[x, 'xmax']]
        
    return cof