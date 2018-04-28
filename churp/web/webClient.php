<?php

session_start();

$host = "127.0.0.1";
$port = 12001;
// No Timeout 
set_time_limit(0);

$socket = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP) or die("Could not create socket\n");

$result = socket_connect($socket, $host, $port) or die("Could not connect to server\n");

$username= "1:trollBoxer";
$usernameProtocol = base64_encode($username);

socket_write($socket, $usernameProtocol, strlen($usernameProtocol));
/*
$msg = "2:trollBoxer:hello there#000000";
socket_write($socket, $msg, strlen($msg));
*/
while (true)
{
	$rawData = socket_read ($socket, 1024) or die("Could not read server response\n");
	$result = base64_decode($rawData);
	$result = substr($result, 0, -7);
	echo $result."\n";
}

socket_close($socket);

?>