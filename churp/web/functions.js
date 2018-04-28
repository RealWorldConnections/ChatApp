function login()
{
	var user = document.getElementById("user").value;
	
	console.log("User: " + user);
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() 
	{
		if (this.readyState == 4 && this.status == 200) {
			// Typical action to be performed when the document is ready:
			document.getElementById("demo").innerHTML = xhttp.responseText;
		}
	};
	xhttp.open("POST", "filename", true);
	xhttp.send();
}