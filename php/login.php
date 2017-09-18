
<?php
session_start();
$flag=1;

if(empty($_POST['email'])) {
	echo "Username is required.";
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

    /*$result = pg_query($conn, "SELECT * FROM users");
    while($row = pg_fetch_assoc($result)){

        echo "Name : ".$row['name']."<br>Email : ".$row['email'];
    }*/


    $sql = "SELECT * FROM users WHERE password = $1";
    pg_prepare($conn, "prep", $sql);
    $result = pg_execute($conn, "prep", array($pwd));
    //$stmt = $conn->prepare($sql);

    //$stmt->bind_param('s',$pwd);

    if(pg_result_seek($result, 0)){
        //$stmt->bind_result($name,$mail);
        $row = pg_fetch_assoc($result);
        if($row['email'] == $email){
            $_SESSION['uid']=$row['id'];
            $_SESSION['name']=$row['name'];
            $_SESSION['email']=$row['email'];
            include 'signout.php';
            echo "<h1>Welcome ".$row['name']."</h1>";
        }
        else{
            echo "<center><p style='color:white'>Email or password is wrong</p></center>";
            include "../html/signin.html";
        }
    }
    else {
echo "<center><p style='color:white'>Email or password is wrong</p></center>";
        include "../html/signin.html";
    }
    pg_close($conn);

}

function checkData($d) {
    return trim($d);
}

?>