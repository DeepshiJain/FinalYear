<?php

session_start();
$flag=1;

if(empty($_POST['name'])) {
    echo "Username is required.";
    $flag = 0;
}
if(empty($_POST['email'])) {
    echo "Email is required.";
    $flag = 0;
}
if(empty($_POST['pwd'])) {
    echo "Passwordn is required.";
    $flag = 0;
}
if($flag == 1){
    include "conn.php";

    $name = checkData($_POST['name']);
    $email = checkData($_POST['email']);
    $pwd = checkData($_POST['pwd']);

    $sql = "INSERT INTO users VALUES(DEFAULT,$1,$2,$3)";
    pg_prepare($conn, "prep", $sql);
    $result = pg_execute($conn, "prep", array($name,$email,$pwd));
    if($result){
        //$_SESSION['uid']=$id;
        $_SESSION['name']=$name;
        $_SESSION['email']=$email;
        include 'signout.php';
        echo "<h4>Account created successfully</h4>";
        echo "<h1>Welcome ".$name."</h1>";

    }
    else {
        echo "<center><p style='color:white'>Something went wrong.Try Again..!!</p></center>";
        include "../html/signup.html";
    }

    pg_close($conn);
}

function checkData($d) {
	return trim($d);
}

?>