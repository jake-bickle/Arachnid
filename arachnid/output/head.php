<?php
    $json_file = file_get_contents('scraped_data/arachnid_data.json');
    $scraped_data = json_decode($json_file, true);
?>

<title>Arachnid | The OSINT Crawler</title>
<!-- Required meta tags -->
<meta charset="utf-8">
<meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" name="viewport" />
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<!--     Fonts and icons     -->
<link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Roboto+Slab:400,700|Material+Icons" />
<link rel="stylesheet" href="assets/icons/font-awesome.min.css">
<!-- Material Kit CSS -->
<link href="assets/css/material-dashboard.css?v=2.1.1" rel="stylesheet" />
<link rel="stylesheet" href="assets/css/main.css">
<link rel="icon" href="/favicon.png">

<?php
    if (empty($scraped_data["metadata"]["end_time"])) {
        echo "<meta http-equiv=\"refresh\" content=\"31\">";
    }

 ?>
