<?php
class File  {
    public $path_file = "t.txt";
    
    function fileWrite ($msg) {
        $fd = fopen("t.txt",'a+') or die("Error");
        fwrite($fd,"$msg");
        fclose($fd);
    }
}
?>
