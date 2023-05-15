<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Establish a database connection
    $conn = mysqli_connect("localhost", "root", "123456789", "diplomatiki11");

    // Check for connection errors
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

    // Get the weights from the form
    $weight1_customer = $_POST['cat1_metric1_weight'];
    $weight2_customer = $_POST['cat1_metric2_weight'];
    $weight3_customer = $_POST['cat1_metric3_weight'];
    $weight1_store = $_POST['cat2_metric1_weight'];
    $weight2_store = $_POST['cat2_metric2_weight'];
    $weight3_store = $_POST['cat2_metric3_weight'];
    $weight1_broker = $_POST['cat3_metric1_weight'];
    $weight2_broker = $_POST['cat3_metric2_weight'];
    $weight3_broker = $_POST['cat3_metric3_weight'];
    $weight1_metrics = $_POST['cat4_metric1_weight'];
    $weight2_metrics = $_POST['cat4_metric2_weight'];
    $weight3_metrics = $_POST['cat4_metric3_weight'];
    $weight4_metrics = $_POST['cat4_metric4_weight'];

    // Delete the old weights
    $delete_sql = "DELETE FROM weights";
    mysqli_query($conn, $delete_sql);

    // Insert the new weights
    $insert_sql = "INSERT INTO weights (speed_customer_weight, accuracy_customer_weight, cust_service_customer_weight, speed_store_weight, accuracy_store_weight, customer_service_weight, speed_broker_weight, accuracy_broker_weight, cust_service_broker_weight, avg_dist_weight, overhead_weight, startwork_diff_weight, endwork_diff_weight) VALUES ('$weight1_customer', '$weight2_customer', '$weight3_customer', '$weight1_store', '$weight2_store', '$weight3_store', '$weight1_broker', '$weight2_broker', '$weight3_broker', '$weight1_metrics', '$weight2_metrics', '$weight3_metrics', '$weight4_metrics')";

    if (mysqli_query($conn, $insert_sql)) {
        echo "Weights updated successfully";
    } else {
        echo "Error updating weights: " . mysqli_error($conn);
    }

    // Close the database connection
    mysqli_close($conn);
}
?>