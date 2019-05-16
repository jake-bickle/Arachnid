
<?php include '../scraped_data.php' ?>

<h3>Scraped Data</h3>

<div class="row" id="scraped-data-blocks">
    <!-- EMAILS -->
    <div class="col-md-4" <?php if (count($emails) < 1) {echo "style='display:none'";}?>>
        <div class="card">
          <div class="card-header">
            <h4 class="card-title"><i class="material-icons">email</i>Emails Found</h4>
          </div>
          <div class="card-body table-responsive">
              <table class="table table-hover">
                <tbody>
                    <?php
                        foreach ($emails as $email) {
                            echo "<tr>";
                            echo "<td>".$email."</td>";
                            echo "</tr>";
                        }
                     ?>
                </tbody>
              </table>
          </div>
        </div>
    </div>

    <!-- PHONE NUMBER -->
    <div class="col-md-4" <?php if (count($phone_numbers) < 1) {echo "style='display:none'";}?>>
        <div class="card">
          <div class="card-header">
            <h4 class="card-title"><i class="material-icons">phone</i>Phone Numbers Found</h4>
          </div>
          <div class="card-body table-responsive">
              <table class="table table-hover">
                <tbody>
                    <?php
                        foreach ($phone_numbers as $number) {
                            echo "<tr>";
                            echo "<td>".$number."</td>";
                            echo "</tr>";
                        }
                     ?>
                </tbody>
              </table>
          </div>
        </div>
    </div>

    <!-- SOCIAL MEDIA -->
    <div class="col-md-4" <?php if (count($social_links) < 1) {echo "style='display:none'";}?>>
        <div class="card">
          <div class="card-header">
            <h4 class="card-title">Social Media Links</h4>
          </div>
          <div class="card-body table-responsive">
              <table class="table table-hover">
                <tbody>
                    <?php
                        foreach ($social_links as $link) {
                            echo "<tr>";
                            echo "<td> <a href=' " . $link[0] . " '> " .$link[0]."</a></td>";
                            echo "</tr>";
                        }
                     ?>
                </tbody>
              </table>
          </div>
        </div>
    </div>

    <!-- CUSTOM REGEX-->
    <div class="col-md-4" <?php if (count($custom_regex) < 1) {echo "style='display:none'";}?>>
        <div class="card">
          <div class="card-header">
            <h4 class="card-title">Custom Regex Results</h4>
          </div>
          <div class="card-body table-responsive">
              <table class="table table-hover">
                <tbody>
                    <?php
                        foreach ($custom_regex as $result) {
                            echo "<tr>";
                            echo "<td>".$result."</td>";
                            echo "</tr>";
                        }
                     ?>
                </tbody>
              </table>
          </div>
        </div>
    </div>

</div>

<script type="text/javascript">
    // Dynamiclly assign header colors using JS based on number of things assigned.
    var blockColors = [
        'card-header-warning',
        'card-header-primary',
        'card-header-danger',
        'card-header-success',
        'card-header-info',
    ]
    var x = 0;
    $(".card-header").each(function(){
        if (x <= 4) {
            $(this).addClass(blockColors[x])
            console.log("Assigning header of " + blockColors[x])
            x++
        } else {
            x = 0
            $(this).addClass(blockColors[x])
            console.log("Assigning header of " + blockColors[x])
        }
    });
</script>
