<?php



if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $value1 = $_POST["id"];
    $value2 = $_POST["date"];
    $value3 = $_POST["id_order"];
    $value4 = $_POST["rating1"];
    $value5 = $_POST["rating2"];
    $value6 = $_POST["rating3"];


$servername = "localhost";
$username = "root";
$password = "123456789";
$dbname = "diplomatiki11";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

// Retrieve values from POST request
$value1 = $_POST['id'];
$value2 = $_POST['date'];
$value3 = $_POST['id_order'];
$value4 = $_POST['rating1'];
$value5 = $_POST['rating2'];
$value6 = $_POST['rating3'];

// Prepare and execute SQL queries
$sql1 = "SELECT id_distributor FROM Distributor WHERE id_distributor=?";
$stmt1 = $conn->prepare($sql1);
$stmt1->bind_param("i", $value1);
$stmt1->execute();
$result1 = $stmt1->get_result();

if ($result1->num_rows == 0) {
  echo "No distributor with this name found!";
} else {
  // Check if order exists
  $sql2 = "SELECT id_aitimatos FROM Aitima WHERE id_aitimatos=?";
  $stmt2 = $conn->prepare($sql2);
  $stmt2->bind_param("i", $value3);
  $stmt2->execute();
  $result2 = $stmt2->get_result();

  if ($result2->num_rows == 0) {
  } else {
    // Check if shift exists
    $sql3 = "SELECT date_shift FROM Shift WHERE date_shift=?";
    $stmt3 = $conn->prepare($sql3);
    $stmt3->bind_param("s", $value2);
    $stmt3->execute();
    $result3 = $stmt3->get_result();

    if ($result3->num_rows == 0) {
      echo "We cannot find the id of that specific order!";
    } else {
      // Insert rating from customer into database
      $sql4 = "SELECT id_rating_costumer FROM RatingFromCostumer WHERE id_rating_costumer=? AND dat_shif_costumer=? AND id_aitimatos_costumer=?";
      $stmt4 = $conn->prepare($sql4);
      $stmt4->bind_param("iss", $result1->fetch_assoc()['id_distributor'], $value2, $value3);
      $stmt4->execute();
      $result4 = $stmt4->get_result();
      
      if ($result4->num_rows > 0) {
        // Rating already exists, ask user to update it
        $sql5 = "UPDATE RatingFromCostumer SET speed=?, accuracy=?, customer_service=? WHERE id_rating_costumer=? AND dat_shif_costumer=? AND id_aitimatos_costumer=?";
        $stmt5 = $conn->prepare($sql5);
        $stmt5->bind_param("iiiiss", $value4, $value5, $value6, $result4->fetch_assoc()['id_rating_costumer'], $value2, $value3);
        if ($stmt5->execute()) {
          echo "Rating updated successfully!";
        } else {
          echo "Failed to update rating " . $conn->error;
        }
      } else {
        // Rating does not exist, insert new rating
        $sql5 = "INSERT INTO RatingFromCostumer (id_rating_costumer, dat_shif_costumer, id_aitimatos_costumer, speed, accuracy, customer_service) VALUES (?, ?, ?, ?, ?, ?)";
        $stmt5 = $conn->prepare($sql5);
        $stmt5->bind_param("issiii",$value1, $value2, $value3, $value4, $value5, $value6);
        if ($stmt5->execute()) {
          echo "Thanks for your rating!";
        } else {
          echo "Failed to insert record into RatingFromCostumer table " . $conn->error;
        }
      }
    }}}} 
      $stmt1->close();
      $stmt2->close();
      $stmt3->close();
      $stmt4->close();
      $stmt5->close();
      $conn->close();
  
?>


