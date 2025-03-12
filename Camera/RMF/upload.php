<?php
$uploadDir = "photos/";
if (!is_dir($uploadDir)) mkdir($uploadDir);
if (isset($_FILES["photo"])) {
    $filename = $uploadDir . time() . ".jpg";
    move_uploaded_file($_FILES["photo"]["tmp_name"], $filename);
}
?>
