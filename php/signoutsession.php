<?php
session_start();

//echo "<p style='color:white'>Successfully logged out</p>";

session_unset();
session_destroy();

$url = "../html/index.html";
header( "Location: $url" );
?>