content = """\
        <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>CANBUS</title>
</head>
<style>
    *{
        margin: 0;
        padding: 0;
    }
    body{
        
        box-sizing: border-box;
        overflow-x: hidden;
        overflow-y: scroll;
        font-family: sans-serif;
        background-color: rgb(33,33,33);
    }
    .container{
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 348px;
        background-color: rgb(33, 33, 33);
    }
    .section{
        display: flex;
        justify-content: space-around;
        width: 100%;
        height: 48%;
    }
    .section-element{
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        width: 48%;
        height: 98%;
        background-color: rgb(45, 45, 45);
    }
    .section-label,.rotate{
        
        font-size: 22px;
        color: rgba(117, 117, 117, 0.692);
    }
    .section-item{
        
        font-size: 62px;
        
        color:rgba(240, 240, 240, 0.692) ;
        
    }
    .rotate{
        display: none;
    }
    @media only screen and (max-width: 600px){
        .container{
            display: none;
        }
        .rotate{
            display: flex;
            margin-top: 40px;
            width: 100%;
            height: 30px;
            align-items: center;
            justify-content: center;
        }
    }
   
</style>
<body>
    <h1 class="rotate">Поверните ваше устройство</h1>
    <div class="container" >
        <div class="section" >
            <div class="section-element">
                <h3 class="section-label">Температура ОЖ</h3>
                <h1 class="section-item"></h1>
            </div>
            <div class="section-element">
                <h3 class="section-label">Расход топлива l/100km</h3>
                <h1 class="section-item"></h1>
            </div>
        </div>
        <div class="section">
            <div class="section-element">
                <h3 class="section-label">Температура масла</h3>
                <h1 class="section-item"></h1>
            </div>
            <div class="section-element">
                <div class="element-item">
                    <h3 class="section-label" id="check">CHECK</h3>
                </div>
                <div class="element-item">
                    <h3 class="section-label" id="AC">A/C</h3>
                </div>
            </div>
        </div>
    </div>
    <script>
        document.addEventListener("DOMContentLoaded",function(){
            let socket = new WebSocket("ws://candashboard.local:8000")
            let itemValue = document.getElementsByClassName('section-item')
            let mcp_status = {  "0xAA":"Не удалось выполнить сброс модуля MCP2515",
                                "0xBB":"Не удалось установить скорость чтения на MCP2515",
                                "0xDD":"Не удалось установить нормальный режим работы MCP2515",
                                "0xFF":"Соединение с MCP2515 установленно"}
            let acceptSending = true
            
            function showAlert(alertIndex){
                alert(mcp_status[alertIndex])
            }
            socket.onopen = function(e){
                function get_CanBus_data(){
                    if (acceptSending===true){
                        socket.send('get_CanBus_data')
                    }
                    else{
                        return
                    }
                }
                socket.send('get_mcp_status')
                socket.onmessage = function(event){
                    switch (event.data){
                        case "0xAA":
                            showAlert(event.data)
                            socket.send('close_ws')
                            break
                        case "0xBB":
                            showAlert(event.data)
                            socket.send('close_ws')
                            break
                        case "0xDD":
                            showAlert(event.data)
                            socket.send('close_ws')
                            break
                        case "0xFF":
                            showAlert(event.data)
                            let myInterval = setInterval(get_CanBus_data,500)
                            break
                        case "no_bus_data":
                            acceptSending = false
                            alert('Нет данных с шины CAN. Проверте соединение с CAN')
                            break
                        default:
                            console.log(event.data)
                            break
                    }
                }
            }
            });
    </script>
    <script src="main.js"></script>
</body>
</html>
            """