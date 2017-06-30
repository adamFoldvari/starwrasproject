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
  modal.find('.modal-title').text('Residents of ' + planetName)
  var residentsString = button.data('residents');
  var residentsSubString = residentsString.substr(1).slice(0, -1).replace(/'/g, "").replace(/ /g, "")
  var residentsForPlanet = residentsSubString.split(',')
  Object.values(residentsForPlanet).forEach(function(value) {
        value = [value.slice(0, 4), 's', value.slice(4)].join('');
        $('.modal-table-body').empty()
        getResidentAttributes(value);
    });
});

function getResidentAttributes(url){
  $.getJSON(url, function(response){
    var newRowContent = "<tr><td>" + response['name'] + "</td><td>" + response['height'] + "</td><td>" + response['mass'] + "</td><td>" + response['hair_color'] +
    "</td><td>" + response['skin_color'] + "</td><td>" + response['eye_color'] + "</td><td>" + response['birth_year']+ "</td><td>"+ response['gender'] + "</td></tr>"
    $('.modal-table-body').append(newRowContent)
      });
}