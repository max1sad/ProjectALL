    var Devices = new Vue({
        el: '#Devices',
        data: {
            devices_name: ['Имя_хоста_(ip_и_mac_адрес)','Регистрация','Имя_(роль)_в_домене', 'Контр.домена', 'Активность_хоста','Активность_агента'],
            devices: [],
            selectMode: 'single',
            headVariant: 'light',
            comand_arm:'',
            dev: [],
            
            
        },
        methods: {
            
            /*получить данные из БД*/
            getDataDevices: function () {
                allObj.check_form_devices = true;
                axios
                    .get('scripts_php/router.php/devices')
                    .then(response => {
                        console.log(response);
                        this.devices = response.data;
                    });
                    var st = document.getElementById('DevicesAtr');
                    st.style.display='block';
            },
            

            onRowSelected(items) {
                if (items != ""){
                    this.dev = [];
                    this.dev = items;
                    var n = 0;
                    //на вход поступает массив объектов,ключ-значение.
                    var rr = Object.values(this.dev[0]);
                    var id = Object.entries(this.dev[0]);
                    // знаем значение заранее, где будет располагаться ,но если добавятся еще какие либо поля что бы не менять положение, делается церез цикл.
                    for (let i = 0; i < id.length; i += 1) {
                        if (id[i][0] === 'id') {
                            allObj.idDev = id[i][1];
                            console.log(allObj.idDev);
                            n += 1;
                        }
                        if (id[i][0] === 'isActiveHost') {
                            allObj.isActiveHost = id[i][1];
                            console.log(allObj.isActiveHost);
                            n += 1;
                        }
                        if (id[i][0] === 'isActiveAgent') {
                            allObj.isActiveAgent = id[i][1];
                            console.log(allObj.isActiveAgent);
                            n += 1;
                        }
                        if (n === 3) {
                            console.log('exit');
                            break;
                        }
                    }
                    // активируем все элементы если агент активер и хост тоже
                    if (allObj.isActiveAgent === 't' && allObj.isActiveHost === 't') {
                        enableElements("enable_img"); 
                    }
                    //поиск по регулярному значению в строке массива значений
                    //let reg_ip = /ip:[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/;
                    //console.log(reg_ip.exec(rr[0])[0]);
                }else {
                    allObj.idDev = '';
                    allObj.isActiveHost = '';
                    allObj.isActiveAgent = '';
                    disableElements("enable_img");
                    //console.log(allObj.idDev);
                }
                
                
            },
            
            
        },
      mounted() {
          
          //Получаем данные при загрузке страницы, так как это стартовая страница будет.
          this.getDataDevices();
          //this.postCommand();

      },
           
    });
    
// функция которая отслеживаиет событие нажатие мыши. Дальше определяется элемент на который нажали,и происходит скрытие всплывающего меню.
let id_div = document.getElementById('Devices');
id_div.onmousedown = function(e) {
    if (e.which == 3) {
        if (e.target.tagName == 'TD' || e.target.tagName == 'STRONG' || ( e.target.tagName == 'IMG' && e.target.id == 'mn-1')) {
            console.log(e.which);
            showMenuDevices();
            allObj.isActiveDopMenu = 'dop-menu';
            //var st = document.getElementsByClassName("menu-devices")[0];
            //st.style.display='none';
        } 
    }
        
};

        //setInterval(function () {
     //         app.getEvent();
      //        app.getDataDevices();
      //          app.getComandResult();
      //  },5000);
 

