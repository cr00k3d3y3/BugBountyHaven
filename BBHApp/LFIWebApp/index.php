<?php
// Ensure uploads dir exists and is writable
if (!file_exists('uploads')) {
    mkdir('uploads', 0777, true);
}

// File upload logic
if (isset($_FILES['file'])) {
    $target = "uploads/" . basename($_FILES['file']['name']);
    if (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
        echo "✅ File uploaded: " . htmlspecialchars($target);
    } else {
        echo "❌ Upload failed.";
    }
}

// LFI include
if (isset($_GET['page'])) {
    $page = $_GET['page'];
    if (pathinfo($page, PATHINFO_EXTENSION) === 'txt') {
        readfile($page);
    } else {
        include($page);
    }
}

include("nav.php");

?>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="Upload">
</form>
