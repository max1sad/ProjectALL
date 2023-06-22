<html>

<head>


    <meta charset="UTF-8">
    <title>АРМ АБИ</title>
    <!-- подключаем библиотеки для элементов vue js -->
    <link type="text/css" rel="stylesheet" href="library_css/vue_css/bootstrap.min.css" />
    <link type="text/css" rel="stylesheet" href="library_css/vue_css/bootstrap-vue.min.css" />
    
    <script src="library_js/vue_js/vue.js"></script>
    <script src="library_js/vue_js/bootstrap-vue.min.js"></script>
    <!-- для взаимодействия с API -->
    <script src="library_js/axios.min.js"></script>
    <!-- для отрисовки дерева каталогов -->
    <link rel="stylesheet" href="library_css/tree_css/style.min.css" />
    <script src="library_js/tree_js/jquery.min.js"></script>
    <script src="library_js/tree_js/jstree.min.js"></script>
    
    <link rel="stylesheet" href="scripts_css/menu_vertikal.css" />
	<link rel="stylesheet" href="scripts_css/menu_schapka.css" />
	<link rel="stylesheet" href="scripts_css/modal_window.css" />
	<link rel="stylesheet" href="scripts_css/css_devices.css" />
	
  <style>

        body{
        min-width:1000px;
        min-height:800px;
        /*настраиваем шрифт*/
        font-family: Arial, Helvetica, sans-serif;
        }

        /*общие настройки сетки*/
        .grid {
        height: 100%;
        min-width:920px;
        /*рисуем зелёные рамки*/
        
        /*подключаем сетку*/
        display: grid;
        margin-left: auto;
        /*формируем по 4 одинаковых строки и столбца*/
        grid-template-columns: repeat(9, 10%);
        grid-template-rows: repeat(12, 70px);
        } 

        /*внешний вид ячеек*/
        .grid > * {
        /*фоновый цвет*/
        background-color: #ffbf94;
        /*скругление углов*/
        border-radius: 5px;
        /*расстояние от одной границы ячейки до другой*/
        margin: 1px;
        }

        .oblast-3 {
        grid-row-start: 13;
        grid-row-end: 14;
        grid-column-start: 2;
        grid-column-end: 11;
            
        }
        
        .oblast-1 {
        overflow-y: auto;
        grid-row-start: 2;
        grid-row-end: 13;
        grid-column-start: 2;
        grid-column-end: 10;
        }
        .oblast-2 {
        grid-row-start: 2;
        grid-row-end: 13;
        grid-column-start: 10;
        grid-column-end: 11;

        }
        .oblast-0 {
        grid-row-start: 1;
        grid-column-start: 2;
            grid-column-end: 11;
        }
        .oblast-4 {
        grid-row-start: 1;
        grid-row-end: 14;
        
        }
        
        .enable_img {
            pointer-events: none;
            filter: grayscale(1);
        }

        /*Для всплывающих подсказов стиль задается*/
        [data-hint] {
        position: relative;
        cursor: hint;
        }

        [data-hint]::after {
            opacity: 0;
            width: max-content;
            color: #FFFFFF;
            background-color: rgba(0,0,0,.7);
            border-radius: 6px;
            padding: 10px;
            content: attr(data-hint);
            font-size: 12px;
            font-weight: 400;
            line-height: 1em;
            position: absolute;
            top: -5px;
            left: 50%;
            transform: translate(-50%, -100%);
            pointer-events: none;
            transition: opacity 0.2s;
        }

        [data-hint]:hover::after {
            opacity: 1;
        }

  </style>
</head>

<body oncontextmenu="return false;">

