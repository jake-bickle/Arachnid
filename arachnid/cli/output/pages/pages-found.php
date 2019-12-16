<?php include '../scraped_data.php' ?>

<h3>All Pages</h3>
<div class="card">
    <div class="card-header card-header-tabs card-header-warning">
        <div class="nav-tabs-navigation">
            <div class="nav-tabs-wrapper">
                <span class="nav-tabs-title">Pages: </span>
                <ul class="nav nav-tabs" data-tabs="tabs">
                    <li class="nav-item">
                        <a class="nav-link active" href="#pages_table" data-toggle="tab">
              <i class="material-icons">reorder</i> Table
              <div class="ripple-container"></div>
            </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link " href="#pages_graph" data-toggle="tab">
              <i class="material-icons">device_hub</i> Graph
              <div class="ripple-container"></div>
            </a>
                    </li>

                </ul>
            </div>
        </div>
    </div>
    <div class="card-body">
        <div class="tab-content">
            <div class="tab-pane active" id="pages_table">
                <table class="table table-hover">
                    <tbody>
                        <?php
                            foreach ($pages as $page) {
                                echo "<tr>";
                                echo "<td> <a href='" . $page[0] ."'>" . $page[0] . "</a></td>";
                                echo "<td>" . $page[2] . "</td>";
                                echo "</tr>";
                            }
                         ?>
                    </tbody>
                </table>
            </div>
            <div class="tab-pane " id="pages_graph">
                <h3>Graph coming soon!</h3>
            </div>

        </div>
        <!-- <a href="#" id="fullscreen-btn"><i class="material-icons">fullscreen</i></a> -->
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <div class="card" id="interesting">
            <div class="card-header card-header-warning">
                <h4 class="card-title">"Interesting" Pages Found</h4>
                <p class="card-category">The following are pages that might be worth exploring</p>
            </div>
            <div class="card-body table-responsive">
                <table class="table table-hover">
                    <tbody>
                        <?php
                            foreach ($interesting_pages as $page) {
                                echo "<tr>";
                                echo "<td> <a href='" . $page ."'>" . $page . "</a></td>";
                                echo "</tr>";
                            }
                         ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <!-- Subdomains -->
    <div class="col-md-6">
        <div class="card" id="interesting">
            <div class="card-header card-header-warning">
                <h4 class="card-title">Subdomains</h4>
            </div>
            <div class="card-body table-responsive">
                <table class="table">
                    <tbody>
                        <?php
                            foreach ($domains as $domain) {
                                echo "<tr>";
                                echo "<td>" . $domain . "</td>";
                                echo "</tr>";
                            }
                         ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
