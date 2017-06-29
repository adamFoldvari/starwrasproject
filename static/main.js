$('.btn-primary').on('click', function(){
    var bdata = $(this).attr('data-button');
    if (bdata != 'None'){
        window.location.href = ('/?page='+bdata);
    }
});


$('#residentsModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var modal = $(this)
  var planetName = button.data('planet')
  var residentsString = button.data('residents');
  var residentsSubString = residentsString.substr(1).slice(0, -1).replace(/'/g, "").replace(/ /g, "")
  var residentsForPlanet = residentsSubString.split(',')
  Object.values(residentsForPlanet).forEach(function(value) {
        $('.modal-table-body').empty()
        getResidentAttributes(value, modal);
        
    });
  modal.find('.modal-title').text('Residents of ' + planetName)
});
// thats enough for today, take a rest, watch a movie and tommorrow make here ajax requests to get all residents attributes for the planet
// you should use nested for loops i quess.... good luck



  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  // var modal = $(this)
  // modal.find('.modal-title').text('New message to ' + recipient)
  // modal.find('.modal-body input').val(recipient)


function getResidentAttributes(url){
  $.getJSON(url, function(response){
    var newRowContent = "<tr><td>" + response['name'] + "</td><td>" + response['height'] + "</td><td>" + response['mass'] + "</td><td>" + response['hair_color'] +
    "</td><td>" + response['skin_color'] + "</td><td>" + response['eye_color'] + "</td><td>" + response['birth_year']+ "</td><td>"+ response['gender'] + "</td></tr>"
    $('.modal-table-body').append(newRowContent)
      });
}