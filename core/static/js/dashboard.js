$(document).ready(function() {
    $('.task-toggle').on('click', function() {
        var target = $(this).data('target');
        if ($(target).is(':visible')) {
            $(target).slideUp(300);
        } else {
            $(target).slideDown(300);
        }
    });
});
