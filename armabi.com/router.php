<?php

require_once('file_write.php');

require_once('tcpip.php');

/* глобальные переменные*/
$result_command = '1';

$file = new File();

// Маршруты
// [маршрут => функция которая будет вызвана]
$routes = [
    // срабатывает при вызове корня или /router.php
    '/' => 'hello',
    // срабатывает при вызове /event или /router.php/event
    '/event' => 'getEvent',
    // срабатывает при вызове /devices или /router.php/devices
    '/devices' => 'getDevices',
    // срабатывание при пост запросе /comand 
    '/comand' => 'postComand',
    '/arm' => 'getArm',
    '/tree' => 'getStructureTree',

];
 
$connect_data = "host=192.168.99.58 port=5445 dbname=dbarmabi user=armabi password=12345678";

$db_connect = pg_connect($connect_data);
if (!$db_connect) {
    echo "notFound";
}
//sleep(5);
    //$sql = "select id, \"alertMsg\" from alerts order by id desc;";

    //$res = pg_query($sql);
    //$resul = pg_fetch_all($res);

//while ($row = pg_fetch_array($res)) {
//echo "{$row['id']} -- {$row['alertMsg']}";
//echo "<br>";
//}
function sqlResult($sql) {

       $res = pg_query($sql);
       $resul = pg_fetch_all($res); 

    return $resul;

}

   //echo json_encode($resul);

// возвращает путь запроса
// вырезает router.php из пути
function getRequestPath() {
    #if ($_SERVER['REQUEST_METHOD'] == "GET") {
    $path = $_SERVER['REQUEST_URI'];
    global $file;
    $file->fileWrite($path);
    return '/' . ltrim(str_replace('/armabi.com/router.php', '', $path), '/');
    #}
}

// наш роутер, в который передаются маршруты и запрашиваемый путь
// возвращает функцию если маршшрут совпал с путем
// иначе возвращает функцию notFound
function getMethod(array $routes, $path) {
    global $file;
    // перебор всех маршрутов
    foreach ($routes as $route => $method) {
        // если маршрут сопадает с путем, возвращаем функцию
        if ($path === $route) {
            $file->fileWrite($method);
            return $method;
        }
    }

    return 'notFound';
}

function structurArm($ar_arm) {
    $new_arr = [];
    $arr_t = [];
    #sleep(5);
    foreach($ar_arm as $row){

        $decsr = "<strong>".$row['hostName']."<br>ip:".$row['ipAddr']."<br>"."mac: ".$row['macAddr']."</strong>";
        $new_arr['hostName'] = $decsr;
        if ($row['isConfirm'] == "t"){
            $new_arr['isConfirm'] = '<img src="check2.png" id="mn-1"></img>';
        } else {
            $new_arr['isConfirm'] = '<img src="fail.png" id="mn-1"></img>';
        }
        $new_arr['domainName'] = $row['domainName'];
        $new_arr['description'] = $row['description'];
        if ($row['isDomainContr'] == "1"){
            $new_arr['isDomainContr'] = '<img src="check2.png" id="mn-1"></img>';
        } else {
            $new_arr['isDomainContr'] = $row['isDomainContr'];
        }
        if ($row['isActiveHost'] == "t"){
            $new_arr['isActiveHost'] = '<img src="check2.png" id="mn-1"></img>';
        } else {
            $new_arr['isActiveHost'] = '<img src="fail.png" id="mn-1"></img>';
        }
        if ($row['isActiveAgent'] == "t"){
            $new_arr['isActiveAgent'] = '<img src="check2.png" id="mn-1"></img>';
        } else {
            $new_arr['isActiveAgent'] = '<img src="fail.png" id="mn-1"></img>';
        }
        $arr_t[] =  $new_arr;
    }
    //var_dump($arr_t);
    //file_put_contents('t.txt', $arr_t);
    return $arr_t;
}
function getStructureTree(){
$outData = file_get_contents("tree.json");
return json_encode($outData);
}

// функция для корня
function hello() {
    $sql = "select \"hostName\",\"ipAddr\",\"macAddr\", \"isConfirm\",\"domainName\",description,\"isDomainContr\",\"isActiveHost\",\"isActiveAgent\" from devices  ;";
    $result = sqlResult($sql);
    $new_arr = [];
    $arr_t = [];
    $count = 0;
    foreach($result as $row){
    
    $decsr = "<strong>".$row['hostName']."<br>ip:".$row['ipAddr']."<br>".$row['macAddr']."</strong>";
    $new_arr['hostName'] = $decsr;
    if ($row['isConfirm'] == "t"){
        $new_arr['isConfirm'] = '<b-img src="check2.png"></b-img>';
    }
    else {
        $new_arr['isConfirm'] = '<b-img src="fail.png"></b-img>';
    }
    $new_arr['domainName'] = $row['domainName'];
    $new_arr['description'] = $row['description'];
    $new_arr['isDomainContr'] = $row['isDomainContr'];
    $new_arr['isActiveHost'] = $row['isActiveHost'];
    $new_arr['isActiveAgent'] = $row['isActiveAgent'];
    $arr_t[] =  $new_arr;
    }
    #var_dump($arr_t);
    //file_put_contents('t.txt', $count);
    //return json_encode($arr_t);
    //return 'Hello, world!';
}

// функция для страницы "/event"
function getEvent() {
    #$sql = "select id, \"alertMsg\" from alerts order by id desc;";
    $sql = "select \"hostName\",timestamp, \"eventLvl\", \"user\",\"alertMsg\", \"fullLog\" from alerts order by id desc limit 20;";
    $result = sqlResult($sql);
    return json_encode($result);
}

// функция для страницы "/devices"
function getDevices() {
global  $file;
    $file->fileWrite("yes");
    #$sql = "select id, \"hostName\" from \"devices\"";
    $sql = "select \"hostName\",\"ipAddr\",\"macAddr\", \"isConfirm\",\"domainName\",description,\"isDomainContr\",\"isActiveHost\",\"isActiveAgent\" from devices  ;";
    $result = sqlResult($sql);
#var_dump($result);

    $result = structurArm($result);
    
    return json_encode($result);
}

function getJson() {
    #$sql = "select id, \"hostName\" from \"devices\"";
    $sql = "select data from json_test1;";
    $result = sqlResult($sql);
#var_dump($result);
    //$file->fileWrite();
    
    
    return $result;
}
// Функция для получения данных от клиента отправленных на страницу /comand
function postComand() {
    // функция для получения данных из входящего запроса
    $txtt = file_get_contents('php://input').PHP_EOL;
    $ip_clienta = $_SERVER['REMOTE_ADDR'];
    if ($ip_clienta == "127.0.0.1") {
        $ip_clienta = "192.168.99.58";
    } 
    // данные в json, что бы с ними работать нужно декодировать их
    #$txtt = json_decode($txtt,true);
    global $result_command;
    global $file;
    $res = getJson();
    #$result_command = tcpWriteAndRead($txtt);
    $txtt .= $ip_clienta;
    #$t = json_decode(json_encode($res),true);

    #var_dump($res[0]['data']);
    #$file->fileWrite($res[0]['data']); 
    $file->fileWrite("[".$res[3]['data']."]");
     #"["+$res[0]['data']+"]";
    return json_encode("[".$res[3]['data']."]");
    #return json_encode($result_command);
    
    #file_put_contents('t.txt',$txtt['txt']);

}


// Роутер
// получаем путь запроса
$path = getRequestPath();
//file_put_contents('t.txt',"$path");
//echo $path;
// получаем функцию обработчик
$method = getMethod($routes, $path);
// отдаем данные клиенту
echo $method(); 

?>
