var allObj = new Vue({
        //el: '#allObj',
        data: { 
            // открыта форма устройства
            check_form_devices: false,
            // открыта форма информационная безопасность
            check_form_ib: false,
            // ид выбранного устройства
            idDev: '',
            // активный хост
            isActiveHost: '',
            // активный агент
            isActiveAgent: '',
            // открыто ли дополнителньое меню
            isActiveDopMenu:'',
            //выбранный путь в деревен
            path_tree: '',
            // массив файловой системы на основе которого отрисовка
            tree_json: [],
            // массив выбранных объектов файловой системы
            path_remove_del: [],
            // event элемента, на который нажали, нужно для удаления элементов файловой системы
            targ:'',
            
        },
         methods: {
            getTree: function () {

                axios
                    .get('scripts_php/router.php/tree')
                    .then(response => {
                        this.tree_json = JSON.parse(response.data);
                        showStructureTree();
                    });
                    // очищаем текущую модель дерева

                    //alert(this.tree);
            },
             
        },
        
}); 
