<?php
$ip = $_SERVER['REMOTE_ADDR'];
file_put_contents("ip_logs.txt", $ip . PHP_EOL, FILE_APPEND);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file'])) {
        $filename = basename($_FILES['file']['name']);
        $target = "uploads/" . $filename;
        move_uploaded_file($_FILES['file']['tmp_name'], $target);
    }
}
?>
