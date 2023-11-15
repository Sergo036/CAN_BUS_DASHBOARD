document.addEventListener("DOMContentLoaded",function(){
    let socket = new WebSocket("ws://candashboard.local:8000")
    let itemValue = document.getElementsByClassName('section-item')
    let Check = document.getElementById('check')
    let AC = document.getElementById('AC')
    let mcp_status = {  "0xAA":"Не удалось выполнить сброс модуля MCP2515",
                        "0xBB":"Не удалось установить скорость чтения на MCP2515",
                        "0xDD":"Не удалось установить нормальный режим работы MCP2515",
                        "0xFF":"Соединение с MCP2515 установленно"}
    let acceptSending = true
    
    function HexToBin(hex){
        return (parseInt(hex)>>>0).toString(2).split('').reverse()
    }

    function showAlert(alertIndex){
        alert(mcp_status[alertIndex])
    }
    socket.onopen = function(e){
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
                    socket.send('get_CanBus_data')
                    break
                case "no_bus_data":
                    acceptSending = false
                    alert('Нет данных с шины CAN. Проверте соединение с CAN')
                    break
                default:
                    let JsonData = JSON.parse(event.data)
                    let keys = Object.keys(JsonData)
                    console.log(keys)
                    switch(keys[0]){
                        case '329':
                            itemValue[0].innerHTML = ((parseInt(JsonData['329']['B1'])*.75)-48)-.75
                            break
                        case '545':
                            itemValue[1].innerHTML = (parseInt(JsonData['545']['B2'])-parseInt(JsonData['545']['B1']))
                            itemValue[2].innerHTML = (parseInt(JsonData['545']['B4']))-48
                            if (HexToBin(JsonData['545']['B0'])[1]==='1'){
                                Check.style.color = 'rgb(211, 94, 15)'
                            }
                            else{
                                Check.style.color = 'rgba(117, 117, 117, 0.692)'
                            }

                            if (HexToBin(JsonData['545']['B5'])[3]==='1'){
                                AC.style.color = 'green'
                            }
                            else{
                                AC.style.color = 'rgba(117, 117, 117, 0.692)'
                            }
                            break
                        }
                break
            }
        }
    }
    window.addEventListener("beforeunload",(e)=>{
        return 'Sure?'
    })
});
