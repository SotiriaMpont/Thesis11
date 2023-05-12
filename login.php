<?php


if ($_SERVER['REQUEST_METHOD'] == 'POST') {

$servername = "localhost";
$username = "root";
$password = "123456789";
$dbname = "diplomatiki11";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
  // Get the username and password from the login form
  $username = $_POST['username'];
  $password = $_POST['password'];

  // Debugging: Print out the username and password
 
  // Query the User table to get the user's role
  $stmt = $conn->prepare("SELECT isAdmin, isCustomer, isStore FROM User WHERE username=? AND password=?");
  $stmt->bind_param("ss", $username, $password);
  $stmt->execute();
  $result = $stmt->get_result()->fetch_assoc();

  if ($result) {
    if ($result['isAdmin'] == 1) {
      // Redirect to the broker page if the user is an admin
      header('Location: http://localhost/form_broker.html');
      exit();
    } elseif ($result['isCustomer'] == 1) {
      // Redirect to the customer page if the user is a customer
      header('Location: http://localhost/form_costumer1.html');
      exit();
    } elseif ($result['isStore'] == 1) {
      // Redirect to the store page if the user is a store
      header('Location: http://localhost/form_store.html');
      exit();
    }
  } else {
    
    $stmt = $conn->prepare("SELECT id_distributor FROM Distributor WHERE username_distributor=? AND password_distributor=?");
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result()->fetch_assoc();

    if ($result) {
      // Redirect to the distributor page if the login is successful
      $id_distributor = $result['id_distributor'];
      session_start(); //gia na krataei meta to id 
      $_SESSION['id_distributor'] = $result['id_distributor'];
      error_log('Distributor ID: ' . $id_distributor ); // Write to error log
      header('Location: http://localhost/distributor.html');
      exit();
    } else {
      // Redirect to the login page if the username or password is incorrect
      header('Location: http://localhost/login.html');
      exit();
    }
  }
}



ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>
