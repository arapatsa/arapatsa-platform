$(document).ready(function() {
    $('#delete-button').click(function(){
        $(".wrapper-prompt").addClass("is-shown");
        $(".confirm-delete-course").val(this.getAttribute("data-course-key"))
    });

    $('.confirm-delete-course').click(function(){
        var course_id = $(".confirm-delete-course").val()
        var data = {'course_id': course_id}
        $.ajax({
            "type": "POST",
            "url": "/delete-course",
            "data": data,
            success:function(message){
                window.location = '/home';
            },
            error:function(){
                $(".wrapper-prompt").removeClass("is-shown");
            }
        });
    });

    $('.delete-cancel').click(function(){
        $(".wrapper-prompt").removeClass("is-shown");
    });
})