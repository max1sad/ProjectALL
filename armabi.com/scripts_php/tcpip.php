<?php
error_reporting(E_ALL);
//require_once('file_write.php');
//set_time_limit(0);

function test($msg) {
//$msg .= "123";
return $msg;
}
    
    
function tcpWriteAndRead($msg) {


/* Получаем порт сервиса WWW. */
    #$service_port = getservbyname('www', 'tcp');
    $service_port='40050';
    /* Получаем IP-адрес целевого хоста. */
    $address = gethostbyname('192.168.99.21');

    /* Создаём сокет TCP/IP. */
    $socket = socket_create(AF_INET, SOCK_STREAM,SOL_TCP);

    if ($socket === true) {
        echo "Не удалось выполнить socket_create(): причина: " . socket_strerror(socket_last_error()) . "\n";
    } 
    /* выполняем соединение, пока не будет установлен конект.*/
    #do {
        $result = socket_connect($socket, $address, $service_port);
        
    #} while ($result == false);
    $file = new File();
    #$file->fileWrite("5");
    $code_comm = '00000000';
    $leng = strlen($msg);
    
    $code_comm .= $leng;
    $res_msg = substr($code_comm,2,strlen($code_comm));
    $res_msg .= $msg;
    $file->fileWrite($res_msg);
    $che = socket_write($socket, $res_msg);
    $out = '';
    while ($out = socket_read($socket, 2048)) {
    //echo "result ";
    //echo $out;
    socket_close($socket);
    return $out;
    }
    
}

/*if ($result === false) {
    echo "Не удалось выполнить socket_connect().\nПричина: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
} else {
    $in = '12345 45335 35';
    $che = socket_write($socket, $in);
    echo "1- $che.\n";
}*/

function tcpWrite ($msg) {
    $che = socket_write($socket, $msg);
    socket_close($socket);
}
?>
