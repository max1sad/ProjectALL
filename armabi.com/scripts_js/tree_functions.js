 // функция для отрисовки дерева, так же если уже существует дерево и получены новые данные, то она перерисовывает
function showStructureTree () {
                /*Очищаем данные модели и подаем в функцию новые данные для отображения. Дожидаясь момента когда очистит данные.*/
                 $('.frmt').data('jstree',false).empty().jstree(allObj.tree_json);
                // очищаем текущую модель дерева
                //$('#frmt').jstree("destroy").empty();
                //$('#frmt').jstree(this.tree);
            }; 
            
 
 /*Функция определения 2 или 1 клик по обьекту совершен, стандартными методами одиночный клик первым вызывает*/
 jQuery.fn.single_double_click = function(single_click_callback, double_click_callback, timeout) {
  return this.each(function(){
    var clicks = 0, self = this;
    jQuery(this).click(function(event){
      clicks++;
      if (clicks == 1) {
        setTimeout(function(){
          if(clicks == 1) {
            single_click_callback.call(self, event);
          } else {
            double_click_callback.call(self, event);
          }
          clicks = 0;
        }, timeout || 200);
      }
    });
  });
};

/*Определяем двойное или одиночное нажатие по блоку div где отображается дерево каталогов.*/
$(".frmt").single_double_click(function (e) {
    console.log(e.target.tagName);
    /*Смотрим что нажали только на элемент дерева, а не просто по блоку где все в списках отображено, иначе если кликнуть мимо, то он вернет путь данного каталога, определяет по элементу списка*/
    if (e.target.tagName === 'A' || e.target.tagName === 'I') {
        /*|| e.target.tagName === 'I'  Это когда на стрелочку раскрытия нажимаем, что должно делаться в это случае? */
        /*Одиночный клик*/
        var tree = $(this).jstree();
        var node = tree.get_node(e.target);
        var pathN = tree.get_path(node).join("/");
       //app.getTree();
        allObj.path_tree = pathN;
        console.log(allObj.path_tree);
    }
}, function (e) {
    console.log(e.target.tagName);
    /*Двойной клик*/
    if (e.target.tagName === 'A' || e.target.tagName === 'I') {
        var tree = $(this).jstree();
        var node = tree.get_node(e.target);
        var pathN = tree.get_path(node).join("/");
        allObj.getTree()

     }
  //$(this).hide()
}); 
