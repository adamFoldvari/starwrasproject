$('.btn-primary').on('click', function(){
    var bdata = $(this).attr('data-button');
    if (bdata != 'None'){
        window.location.href = ('/?page='+bdata);
    }
});