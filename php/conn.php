<?php

    // $appName = $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    $str = "host=localhost port=5432 dbname=movieDB user=postgres password=deepshi";

    $conn = pg_connect($str);
    if(!$conn){
        die("connection failed");
         echo"hello unsuccessful";
    }
    else {
     echo"hello successful";
    }
?>