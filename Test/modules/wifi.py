def do_connect():
    import network
    from time import sleep
    import machine
    SSID = 'Logistick'
    PSWD = '1234567890'
    sta = network.WLAN(network.STA_IF)
    sta.active(False)
    sleep(.5)
    sta.active(True)
    nets = sta.scan()
    for net in nets:
        net = net[0].decode('utf-8')
        if net == SSID:
            print('Find My SSID')
            sta.connect(SSID,PSWD)
            sta.config(dhcp_hostname='candashboard')
            while not sta.isconnected():
                machine.idle()
            print('Connected!')
            
            return True