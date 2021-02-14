<?php
echo "Hi";

$output = null;
$retval = null;
exec('sudo python3 /home/pi/LEDs/clear.py', $output, $retval);
echo "Returned with status $retval and output:\n";
print_r($output);

//echo '<br>output: ' . shell_exec("sudo python3 /home/pi/LEDs/clear.py");


 ?>
