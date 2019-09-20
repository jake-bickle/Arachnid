<?php include '../scraped_data.php' ?>

<?php

    $data_name_to_display = $_POST['data'];

    // print_r($$data_name_to_display);
    foreach ($$data_name_to_display as $data) {
        print_r($data);
        echo "<br>";
    }
 ?>
