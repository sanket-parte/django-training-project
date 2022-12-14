
$(document).ready(function() {    
    $('#project-submit').click((event)=>{
        event.preventDefault()
        $.ajax({
            dataType : "json",
            url: 'http://127.0.0.1:8000/projects/api/create-project',
            type: 'POST',
            contentType: 'application/json;charset=utf-8',
            data: JSON.stringify({
                "title": $("#id_title").val(),
                "description": $("#id_description").val(),
                "source_url":$("#id_source_url").val(),
                "demo_link":$("#id_demo_link").val(),
                "tags": $('#id_tags').val(),
                "project_image":"",
                "active":true
            }),
            success: function(response){
                console.log('response: ',response);
            },
            error: function(response){
                
            }
        })
    })
})

