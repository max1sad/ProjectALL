

function enableElements (name_class) {
    var st = document.getElementsByClassName(name_class);
    for (let i = 0; i < st.length; i += 1) {
        st[i].style.pointerEvents='auto';
        st[i].style.filter='grayscale(0)';
    }
     
}
function disableElements (name_class) {
    var st = document.getElementsByClassName(name_class);
    for (let i = 0; i < st.length; i += 1) {
        st[i].style.pointerEvents='none';
        st[i].style.filter='grayscale(1)';
    }
     
}
function modalWindowShow (name_id,disable_block) {
    var st = document.getElementById(name_id);
    st.style.display='block';
    if (disable_block != ''){
        var st = document.getElementById(disable_block);
        st.style.pointerEvents='none';
        disableElements ('pointer-e');
    }
    
}
function modalWindowDisable (name_id,disable_block) {
    var st = document.getElementById(name_id);
    st.style.display='none';
    var st = document.getElementById(disable_block);
    st.style.pointerEvents='auto';
    enableElements ('pointer-e');
}

function modalTextValues (name_id,text_value,id_view,id_table) {
    var st = document.getElementById(name_id);
    if (id_table != '') {
        st.innerHTML=text_value + "<img  src=\"images/Icons/delete2.png\" width=\"25\" height=\"25\" style=\"float:right;\" onclick=\"modalWindowDisable('" + id_view + "','all-f'); remTable('" + id_table + "')\"></img>";
    } else {
        //console.log(text_value+ "<img  src=\"images/Icons/delete2.png\" width=\"25\" height=\"25\" style=\"float:right;\" onclick=\"modalWindowDisable('" + id_view + "','all-f')\"></img>");
        st.innerHTML=text_value + "<img  src=\"images/Icons/delete2.png\" width=\"25\" height=\"25\" style=\"float:right;\" onclick=\"modalWindowDisable('" + id_view + "','all-f');\"></img>";
    }
}
function modalSize (name_id,w_s,h_s,l_p,t_p) {
    var st = document.getElementById(name_id);
    st.style.width = w_s;
    st.style.height = h_s;
    if (l_p != '') {
        st.style.left = l_p;
    }
    if (t_p != '') {
        st.style.top = t_p;
    }
}

/*Возвращает координаты х у нажатия.*/
function getPosition(e){
	var x = y = 0;
 
	if (!e) {
		var e = window.event;
	}
 
	if (e.pageX || e.pageY){
		x = e.pageX;
		y = e.pageY;
	} else if (e.clientX || e.clientY){
		x = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
		y = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
	}
 
	return {x: x, y: y}
};
function showMenuDevices(e){
	var coord = getPosition(e);
	//alert(coord.x + "," + coord.y);
	var ball = document.getElementsByClassName("dop-menu")[0];
	//alert(ball);
      ball.style.left = coord.x + 'px';
      ball.style.top = coord.y + 'px'; 
      ball.style.display = 'block';
      
	//$('#coord-click').html(coord.x + "," + coord.y);
};
// функция которая отслеживаиет событие нажатие мыши. Дальше определяется элемент на который нажали,и происходит скрытие всплывающего меню.
document.addEventListener('click' ,(e) => {
    if (allObj.isActiveDopMenu != '' ) {
        var ball = document.getElementsByClassName("dop-menu")[0];
        ball.style.display = 'none';
        allObj.isActiveDopMenu = '';
    }
});

// получаем events  елемента на который нажали. И смотрим перед нажатием был ли получен элемент, то очяищаем у него класс.
function targetDel () {
    
    var data_r = event.target;
    if (data_r.className != 'inline-color') {
        if (allObj.targ != '') {
            allObj.targ.classList.remove('inline-color');
        }
        data_r.classList.add('inline-color');
        allObj.targ = data_r;
        
    } else {
        data_r.classList.remove('inline-color');
        allObj.targ = '';
    }
    //var del_element = event.target.closest('tr').remove();
}
// удаляем элемент из таблицы, и из глобального массива. Очищаем выбранный путь из дерева
function deleteElements() {
    if (allObj.targ != '') {
        var del_element = allObj.targ.closest('tr').remove();
        var elem_values = allObj.targ.innerText;
        let indexDel = allObj.path_remove_del.indexOf(elem_values);
        if (indexDel !== -1) {
            allObj.path_remove_del.splice(indexDel,1);
        }
        allObj.targ = '';
        console.log(allObj.path_remove_del);
    }
}
// Добавление выбранных элементов на форму при помощи клика.
function addElementsForTable (id_table) {
    if (allObj.targ != '') {
            allObj.targ.classList.remove('inline-color');
        }
    var st = document.getElementById(id_table);
    if (allObj.path_remove_del.indexOf(allObj.path_tree) == -1) {
        st.innerHTML += "<tr onclick=\"targetDel()\"><td>" + allObj.path_tree + "</tr></td>";
        allObj.path_remove_del.push(allObj.path_tree);

    }
};
// полное очищение таблицы в качестве таблицы указываем id, и очищаем массив выбранных ранее элементов.
function remTable (id_table) {
    var st = document.getElementById(id_table);
    st.innerHTML = '';
    allObj.path_remove_del = [];
    
}
/*нажатие правой кнопки мыжи на элемент, смотрим общее нажатие мыши, но потом реагируем на код нажатия*/
/*document.getElementById('t-t').onmousedown = function(e) {
    
    if (e.which == 3) {
    alert('ok');
    }
        
}*/

