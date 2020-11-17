<?php

# FLASK-ENV IN LOCATION: /var/app/current

echo "Post Request Testing...\n";
#Change url to change who you send post request to
$url = "http://localhost:5000";

#Send Post Requests
$ch = curl_init($url);

function post_TEST($ch) {
	$post = "w=3&arith=\+&num1=101&num2=010";
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	$result = curl_exec($ch);
	echo "\nCAPTURED DATA:\n" . $result;
	curl_close($ch);
}

post_TEST($ch);
echo "\n";



#Send Put Requests
/*$ch = curl_init();

$data = array('name' => 'Foo', 'file' => '@/home/file_path.txt');

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_SAFE_UPLOAD, false); // required as of PHP 5.6.0
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

curl_exec($ch);*/

#Handle Put Requests
/*if ($_SERVER['REQUEST_METHOD'] == 'PUT')
{
	parse_str(file_get_contents("php://input"), $_PUT);*/
?>