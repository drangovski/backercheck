$(document).ready(function(){
	
	// Get Tab parameters in Settings page
	$tab = $.url("query").split("=")[1];
	if ($('.tab-checkbox').hasClass($tab)) {
		$('.tab-checkbox' + '.' + $tab).attr('checked', 'checked');
	}

	// Clean URL
	var uri = window.location.toString();
	$('.tab-checkbox').on('click', function(){
		if (uri.indexOf("?") > 0) {
		    var clean_uri = uri.substring(0, uri.indexOf("?"));
		    window.history.replaceState({}, document.title, clean_uri);
		}
	});
	
});