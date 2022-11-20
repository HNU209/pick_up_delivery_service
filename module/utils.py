import numpy as np
import pandas as pd

def compute_straight_distance(point):
    # haversine
    km_constant = 3959* 1.609344
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [point[:,0], point[:,1], point[:,2], point[:,3]])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    km = km_constant * c
    return km

# 사용자가 원하는 컬럼의 값 순서대로 정렬
def user_sort_values(data, column, key):
    
    if len(data) > 1:
        row_list  = []
        for i in key:
            row = data.loc[data[column] == i]     
            row_list.append(row)
        row_list = pd.concat(row_list)
        row_list = row_list.reset_index(drop=True)
        
        return row_list
        
    else:
        data = data.reset_index(drop=True)
        return data    



def split_geometry_based_on_time(route, timestamp,time=1):
    target_index = [idx for idx,i in enumerate(timestamp) if i>=time][0]

    if timestamp[target_index] > time:
        target_timestamp = timestamp[target_index-1:target_index+1]
        target_route = route[target_index-1: target_index+1]

        target_figure = (time - target_timestamp[0]) / (target_timestamp[1] - target_timestamp[0])

        lat_1 = target_route[0][1]
        lon_1 = target_route[0][0]

        lat_2 = target_route[1][1]
        lon_2 = target_route[1][0]

        lat_add = (target_route[0][1] - target_route[1][1]) * target_figure
        lon_add = (target_route[0][0] - target_route[1][0]) * target_figure

        if lat_1 == lat_2:
            new_lat = lat_1
        elif lat_1 > lat_2:
            new_lat = lat_1 - lat_add
        elif lat_1 < lat_2:
            new_lat = lat_1 + lat_add
            
        if lon_1 == lon_2:
            new_lon = lon_1
        elif lon_1 > lon_2:
            new_lon = lon_1 - lon_add
        elif lon_1 < lon_2:
            new_lon = lon_1 + lon_add
            
            
        route_A, route_B = route[:target_index], route[target_index:]
        timestamp_A, timestamp_B = timestamp[:target_index], timestamp[target_index:]

        route_A = route_A + [[new_lon, new_lat]]
        route_B = [[new_lon, new_lat]] + route_B

        timestamp_A = timestamp_A + [time]
        timestamp_B = [time] + timestamp_B
        
    elif timestamp[target_index] == time:
        route_A = route[:target_index+1]
        timestamp_A = timestamp[:target_index+1]

        route_B = [route_A[-1]] + route[target_index+1:] 
        timestamp_B = [timestamp_A[-1]] + timestamp[target_index+1:]
        
        new_lat, new_lon = route_A[-1][1], route_A[-1][0]
        
    return route_A, route_B, timestamp_A, timestamp_B, [new_lat, new_lon]