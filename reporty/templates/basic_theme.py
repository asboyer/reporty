template_dict = {}

template_dict['html_template'] = """ 
	<!DOCTYPE html>
	<html>
	<head>
	<style>
	{1}
	</style>
	</head>
	<body>
	{0}
	</body>
	</html>
	    """
    
template_dict['css'] = """
    body {
      background-color: linen;
    }
    
    h1 {
      color: maroon;
      margin-left: 0px;
    }
    """
    
template_dict['header'] = """
<h1>Your Figures:</h1>
<p>Here are the figures upon request.</p>
    
"""
