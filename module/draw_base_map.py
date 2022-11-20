import pydeck as pdk

def draw_map(working_driver, order_items, delivery_items):
    # 승차위치 연두색
    driver_layer = pdk.Layer(
        'ScatterplotLayer',
        working_driver, 
        get_radius=15,
        get_position='[current_lon, current_lat]',
        get_color=[255,50,0]
    )

    # 하차위치 푸른색
    item_layer = pdk.Layer(
        'ScatterplotLayer',
        order_items, 
        get_radius=10,
        get_position='[O_lon, O_lat]',
        get_color=[0,50,255]
    )
    # 빨강 위치
    delivery_layer = pdk.Layer(
        'ScatterplotLayer',
        delivery_items, 
        get_radius=10,
        get_position='[D_lon, D_lat]',
        get_color=[0,255,50]
    )


    base_map = pdk.Deck(layers=[driver_layer,item_layer, delivery_layer],
                        initial_view_state={"latitude": 37.52942, 
                                            "longitude":126.90484,
                                            'zoom':13})

    return base_map