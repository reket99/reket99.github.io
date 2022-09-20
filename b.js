var req = new XMLHttpRequest();
req.open('GET', 'https://link.nhl.com/iami/admin/rest/role?', false) 
req.send();
alert(req.responseText)
