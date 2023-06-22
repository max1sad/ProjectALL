var policyM = new Vue({
        el: '#policyM',
        data: { 
            tree: [],
            path_obj:'',
            // аудит ресурсов
            // массив с отмеченными свойствами
            marked_audit_yes:[],
            // массив всевозможных свойств 
            all_properties:[{text:'o'},{text:'x'},{text:'u'},{text:'d'},{text:'n'},{text:'a'},{text:'r'},{text:'m'},
                {text:'c'},{text:'y'},{text:'Все'}],
            marked_audit_no: ["o"],  
            all_checked_no: false,
            all_checked_yes: false,
            //говорим что по умолчанию будет отображаться
            audit_visible:'Пользователи',
            //Массив возможных отображений
            audit_type_sub:[{text: 'Пользователи'},{text: 'Группы'},{text: 'Остальные'}],
            audit_visible_user:'root',
            audit_user_sub:[{text: 'root'},{text :'max'},{text:'--Доменные пользователи--',disabled:true},{text :'test'}],
            // аудит ресурсов exit
            // Дискретационные атрибуты
            discrete_users: 'root',
            get_discrete_users: [{text: 'root'},{text :'max'},{text:'--Доменные пользователи--',disabled:true},{text :'test'}],
            discrete_groups: 'root',
            get_discrete_groups: [{text: 'root'},{text :'max'},{text:'--Доменные группы--',disabled:true},{text :'test'}],
            
            get_discrete_bit: ['SUID-бит'],
            all_discrete_bit_arr: [{text: 'SUID-бит'},{text: 'SGID-бит'},{text: 'Sticky-бит'}],
            
            get_owner: ['Чтение'],
            get_group: ['Запись'],
            get_other: ['Выполнение'],
            all_discrete_dostup: [{text: 'Чтение',},{text: 'Запись'},{text: 'Выполнение'}],
            
            install_recursiv: null,
            
            all_acl_subject: [{text: 'Маска'},{text: 'Пользователи'},{text: 'Группы'},{text: 'Остальные'}],
            get_acl_subject: 'Маска',
            
            default_acl_sub_user: 'root',
            get_acl_sub_user: [{text: 'root'},{text :'max'},{text:'--Доменные пользователи--',disabled:true},{text :'test'}],
            
            d_acl_sub_show: false,
            d_acl_sub_disable: false,
            d_acl_check_sub: false,
            
            acl_dostup:[{text: 'Чтение',},{text: 'Запись'},{text: 'Выполнение'},{text: 'По умолчанию'}],
            get_acl_dostup:[],
            
            d_acl_recursiv: null,
            
            get_acl_table:[{'Субъект':'МАСКА','Права':'rwx',delAccess:'<button>удалить</button>'},{'Субъект':'МАСКА','Права':'rw',delAccess:'<button>удалить</button>'},
                {'Субъект':'МАСКА','Права':'rwx',delAccess:'<button>удалить</button>'},{'Субъект':'МАСКА','Права':'rw',delAccess:'<button>удалить</button>'},
                {'Субъект':'МАСКА','Права':'rwx',delAccess:'<button>удалить</button>'},{'Субъект':'МАСКА','Права':'rw',delAccess:'<button>удалить</button>'},
                {'Субъект':'МАСКА','Права':'rwx',delAccess:'<button>удалить</button>'},{'Субъект':'МАСКА','Права':'rw',delAccess:'<button>удалить</button>'},
                {'Субъект':'МАСКА','Права':'rwx',delAccess:'<button>удалить</button>'},{'Субъект':'МАСКА','Права':'rw',delAccess:'<button>удалить</button>'},
                {'Субъект':'МАСКА','Права':'rwx',delAccess:'<button>удалить</button>'},{'Субъект':'МАСКА','Права':'rw',delAccess:'<button>удалить</button>'},
                {'Субъект':'МАСКА','Права':'rwx',delAccess:'<button>удалить</button>'},{'Субъект':'МАСКА','Права':'rw',delAccess:'<button>удалить</button>'}
            ],
            // свойства таблицы
            selectMode: 'single',
            headVariant: 'light',
            //***
            // переменные для активности вкладок (Дискретационные, аудит, мандатные атрибуты). Изменяются через функцию isActiveForms
            isActiveDiscrete: false,
            isActiveAudit:false,
            isActiveMandate:false,
        },
         methods: {
            // функция принимает на вход название окна, которому принадлежит переменная отвечающая за активность окна. 
            isActiveForms: function (name_forms) {
                if (name_forms === 'isActiveDiscrete') {
                    this.isActiveDiscrete = true;
                    this.isActiveAudit = false;
                    this.isActiveMandate = false;
                }
                if (name_forms === 'isActiveAudit') {
                    this.isActiveAudit = true;
                    this.isActiveDiscrete = false;
                    this.isActiveMandate = false;
                }
                if (name_forms === 'isActiveMandate') {
                    this.isActiveMandate = true;
                    this.isActiveDiscrete = false;
                    this.isActiveAudit = false;
                }
            }, 
            // Проверка активности элементов, в зависимости что выбрано в типе субъекта.
            checkSubiectActive: function () {
                if (this.d_acl_check_sub) {
                    this.d_acl_sub_disable = false;
                }else if (this.d_acl_check_sub == false && this.d_acl_sub_show == true){this.d_acl_sub_disable = true;}
                if (this.d_acl_check_sub == false && this.d_acl_sub_show == false && this.get_acl_subject != 'Маска') {
                    this.d_acl_sub_show = true;
                    this.d_acl_check_sub = true;
                }else if (this.d_acl_check_sub == false && this.d_acl_sub_show == true && this.get_acl_subject === 'Маска') {
                    this.d_acl_sub_disable = true;
                } 
                if (this.get_acl_subject === 'Маска'){
                    this.d_acl_sub_disable = false;
                    this.d_acl_sub_show = false;
                    this.d_acl_check_sub = false;
                }
            },
           // выделить все сворйства для отрицательного результата         
            selectionAllOptionsNo: function (checked) {
                if(checked.includes('Все')) {
                    let i = 0;
                    while (i < (this.all_properties.length-1)){
                        this.marked_audit_no.push(this.all_properties[i]['text']); 
                        i = i + 1;
                    } 
                    this.all_checked_no = true;
                }
                if ( this.marked_audit_no.includes('Все') === false && this.all_checked_no === true ){
                    this.marked_audit_no = [];
                    this.all_checked_no = false;
                }
            },
            // выделить все сворйства для положительного результата
            selectionAllOptionsYes: function (checked) {
                if(checked.includes('Все')) {
                    let i = 0;
                    while (i < (this.all_properties.length-1)){
                        this.marked_audit_yes.push(this.all_properties[i]['text']); 
                        i = i + 1;
                    } 
                    this.all_checked_yes = true;
                }
                if ( this.marked_audit_yes.includes('Все') === false && this.all_checked_yes === true ){
                    this.marked_audit_yes = [];
                    this.all_checked_yes = false;
                }
            },
         // закрытие метода объявления функций;   
        },
        
        
});




