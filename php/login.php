
<?php
session_start();
$flag=1;

if(empty($_POST['email'])) {
	echo "Username is required.<br/>";
	$flag=0;
}
if(empty($_POST['pwd'])) {
	echo "Password is required.";
	$flag=0;
}
if($flag==1){
    include "conn.php";

    $email = $_POST['email'];
    $pwd = $_POST['pwd'];

    $email = checkData($email);
    $pwd = checkData($pwd);

    $sql = "SELECT * FROM user WHERE password LIKE ?";
}

function checkData($d) {
    return trim($d);
}

?>