<!--<div id="allObj"></div>-->
  <!-- создаём контейнер, который будет отвечать за нашу сетку -->
  <div class="grid" id="all-f">
    <!-- и создаём вложенные элементы -->
	<div class="oblast-0">
				<div class="navbar">
					<div class="dropdown">
						<button class="dropbtn">Файл
							<i class="fa fa-caret-down"></i>
						</button>
						<div class="dropdown-content">
							<a href="#">Резервная копия БД</a>
							<a href="#">Восстановление БД</a>
							<a href="#">Правила РД</a>
							<a href="#">Отчуждаемые МНИ</a>
							<a href="#">Планировщик задач</a>
						</div>
					</div>
					
					<div class="dropdown">
						<button class="dropbtn">Настройки
							<i class="fa fa-caret-down"></i>
						</button>
						<div class="dropdown-content">
							<a href="#">Параметры</a>
						</div>
					</div>
					<a href="#">Справка</a>
				</div>


	</div>
	
    <div class="oblast-1">Основное окно
        

        <div class="data-forms" id="Devices" style="display:block">
            <?php include('template/devices.php');?>
        
        </div>
        <div class="data-forms" id="Av" style="display:none">
           <h1>forms update </h1>
        
        </div>
    </div>
    
    <div class="oblast-2">Списко доменов</div>
    <div class="oblast-3" id="RR">
        <div class="data-forms" id="DevicesAtr" style="display:none;">
            <?php include('template/devices_atr.php');?>
        </div>
        
        <div class="data-forms" id="AvAtr" style="display:none;pointer-events:none;">
            <h1> test data </h1>
        </div>

	</div>
	<div class="oblast-4">
			<div class="side-menu">
				<div class="side-menu-buttons"> 
					<a href="#link" class="side-menu-item" onclick="openTab(event,'Devices');Devices.getDataDevices();">
						<div class="side-menu-item-icon">
							<img src="images/Icons/_dev.png" width="48" height="48"></img>
						</div>
						<div class="side-menu-hover">Устройства</div>
					</a> 
					<a href="#link" class="side-menu-item">
						<div class="side-menu-item-icon">
							<img src="images/Icons/_users.png" width="48" height="48"></img>
						</div>
						<div class="side-menu-hover">Пользователи</div>
					</a> 
					<a href="#link" class="side-menu-item svg-icon-anim">
						<div class="side-menu-item-icon">
							<img src="images/Icons/_tests.png" width="48" height="48"></img>
						</div>
						<div class="side-menu-hover">Тестирвоание СЗИ</div>
					</a> 
					<a href="#link" class="side-menu-item">
						<div class="side-menu-item-icon">
							<img src="images/Icons/_ic.png" width="48" height="48"></img>
						</div>
						<div class="side-menu-hover">Контроль целостности</div>
					</a> 
					<a href="#link" class="side-menu-item">
						<div class="side-menu-item-icon">
							<img src="images/Icons/_av2.png" width="48" height="48"></img>
						</div>
						<div class="side-menu-hover">Антивирусная проверка</div>
					</a> 
					<a href="#link" class="side-menu-item" onclick="openTab(event, 'Av');">
						<div class="side-menu-item-icon">
							<img src="images/Icons/_nsd.png" width="48" height="48"></img>
						</div>
						<div class="side-menu-hover">События ИБ</div>
					</a> 
					<a href="#link" class="side-menu-item">
						<div class="side-menu-item-icon">
							<img src="images/Icons/_nsd_ext.png" width="48" height="48"></img>
						</div>
						<div class="side-menu-hover">Внешние события ИБ</div>
					</a> 
				</div>
				
			</div>
	</div>

  </div>
  
  <div class="dop-menu">
        <?php include('template/devices_atr_modal.php');?>
  </div>
  
    <div id="p-m">
        <?php include('template/policy_management.php');?>
    </div>
    <div class="modal-view" id="run-proc">
        <div class="grid-modal">
            <div class="g-m-o-1">
                <p id="header-p">Заголовок из функции</p>
            
            </div>
            <div class="g-m-o-2" id="t-t"></div>
        </div>
    </div>
    <div class="modal-view" id="delete-obj">
        <div class="grid-modal">
            <div class="g-m-o-1">
                <p id="header-p-d">Заголовок из функции</p>
            
            </div>
            <div class="g-m-o-2">
                <?php include('template/garanteed_removal.php');?>
                
            </div>
        </div>
    </div>
</body>

<script src="scripts_js/global_parameters.js"></script>
<script src="scripts_js/global_function.js"></script>

<script src="scripts_js/devices.js"></script>
<script src="scripts_js/policy_management.js"></script>
<script src="scripts_js/tree_functions.js"></script>

<script src="scripts_js/update_forms.js"></script>


</html>
