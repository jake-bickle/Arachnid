<?php include '../scraped_data.php' ?>

<?php

    $data_name_to_display = $_POST['data'];

    if (is_array($$data_name_to_display[0])) {
        echo '<table>';
        foreach ($$data_name_to_display as $data) {
            echo '<tr>';
                for ($i = 0; $i < count($data); $i++ ) {
                    echo '<td>' . $data[$i] . ',' .'</td>';
                }
            echo '</tr>';
        }
        echo '</table>';
    } else {
        foreach ($$data_name_to_display as $data) {
            echo $data . "<br>";
        }
    }



 ?>
