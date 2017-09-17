
<?php
session_start();
$flag=1;
         916
76253    709
66017    848
31644    130
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