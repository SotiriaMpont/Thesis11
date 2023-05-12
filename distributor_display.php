<?php

$servername = "localhost";
$username = "root";
$password = "123456789";
$dbname = "diplomatiki11";

// Start the session and get the distributor ID
session_start();

if (isset($_SESSION['id_distributor'])) {
    $id_distributor = $_SESSION['id_distributor'];
} else {
    error_log("distributor_id is not set in the session");
    exit;
}

// Get the shift date from the GET parameters
if (isset($_GET['date'])) {
    $date = $_GET['date'];
} else {
    error_log("date is not set in the GET parameters");
    exit;
}

error_log("date: $date, distributor_id: $id_distributor");

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Execute the SQL query
$sql = "SELECT * FROM Total_Score WHERE shift = '$date' AND distributor_id='$id_distributor'";

$result = mysqli_query($conn, $sql);

if ($result !== false) {
    // Get the total score value
    $row = mysqli_fetch_assoc($result);
    if ($row !== null) {
        $total_score = $row['total_rate'];
        $total_rate_costumer = $row['total_rate_costumer'];
        $total_rate_store = $row['total_rate_store'];
        $total_rate_broker = $row['total_rate_broker'];
        $total_rate_metrics = $row['metrics_rate'];

        include 'distributor.html';
        error_log("Total rate metrics: $total_rate_metrics");
    } else {
        error_log("No rows returned from the query");
    }
} else {
    error_log("Error executing query: " . mysqli_error($conn));
}

// Close the database connection
mysqli_close($conn);

?>