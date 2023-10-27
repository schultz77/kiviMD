screen_helper = """
#:import Window kivy.core.window.Window
#:set color_shadow [0, 0, 0, .2980392156862745]

<TextFieldRound@MDTextFieldRound>
    size_hint_x: None
    normal_color: color_shadow
    active_color: color_shadow

MDBoxLayout:
    id: layout_parent
    layout_1: layout_child 
    orientation: "vertical"
    spacing: "10dp"

    
    MDTopAppBar:
        id: toolbar
        title: 'Lock Application'
        md_bg_color: app.theme_cls.primary_color
        left_action_items: [["menu", lambda x: app.navigation_draw()]]
        right_action_items: [["exit-run", lambda x: app.exit_app()]]
        elevation: 5
        
    MDBoxLayout:
        id: layout_child
        tf_temp: tf_temp
        tf_hum: tf_hum
        
        orientation: "vertical"
        adaptive_height: True
        padding: dp(180)
        spacing: dp(60)
    
        MDTextField:
            id: tf_temp
            mode: "round"
            font_size: '30sp'
            halign: 'right'
            # hint_text: "Enter username"
            helper_text: "temperature °C"
            helper_text_mode: "persistent"
            icon_left: "home-thermometer-outline"
            
            icon_left_color: app.theme_cls.primary_color
            
            pos_hint:{'center_x': 0.5, 'center_y': 0.5}
            size: Window.width - dp(40), "50dp"
            size_hint_x:None
            width:300
            readonly: True
            
        MDTextField:
            id: tf_hum
            mode: "round"
            font_size: '30sp'
            halign: 'right'
            # hint_text: "Enter username"
            helper_text: "hummidity %"
            helper_text_mode: "persistent"
            icon_left: "water-percent"
            
            icon_left_color: app.theme_cls.primary_color
            
            pos_hint:{'center_x': 0.5, 'center_y': 0.5}
            size_hint_x: None
            size: Window.width - dp(40), "50dp"
            width:300
            height: 100
            readonly: True
    

    MDBottomAppBar:
        MDTopAppBar:
            elevation: 1
            # left_action_items: [["coffee", lambda x: app.navigation_draw()]]
            mode: 'end'
            type: 'bottom'
            icon: "lock-open-variant"
            on_action_button: app.lock_cmd()
            
    
"""
