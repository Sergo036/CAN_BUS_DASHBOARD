
import json

from microWebSrv import MicroWebSrv
from modules import connect_mcp2515,create_data_list,do_connect

@MicroWebSrv.route('/')
@MicroWebSrv.route('/style.css')
@MicroWebSrv.route('/main.js')
def _httpHandlerTestGet(httpClient, httpResponse) :
    path = httpClient.GetRequestPath()
    if '.css' in path:
        httpResponse.WriteResponseFile('/www/style.css', contentType='text/css', headers=None)
    elif '.js' in path:
        httpResponse.WriteResponseFile('/www/main.js', contentType='application/javascript', headers=None)
    else:
        httpResponse.WriteResponseFile('/www/index.html', contentType='text/html', headers=None)


     
def _streamData(webSocket, httpClient):
    webSocket.RecvTextCallback = _send_data
    webSocket.ClosedCallback = _closedStream
    
    
def _closedStream(webSocket):
     print('Close WS')
     webSocket.Close()

def _send_data(webSocket,msg):
    if 'get_mcp_status' in msg:
        webSocket.SendText(connect_mcp2515())
    elif 'CanBus' in msg:
        while True:
            data = create_data_list()
            if data:
                
                webSocket.SendText(json.dumps(data))
            

    else:
        _closedStream(webSocket)

if do_connect():
    srv = MicroWebSrv(port=8000)
    srv.MaxWebSocketRecvLen     = 1025
    srv.WebSocketThreaded		= True
    srv.AcceptWebSocketCallback = _streamData
    srv.Start()




    













           
    
            
        





