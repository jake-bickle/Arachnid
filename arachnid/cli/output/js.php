<?php

    $json_file = file_get_contents('scraped_data/arachnid_data.json');
    $scraped_data = json_decode($json_file, true);

 ?>

<!--   Core JS Files   -->
<script src="assets/js/core/jquery.min.js"></script>
<script src="assets/js/core/popper.min.js"></script>
<script src="assets/js/core/bootstrap-material-design.min.js"></script>
<script src="assets/js/material-dashboard.js?v=2.1.1" type="text/javascript"></script>

<script type="text/javascript">
    // Tnitialize Boostrap all tooltips on a page
    $(document).ready(function() {
        $("body").tooltip({ selector: '[data-toggle=tooltip]' });


        <?php
            if (!empty($scraped_data["metadata"]["end_time"])) {
                echo "
                    $('#scan-status').find(\"i:first\").html(\"done\").removeClass(\"scanning\")
                    $('#scan-status').css(\"color\", \"green\")
                    $('#scan-status').find(\"span\").html(\"Scan Complete\")
                ";
            } else {
                echo "
                    $('#scan-status').find(\"i:first\").html(\"autorenew\").addClass(\"scanning\")
                    $('#scan-status').css(\"color\", \"orange\")
                    $('#scan-status').find(\"span\").html(\"Scanning\")
                ";
            }

         ?>
         });



</script>

<script src="assets/js/main.js" charset="utf-8"></script>
