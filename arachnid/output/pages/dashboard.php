<?php include '../scraped_data.php' ?>

<h1 id="dashboardTitle">Site Report for <span class="fullSiteURL"><?php echo $site_title ?></span></h1>
<hr>
<!-- SUMMARY BLOCKS -->
<div class="row" id="summaryBlocks">
    <div class="col-lg-3 col-md-6 col-sm-6">

        <!-- Number of Pages Summary Block -->
        <div class="card card-stats" id="pagesSummary">
            <div class="card-header card-header-warning card-header-icon">
                <div class="card-icon">
                    <i class="material-icons">content_copy</i>
                </div>
                <p class="card-category">Pages Found</p>
                <h3 class="card-title numOfPages"> <?php echo count($pages) ?> </h3>
            </div>
            <div class="card-footer">
            </div>
        </div>
    </div>

    <!-- Number of emails summary block -->
    <div class="col-lg-3 col-md-6 col-sm-6">
        <div class="card card-stats" id="emailSummary">
            <div class="card-header card-header-info card-header-icon">
                <div class="card-icon">
                    <i class="material-icons">alternate_email</i>
                </div>
                <p class="card-category">Emails Found</p>
                <h3 class="card-title numOfEmails"><?php echo count($emails) ?></h3>
            </div>
            <div class="card-footer">
            </div>
        </div>
    </div>

    <!-- Number of phone numbers summary block -->
    <div class="col-lg-3 col-md-6 col-sm-6">
        <div class="card card-stats">
            <div class="card-header card-header-danger card-header-icon">
                <div class="card-icon">
                    <i class="material-icons">phone</i>
                </div>
                <p class="card-category">Numbers Found</p>
                <h3 class="card-title"><?php echo count($phone_numbers) ?></h3>
            </div>
            <div class="card-footer">
            </div>
        </div>
    </div>

    <!-- Social Handles -->
    <div class="col-lg-3 col-md-6 col-sm-6">
        <div class="card card-stats">
            <div class="card-header card-header-primary card-header-icon">
                <div class="card-icon">
                    <i class="material-icons">share</i>
                </div>
                <p class="card-category">Social Handles</p>
                <h3 class="card-title"><?php echo count($social_links) ?></h3>
            </div>
            <div class="card-footer">
            </div>
        </div>
    </div>

</div>

<div class="row">
    <!-- Scan Info-->
    <div class="col-md-6">
      <div class="card" id="scan-info">
        <div class="card-header card-header-warning">
          <h4 class="card-title">Scan Overview</h4>
          <p class="card-category">The following are the options set for the scan</p>
        </div>
        <div class="card-body">
            <?php
                echo "<pre>" . json_encode( $scraped_data["metadata"], JSON_PRETTY_PRINT) . "</pre>" ;
             ?>
        </div>
      </div>
    </div>

    <!-- Errors and Alrts -->
    <div class="col-md-6">
      <div class="card" id="crawl-errors">
        <div class="card-header card-header-danger">
          <h4 class="card-title">Crawl Alerts </h4>
          <p class="card-category">The following alerts generated during the crawl</p>
        </div>
        <div class="card-body table-responsive">
            <table class="table table-hover">
              <tbody>

                  <?php

                      if (isset($all_warnings)){
                          foreach ($all_warnings as $single_warning) {
                              echo "<tr>";
                              echo "<td> <a href='" . $single_warning[0] ."'>" . $single_warning[0] . "</a></td>";
                              echo "<td> <i class=\"material-icons\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"" . $single_warning[1] . "\">info</i></td>";
                              echo "</tr>";
                          }
                      }

                   ?>
                <!-- <tr>
                    <td><i class="material-icons">warning</i></td>
                    <td>This is an example error</td>
                    <td><i class="material-icons" data-toggle="tooltip" data-placement="bottom" title="Information about this error">info</i></td>
                </tr> -->
              </tbody>
            </table>
        </div>
      </div>
    </div>
</div>
