$('.btn-primary').on('click', function(){
    var bdata = $(this).attr('data-button');
    if (bdata != 'None'){
        window.location.href = ('/?page='+bdata);
    }
});


$('#residentsModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
//   var recipient = button.data('whatever') // Extract info from data-* attributes
  var residentsString = button.data('residents');
  var residentsSubString = residentsString.substr(1).slice(0, -1).replace(/'/g, "").replace(/ /g, "")
  var residentsForPlanet = residentsSubString.split(',')
  Object.values(residentsForPlanet).forEach(function(value) {
        getResidentAttributes(value);
    });
  // for (var i = 0; i < residentsForPlanet.length; i++){
    
  // }
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
      console.log(response['name'])
      });
}