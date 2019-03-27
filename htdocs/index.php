

<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <?php include 'head.php' ?>
    </head>
    <body>
        <div class="wrapper ">
            <!-- Sidebar -->
            <div class="sidebar" data-color="purple" data-background-color="white">
                <?php include 'sidebar.php';?>
            </div>

            <div class="main-panel">
                <!-- Navbar -->
                <?php include 'navbar.php' ?>
                <!-- End Navbar -->
                <div class="content">
                    <div class="container-fluid" id="pageContent">
                        <!-- CONTETN GOES HERE -->
                    </div> <!--/container-fluid-->
                </div> <!--/content-->
                <footer class="footer">
                    <div class="container-fluid">
                        <?php include 'footer.php' ?>
                    </div>
                </footer>
            </div> <!--/main-panel-->
        </div> <!--/wrapper-->

        <!-- JS -->
        <?php include 'js.php' ?>
    </body>
</html>
