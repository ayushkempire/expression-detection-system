$(document).ready(function() {
	document.getElementById('upload-button').addEventListener('click', function() {
		document.getElementById('file-input').click();
	});
	
	document.getElementById('file-input').addEventListener('change', function() {
		if(this.files.length > 0){
			document.getElementById('file-submit').click();
		}
	});

	$('#upload-form').on('submit', function(event) {
		event.preventDefault();
		var formData = new FormData(this);
		$('#message').html('<span class="analysis-msg"><img src="/static/img/loading.svg"><span>Uploading image... Please wait.</span></span>');
		$.ajax({
			url: '/upload',
			type: 'POST',
			data: formData,
			contentType: false,
			processData: false,
			success: function(response) {
				document.querySelector(".ic").setAttribute("style","display: none;")
				$('#uploaded-image').attr('src', '/' + response.file_path).show();
				$('#message').html('<span class="analysis-msg"><img src="/static/img/loading.svg"><span>Analyzing facial expressions... Please wait.</span></span>');
				
				$.ajax({
					url: '/analyze',
					type: 'GET',
					success: function(response){
						$('#message').html('<span class="result-msg">Expression detected:&nbsp;&nbsp;<span class="bold">' + response.emotion + '</span></span>');
					},
					error: function(response){
						$('#message').html('<span class="error-msg"><img src="/static/img/error.svg"><span>Error analyzing the image.</span></span>');
					}
				});
			},
			error: function(response) {
				$('#message').html('<span class="error-msg"><img src="/static/img/error.svg"><span>Error uploading the image.</span></span>');
			}
		});
	});
});