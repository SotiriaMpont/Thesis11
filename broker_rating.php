<?php
$stmt3 = null;
$stmt4 = null;
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $value1 = $_POST["id"];
    $value2 = $_POST["date"];
    $value3 = $_POST["id_order"];
    $value4 = $_POST["rating1"];
    $value5 = $_POST["rating2"];
    $value6= $_POST["rating3"];


// Connect to database
$servername = "localhost";
$username = "root";
$password = "123456789";
$dbname = "diplomatiki11";

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Select distributor with given ID
$sql1 = "SELECT id_distributor FROM Distributor WHERE id_distributor=?";
$stmt1 = $conn->prepare($sql1);
$stmt1->bind_param("i", $value1);
$stmt1->execute();
$result1 = $stmt1->get_result()->fetch_all(MYSQLI_ASSOC);

if (count($result1) == 0) {
    echo "No distributor with this id found!";
} else {
    $distributor_id = $result1[0]['id_distributor'];

    $sql0 = "SELECT * FROM Aitima WHERE id_distr=? AND id_aitimatos=?";
    $stmt0 = $conn->prepare($sql0);
    $stmt0->bind_param("is", $distributor_id, $value3);
    $stmt0->execute();
    $result0 = $stmt0->get_result()->fetch_all(MYSQLI_ASSOC);

    if (count($result0) == 0) {
        echo "Distributor has not been assigned the request!";
        exit();
    } else {
        // Check if rating already exists
        $sql2 = "SELECT * FROM RatingFromBroker WHERE id_di=? AND dat_shift=? AND id_aitim=?";
        $stmt2 = $conn->prepare($sql2);
        $stmt2->bind_param("iss", $distributor_id, $value2, $value3);
        $stmt2->execute();
        $result2 = $stmt2->get_result()->fetch_all(MYSQLI_ASSOC);

        if (count($result2) > 0) {

            // update old rating and insert new rating
            $sql3 = "UPDATE RatingFromBroker SET speed=?, accuracy=?, customer_service=? WHERE id_di=? AND dat_shift=? AND id_aitim=?";
            $stmt3 = $conn->prepare($sql3);
            $stmt3->bind_param("iiiiss", $value4, $value5, $value6, $distributor_id, $value2, $value3);
            $stmt3->execute();
            $stmt4 = null;
            echo "Your rating is updated !";
            
        } else {
            // Insert rating into table
            $sql4 = "INSERT INTO RatingFromBroker (id_di, dat_shift, id_aitim, speed,accuracy,customer_service) VALUES (?, ?, ?, ?,?, ?)";
            $stmt4 = $conn->prepare($sql4);
            $stmt4->bind_param("issiii", $distributor_id, $value2, $value3, $value4,$value5,$value6);
            $stmt4->execute();
            echo "Thanks for you rating! ";
        }


        } } }


?>