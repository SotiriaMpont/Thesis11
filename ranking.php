<?php
$tableData = ""; // Initialize the table data variable

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $date = $_POST["date"];
  $servername = "localhost";
  $username = "root";
  $password = "123456789";
  $dbname = "diplomatiki11";
  $searchClicked = isset($_POST['search-button']);
  // Create connection
  $conn = new mysqli($servername, $username, $password, $dbname);

  // Check connection
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }

  $query = "SELECT distributor_id, total_rate FROM Total_Score WHERE shift = '$date' ORDER BY total_rate DESC";
  $result = mysqli_query($conn, $query);

  // Check if the query was successful
  if ($result) {
    $rank = 1; // Initialize the rank counter

    while ($row = mysqli_fetch_assoc($result)) {
      $distributor = $row['distributor_id'];
      $totalScore = $row['total_rate'];

      // Build the table row
      $tableData .= "<tr>";
      $tableData .= "<td>{$rank}</td>";
      $tableData .= "<td>{$distributor}</td>";
      $tableData .= "<td>{$totalScore}</td>";
      
      $tableData .= "</tr>";

      $rank++; // Increment the rank counter
    }
    include 'ranking.html';
  } else {
    // Query execution failed
    echo "Error executing the query: " . mysqli_error($conn);
  }

  // Close the database connection
  mysqli_close($conn);
}


?>